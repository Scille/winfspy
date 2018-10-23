import argparse
import time

from winfspy._base_file_system_interface import BaseFileSystemUserContext
from winfspy._ll_file_system_interface import file_system_interface_factory
from winfspy._ll_service import run_service, BaseServiceUserContext
from winfspy._ll_volume_params import volume_params_factory
from winfspy.bindings import lib, ffi
from winfspy.filetime import filetime_now
from winfspy.ntstatus import nt_success, cook_ntstatus, NTSTATUS
from winfspy.file_attributes import FILE_ATTRIBUTE
from winfspy import start_fs

from pathlib import PureWindowsPath


class BaseFileObj:
    @property
    def name(self):
        return self.path.name

    def __init__(self, path):
        self.path = path
        now = filetime_now()
        self.creation_time = now
        self.last_access_time = now
        self.last_write_time = now
        self.change_time = now
        self.index_number = 0

        self.security_descriptor = ffi.NULL
        self.security_descriptor_size = 0


class FileObj(BaseFileObj):
    def __init__(self, path):
        super().__init__(path)
        self.file_size = 0
        self.allocation_size = 4096

    @property
    def attributes(self):
        return FILE_ATTRIBUTE.FILE_ATTRIBUTE_NORMAL


class FolderObj(BaseFileObj):
    def __init__(self, path):
        super().__init__(path)
        self.file_size = 4096
        self.allocation_size = 4096

    @property
    def attributes(self):
        return FILE_ATTRIBUTE.FILE_ATTRIBUTE_DIRECTORY


class OpenedObj:
    def __init__(self, file_obj):
        self.file_obj = file_obj


class InMemoryFileSystemContext(BaseFileSystemUserContext):
    def __init__(self, volume_label):
        if len(volume_label) > 31:
            raise ValueError("`volume_label` must be 31 characters long max")
        self.volume_label = volume_label
        self.max_file_nodes = 1024
        self.max_file_size = 16 * 1024 * 1024
        self.file_nodes = 1

        self._opened = {}
        root_path = PureWindowsPath("/")
        self._entries = {
            root_path: FolderObj(root_path),
            root_path / "foo": FolderObj(root_path / "foo"),
            root_path / "foo/spam.txt": FileObj(root_path / "foo/spam.txt"),
            root_path / "bar.txt": FileObj(root_path / "bar.txt"),
        }

    def get_volume_info(self, volume_info):
        volume_info.TotalSize = self.max_file_nodes * self.max_file_size
        volume_info.FreeSize = (
            self.max_file_nodes - self.file_nodes
        ) * self.max_file_size
        volume_info.VolumeLabel = self.volume_label
        volume_info.VolumeLabelLength = (
            len(self.volume_label) * 2
        )  # Because stored in WCHAR
        # volume_label_utf16 = self.volume_label.encode('utf-16')
        # volume_label_utf16_size = len(volume_label_utf16)
        # volume_info.VolumeLabelLength = len(volume_label_utf16)
        # ffi.memmove(volume_info.VolumeLabel, volume_label_utf16, len(volume_label_utf16))

        return NTSTATUS.STATUS_SUCCESS

    def set_volume_label(self, volume_label, volume_info):
        assert len(self.volume_label) < 32
        self.volume_label = ffi.string(volume_label)

        return self.get_volume_info(volume_info)

    def get_security_by_name(
        self,
        file_name,
        p_file_attributes_or_reparse_point_index,
        security_descriptor,
        p_security_descriptor_size,
    ):
        file_name = PureWindowsPath(ffi.string(file_name))
        print("GET_SECURITY_BY_NAME ++++>", file_name)

        # Retrieve file
        try:
            file_obj = self._entries[file_name]
        except KeyError:
            return NTSTATUS.STATUS_OBJECT_NAME_NOT_FOUND

        # Get file attributes
        if p_file_attributes_or_reparse_point_index != ffi.NULL:
            p_file_attributes_or_reparse_point_index[0] = file_obj.attributes

        # Get file security
        # TODO
        if p_security_descriptor_size != ffi.NULL:
            if file_obj.security_descriptor_size > p_security_descriptor_size[0]:
                return NTSTATUS.STATUS_BUFFER_OVERFLOW
            p_security_descriptor_size[0] = file_obj.security_descriptor_size

            if security_descriptor != ffi.NULL:
                ffi.memmove(
                    security_descriptor,
                    file_obj.security_descriptor,
                    file_obj.security_descriptor_size,
                )

        return NTSTATUS.STATUS_SUCCESS

    @staticmethod
    def _copy_file_info(file_obj, file_info):
        file_info.FileAttributes = file_obj.attributes
        file_info.ReparseTag = 0
        file_info.AllocationSize = file_obj.allocation_size
        file_info.FileSize = file_obj.file_size
        file_info.CreationTime = file_obj.creation_time
        file_info.LastAccessTime = file_obj.last_access_time
        file_info.LastWriteTime = file_obj.last_write_time
        file_info.ChangeTime = file_obj.change_time
        file_info.IndexNumber = file_obj.index_number

    def open(
        self, file_name, create_options, granted_access, p_file_context, file_info
    ):
        file_name = PureWindowsPath(ffi.string(file_name))
        print("OPEN ++++>", file_name)

        # Retrieve file
        try:
            file_obj = self._entries[file_name]
        except KeyError:
            return NSTATUS.STATUS_OBJECT_NAME_NOT_FOUND

        opened_obj = OpenedObj(file_obj)
        handle = ffi.new_handle(opened_obj)
        self._opened[handle] = opened_obj
        p_file_context[0] = handle

        self._copy_file_info(file_obj, file_info)

        return NTSTATUS.STATUS_SUCCESS

    def close(self, file_context):
        del self._opened[file_context]

    def read_directory(
        self, file_context, pattern, marker, buffer, length, p_bytes_transferred
    ):
        opened_obj = ffi.from_handle(file_context)
        file_obj = opened_obj.file_obj

        class NotEnoughSpace(Exception):
            pass

        def _add_dir_info(entry_obj, name=None):
            # Optimization FTW... FSP_FSCTL_DIR_INFO must be allocated along
            # with it last field (FileNameBuf which is a string)
            if not name:
                name = entry_obj.name
            file_name_size = (len(name) + 1) * 2  # WCHAR string + NULL byte
            dir_info_size = ffi.sizeof("FSP_FSCTL_DIR_INFO") + file_name_size
            dir_info_raw = ffi.new("char[]", dir_info_size)
            dir_info = ffi.cast("FSP_FSCTL_DIR_INFO*", dir_info_raw)
            dir_info.FileNameBuf = name
            dir_info.Size = dir_info_size
            self._copy_file_info(entry_obj, dir_info.FileInfo)
            if not lib.FspFileSystemAddDirInfo(
                dir_info, buffer, length, p_bytes_transferred
            ):
                raise NotEnoughSpace()

        try:
            _add_dir_info(file_obj, name=".")
            if opened_obj.file_obj.path != PureWindowsPath("/"):
                parent_file_obj = self._entries[opened_obj.file_obj.path.parent]
                _add_dir_info(parent_file_obj, name="..")

            for entry_path, entry_obj in self._entries.items():
                try:
                    relative = entry_path.relative_to(file_obj.path)
                    # Not interested into ourself or our grandchildren
                    if len(relative.parts) == 1:
                        _add_dir_info(entry_obj)
                except ValueError:
                    continue
        except NotEnoughSpace:
            pass

        lib.FspFileSystemAddDirInfo(ffi.NULL, buffer, length, p_bytes_transferred)

        return NTSTATUS.STATUS_SUCCESS


# def file_system_interface_factory(user_context):
#     if not isinstance(user_context, BaseFileSystemIterfaceUserContext):
#         raise ValueError(
#             f"`user_context` must be of type `{BaseFileSystemIterfaceUserContext.__qualname__}`"
#         )
#     # file_system_interface.UserContext = ffi.new_handle(user_context)


def enable_debug_log():
    stderr_handle = lib.GetStdHandle(lib.STD_ERROR_HANDLE)
    lib.FspDebugLogSetHandle(stderr_handle)


# def volume_params_factory(file_system_name, volume_prefix=None):
#     volume_params = ffi.new("FSP_FSCTL_VOLUME_PARAMS*")
#     volume_params.SectorSize = 512 # dunno what's the size of `ALLOCATION_UNIT`
#     volume_params.SectorsPerAllocationUnit = 1
#     volume_params.VolumeCreationTime = filetime_now()
#     volume_params.VolumeSerialNumber = 0
#     volume_params.FileInfoTimeout = 1000
#     # volume_params.CaseSensitiveSearch = 0
#     # volume_params.CasePreservedNames = 1
#     # volume_params.UnicodeOnDisk = 1
#     # volume_params.PersistentAcls = 1
#     # volume_params.PostCleanupWhenModifiedOnly = 1
#     # volume_params.UmFileContextIsUserContext2 = 1
#     if volume_prefix:
#         volume_params.Prefix = volume_prefix

#     volume_params.FileSystemName = file_system_name

#     return volume_params


class ServiceUserContext(BaseServiceUserContext):
    def __init__(self, mountpoint):
        self.mountpoint = mountpoint

    def on_start(self, argc, argv):
        print("----------------")
        try:
            run_fs(self.mountpoint)
        except Exception as exc:
            import traceback

            traceback.print_tb(exc.__traceback__)
            print(repr(exc))
            return NTSTATUS.STATUS_UNSUCCESSFUL
        return NTSTATUS.STATUS_SUCCESS

    def on_stop(self):
        return NTSTATUS.STATUS_SUCCESS

    def on_control(self, a, b, c):
        return NTSTATUS.STATUS_SUCCESS


def run_fs(mountpoint):
    file_system_interface = file_system_interface_factory()
    volume_params = volume_params_factory(
        sector_size=512,
        sectors_per_allocation_unit=1,
        volume_creation_time=filetime_now(),
        volume_serial_number=0,
        file_info_timeout=1000,
        case_sensitive_search=0,
        case_preserved_names=0,
        unicode_on_disk=1,
        persistent_acls=1,
        post_cleanup_when_modified_only=1,
        um_file_context_is_user_context2=1,
        file_system_name=mountpoint,
        prefix="",
    )
    file_system_ptr = ffi.new("FSP_FILE_SYSTEM**")

    print("init...")
    result = lib.FspFileSystemCreate(
        "WinFsp.Disk", volume_params, file_system_interface, file_system_ptr
    )
    if not nt_success(result):
        raise WindowsError(f"Cannot create file system: {cook_ntstatus(result).name}")

    # lib.FspFileSystemSetDebugLog(file_system_ptr, DebugFlags);

    file_system_context = InMemoryFileSystemContext(mountpoint)
    file_system_context_handle = ffi.new_handle(
        file_system_context
    )  # Avoid GC on the handle
    file_system_ptr[0].UserContext = file_system_context_handle

    result = lib.FspFileSystemSetMountPoint(file_system_ptr[0], mountpoint)
    if not nt_success(result):
        raise WindowsError(f"Cannot mount file system: {cook_ntstatus(result).name}")

    try:
        print("starting...")
        lib.FspFileSystemStartDispatcher(file_system_ptr[0], 0)
        print("done...")
        time.sleep(10)
    finally:
        print("closing...")
        lib.FspFileSystemDelete(file_system_ptr[0])


def main(mountpoint):
    enable_debug_log()

    service_context = BaseServiceUserContext()
    # service_context = ServiceUserContext(mountpoint)
    with run_service("bazinga", service_context, allow_console_mode=True):
        print("running")
        run_fs(mountpoint)
        print("stopping")

    # FspFileSystemSetDebugLog(file_system_ptr, DebugFlags);


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mountpoint")
    parser.add_argument("-d", dest="debug", action="store_true")
    args = parser.parse_args()
    main(args.mountpoint)
    # start_fs(args.mountpoint, debug=args.debug)
