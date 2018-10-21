import argparse
import time

from winfspy._base_file_system_interface import BaseFileSystemUserContext
from winfspy._ll_file_system_interface import file_system_interface_factory
from winfspy._ll_service import run_service, BaseServiceUserContext
from winfspy._ll_volume_params import volume_params_factory
from winfspy.bindings import lib, ffi
from winfspy.filetime import filetime_now
from winfspy.ntstatus import nt_success, cook_ntstatus
from winfspy import start_fs


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


def main(mountpoint):
    enable_debug_log()

    service_context = BaseServiceUserContext()
    with run_service("bazinga", service_context, allow_console_mode=True):

        file_system_interface = file_system_interface_factory()
        import pdb; pdb.set_trace()
        volume_params = volume_params_factory(sector_size=512, sectors_per_allocation_unit=1, volume_creation_time=filetime_now(), volume_serial_number=0, file_info_timeout=1000,
            case_sensitive_search=0, case_preserved_names=0, unicode_on_disk=1, persistent_acls=1, post_cleanup_when_modified_only=1, um_file_context_is_user_context2=1,
            file_system_name=mountpoint, prefix="")
        file_system_ptr = ffi.new('FSP_FILE_SYSTEM**')

        print('init...')
        result = lib.FspFileSystemCreate(
            mountpoint,
            volume_params,
            file_system_interface,
            file_system_ptr
        )
        if not nt_success(result):
            raise WindowsError(f"Cannot create file system: {cook_ntstatus(result).name}")

        file_system_context = BaseFileSystemUserContext()
        file_system_ptr[0].UserContext = ffi.new_handle(file_system_context)


        try:
            print('starting...')
            lib.FspFileSystemStartDispatcher(file_system_ptr[0], 0)
            print('done...')
            time.sleep(1)
        finally:
            print('closing...')
            lib.FspFileSystemDelete(file_system_ptr[0])

    # FspFileSystemSetDebugLog(file_system_ptr, DebugFlags);


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mountpoint")
    parser.add_argument("-d", dest='debug', action='store_true')
    args = parser.parse_args()
    main(args.mountpoint)
    # start_fs(args.mountpoint, debug=args.debug)
