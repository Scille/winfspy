import sys
import logging
import threading
from typing import List
from functools import wraps

from .plumbing.winstuff import NTSTATUS, SecurityDescriptor
from .plumbing.bindings import lib, ffi
from .exceptions import NTStatusError


logger = logging.getLogger("winfspy")


def _catch_unhandled_exceptions(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if sys.gettrace() != threading._trace_hook:
            sys.settrace(threading._trace_hook)
        try:
            return fn(*args, **kwargs)

        except BaseException:
            logger.exception("Unhandled exception")
            return NTSTATUS.STATUS_UNEXPECTED_IO_ERROR

    return wrapper


# Because `encode('UTF16')` appends a BOM a the begining of the output
_STRING_ENCODING = "UTF-16-LE" if sys.byteorder == "little" else "UTF-16-BE"


class BaseFileContext:
    pass


def configure_file_info(file_info, **kwargs):
    file_info.FileAttributes = kwargs.get("file_attributes", 0)
    file_info.ReparseTag = kwargs.get("reparse_tag", 0)
    file_info.AllocationSize = kwargs.get("allocation_size", 0)
    file_info.FileSize = kwargs.get("file_size", 0)
    file_info.CreationTime = kwargs.get("creation_time", 0)
    file_info.LastAccessTime = kwargs.get("last_access_time", 0)
    file_info.LastWriteTime = kwargs.get("last_write_time", 0)
    file_info.ChangeTime = kwargs.get("change_time", 0)
    file_info.IndexNumber = kwargs.get("index_number", 0)


class BaseFileSystemOperations:
    def __init__(self):
        self._opened_objs = {}

    # ~~~ GET_VOLUME_INFO ~~~

    @_catch_unhandled_exceptions
    def ll_get_volume_info(self, volume_info) -> NTSTATUS:
        """
        Get volume information.
        """
        try:
            vi = self.get_volume_info()

        except NTStatusError as exc:
            return exc.value

        volume_info.TotalSize = vi["total_size"]
        volume_info.FreeSize = vi["free_size"]

        volume_label_encoded = vi["volume_label"].encode(_STRING_ENCODING)
        if len(volume_label_encoded) > 64:
            raise ValueError(
                "`volume_label` should be at most 64 bytes long once encoded in UTF16 !"
            )
        ffi.memmove(volume_info.VolumeLabel, volume_label_encoded, len(volume_label_encoded))
        # The volume label length must be reported in bytes (and without NULL bytes at the end)
        volume_info.VolumeLabelLength = len(volume_label_encoded)

        return NTSTATUS.STATUS_SUCCESS

    def get_volume_info(self) -> dict:
        """
        Dict fields:
            - total_size
            - free_size
            - volume_label
        """
        raise NotImplementedError()

    # ~~~ SET_VOLUME_LABEL ~~~

    @_catch_unhandled_exceptions
    def ll_set_volume_label(self, volume_label, volume_info) -> NTSTATUS:
        """
        Set volume label.
        """
        cooked_volume_label = ffi.string(volume_label)
        if len(cooked_volume_label) > 32:
            return NTSTATUS.STATUS_INVALID_VOLUME_LABEL

        try:
            self.set_volume_label(cooked_volume_label)

        except NTStatusError as exc:
            return exc.value

        return self.ll_get_volume_info(volume_info)

    def set_volume_label(self, volume_label: str) -> None:
        raise NotImplementedError()

    # ~~~ GET_SECURITY_BY_NAME ~~~

    @_catch_unhandled_exceptions
    def ll_get_security_by_name(
        self,
        file_name,
        p_file_attributes_or_reparse_point_index,
        security_descriptor,
        p_security_descriptor_size,
    ) -> NTSTATUS:
        """
        Get file or directory attributes and security descriptor given a file name.
        """
        cooked_file_name = ffi.string(file_name)
        try:
            fa, sd, sd_size = self.get_security_by_name(cooked_file_name)

        except NTStatusError as exc:
            return exc.value

        # Get file attributes
        if p_file_attributes_or_reparse_point_index != ffi.NULL:
            # TODO: wrap attributes with an enum ?
            p_file_attributes_or_reparse_point_index[0] = fa

        # Get file security
        if p_security_descriptor_size != ffi.NULL:
            if sd_size > p_security_descriptor_size[0]:
                # In case of overflow error, winfsp will retry with a new
                # allocation based on `p_security_descriptor_size`. Hence we
                # must update this value to the required size.
                p_security_descriptor_size[0] = sd_size
                return NTSTATUS.STATUS_BUFFER_OVERFLOW
            p_security_descriptor_size[0] = sd_size

            if security_descriptor != ffi.NULL:
                ffi.memmove(security_descriptor, sd, sd_size)

        return NTSTATUS.STATUS_SUCCESS

    def get_security_by_name(self, file_name):
        """
        Returns: (file_attributes, security_descriptor, security_descriptor_size)
        """
        raise NotImplementedError()

    # ~~~ CREATE ~~~

    @_catch_unhandled_exceptions
    def ll_create(
        self,
        file_name,
        create_options,
        granted_access,
        file_attributes,
        security_descriptor,
        allocation_size,
        p_file_context,
        file_info,
    ) -> NTSTATUS:
        """
        Create new file or directory.
        """
        cooked_file_name = ffi.string(file_name)

        # `granted_access` is already handle by winfsp

        security_descriptor = SecurityDescriptor.from_cpointer(security_descriptor)

        try:
            cooked_file_context = self.create(
                cooked_file_name,
                create_options,
                granted_access,
                file_attributes,
                security_descriptor,
                allocation_size,
            )

        except NTStatusError as exc:
            return exc.value

        file_context = ffi.new_handle(cooked_file_context)
        p_file_context[0] = file_context
        # Prevent GC on obj and it handle
        self._opened_objs[file_context] = cooked_file_context

        return self.ll_get_file_info(file_context, file_info)

    def create(
        self,
        file_name,
        create_options,
        granted_access,
        file_attributes,
        security_descriptor,
        allocation_size,
    ) -> BaseFileContext:
        raise NotImplementedError()

    # ~~~ OPEN ~~~

    @_catch_unhandled_exceptions
    def ll_open(
        self, file_name, create_options, granted_access, p_file_context, file_info
    ) -> NTSTATUS:
        """
        Open a file or directory.
        """
        cooked_file_name = ffi.string(file_name)

        try:
            cooked_file_context = self.open(cooked_file_name, create_options, granted_access)

        except NTStatusError as exc:
            return exc.value

        file_context = ffi.new_handle(cooked_file_context)
        p_file_context[0] = file_context
        # Prevent GC on obj and it handle
        self._opened_objs[file_context] = cooked_file_context

        return self.ll_get_file_info(file_context, file_info)

    def open(self, file_context) -> BaseFileContext:
        raise NotImplementedError()

    # ~~~ OVERWRITE ~~~

    @_catch_unhandled_exceptions
    def ll_overwrite(
        self,
        file_context,
        file_attributes,
        replace_file_attributes: bool,
        allocation_size: int,
        file_info,
    ) -> NTSTATUS:
        """
        Overwrite a file.
        """
        cooked_file_context = ffi.from_handle(file_context)
        try:
            self.overwrite(
                cooked_file_context, file_attributes, replace_file_attributes, allocation_size,
            )

        except NTStatusError as exc:
            return exc.value

        return self.ll_get_file_info(file_context, file_info)

    def overwrite(
        self, file_context, file_attributes, replace_file_attributes: bool, allocation_size: int,
    ) -> None:
        raise NotImplementedError()

    # ~~~ CLEANUP ~~~

    @_catch_unhandled_exceptions
    def ll_cleanup(self, file_context, file_name, flags: int) -> None:
        """
        Cleanup a file.
        """
        cooked_file_context = ffi.from_handle(file_context)
        if file_name:
            cooked_file_name = ffi.string(file_name)
        else:
            cooked_file_name = None
        # TODO: convert flags into kwargs ?
        try:
            self.cleanup(cooked_file_context, cooked_file_name, flags)

        except NTStatusError as exc:
            return exc.value

    def cleanup(self, file_context, file_name, flags) -> None:
        raise NotImplementedError()

    # ~~~ CLOSE ~~~

    @_catch_unhandled_exceptions
    def ll_close(self, file_context) -> None:
        """
        Close a file.
        """
        cooked_file_context = ffi.from_handle(file_context)
        try:
            self.close(cooked_file_context)

        except NTStatusError as exc:
            return exc.value

        del self._opened_objs[file_context]

    def close(self, file_context) -> None:
        raise NotImplementedError()

    # ~~~ READ ~~~

    @_catch_unhandled_exceptions
    def ll_read(self, file_context, buffer, offset, length, p_bytes_transferred) -> NTSTATUS:
        """
        Read a file.
        """
        cooked_file_context = ffi.from_handle(file_context)
        try:
            data = self.read(cooked_file_context, offset, length)

        except NTStatusError as exc:
            return exc.value

        ffi.memmove(buffer, data, len(data))
        p_bytes_transferred[0] = len(data)

        return NTSTATUS.STATUS_SUCCESS

    def read(self, file_context, offset: int, length: int) -> bytes:
        raise NotImplementedError()

    # ~~~ WRITE ~~~

    @_catch_unhandled_exceptions
    def ll_write(
        self,
        file_context,
        buffer,
        offset,
        length,
        write_to_end_of_file,
        constrained_io,
        p_bytes_transferred,
        file_info,
    ) -> NTSTATUS:
        """
        Write a file.
        """
        cooked_file_context = ffi.from_handle(file_context)
        cooked_buffer = ffi.buffer(buffer, length)

        try:
            p_bytes_transferred[0] = self.write(
                cooked_file_context, cooked_buffer, offset, write_to_end_of_file, constrained_io,
            )

        except NTStatusError as exc:
            return exc.value

        return self.ll_get_file_info(file_context, file_info)

    def write(self, file_context, buffer, offset, write_to_end_of_file, constrained_io):
        raise NotImplementedError()

    # ~~~ FLUSH ~~~

    @_catch_unhandled_exceptions
    def ll_flush(self, file_context, file_info) -> NTSTATUS:
        """
        Flush a file or volume.
        """
        cooked_file_context = ffi.from_handle(file_context)
        try:
            self.flush(cooked_file_context)

        except NTStatusError as exc:
            return exc.value

        return self.ll_get_file_info(file_context, file_info)

    def flush(self, file_context) -> None:
        raise NotImplementedError()

    # ~~~ GET_FILE_INFO ~~~

    @_catch_unhandled_exceptions
    def ll_get_file_info(self, file_context, file_info) -> NTSTATUS:
        """
        Get file or directory information.
        """
        cooked_file_context = ffi.from_handle(file_context)
        try:
            ret = self.get_file_info(cooked_file_context)

        except NTStatusError as exc:
            return exc.value

        # TODO: handle WIN32 -> POSIX date conversion here ?

        file_info.FileAttributes = ret.get("file_attributes", 0)
        file_info.ReparseTag = ret.get("reparse_tag", 0)
        file_info.AllocationSize = ret.get("allocation_size", 0)
        file_info.FileSize = ret.get("file_size", 0)
        file_info.CreationTime = ret.get("creation_time", 0)
        file_info.LastAccessTime = ret.get("last_access_time", 0)
        file_info.LastWriteTime = ret.get("last_write_time", 0)
        file_info.ChangeTime = ret.get("change_time", 0)
        file_info.IndexNumber = ret.get("index_number", 0)

        return NTSTATUS.STATUS_SUCCESS

    def get_file_info(self, file_context) -> dict:
        raise NotImplementedError()

    # ~~~ SET_BASIC_INFO ~~~

    @_catch_unhandled_exceptions
    def ll_set_basic_info(
        self,
        file_context,
        file_attributes,
        creation_time,
        last_access_time,
        last_write_time,
        change_time,
        file_info,
    ):
        """
        Set file or directory basic information.
        """
        cooked_file_context = ffi.from_handle(file_context)
        # TODO: handle WIN32 -> POSIX date conversion here ?
        try:
            ret = self.set_basic_info(
                cooked_file_context,
                file_attributes,
                creation_time,
                last_access_time,
                last_write_time,
                change_time,
                file_info,
            )

        except NTStatusError as exc:
            return exc.value

        file_info.FileAttributes = ret.get("file_attributes", 0)
        file_info.ReparseTag = ret.get("reparse_tag", 0)
        file_info.AllocationSize = ret.get("allocation_size", 0)
        file_info.FileSize = ret.get("file_size", 0)
        file_info.CreationTime = ret.get("creation_time", 0)
        file_info.LastAccessTime = ret.get("last_access_time", 0)
        file_info.LastWriteTime = ret.get("last_write_time", 0)
        file_info.ChangeTime = ret.get("change_time", 0)
        file_info.IndexNumber = ret.get("index_number", 0)

        return NTSTATUS.STATUS_SUCCESS

    def set_basic_info(
        self,
        file_context,
        file_attributes,
        creation_time,
        last_access_time,
        last_write_time,
        change_time,
        file_info,
    ) -> dict:
        raise NotImplementedError()

    # ~~~ SET_FILE_SIZE ~~~

    @_catch_unhandled_exceptions
    def ll_set_file_size(self, file_context, new_size, set_allocation_size, file_info):
        """
        Set file/allocation size.
        """
        cooked_file_context = ffi.from_handle(file_context)

        try:
            self.set_file_size(cooked_file_context, new_size, set_allocation_size)

        except NTStatusError as exc:
            return exc.value

        return self.ll_get_file_info(file_context, file_info)

    def set_file_size(self, file_context, new_size, set_allocation_size) -> None:
        raise NotImplementedError()

    # ~~~ CAN_DELETE ~~~

    @_catch_unhandled_exceptions
    def ll_can_delete(self, file_context, file_name) -> NTSTATUS:
        """
        Determine whether a file or directory can be deleted.
        """
        cooked_file_context = ffi.from_handle(file_context)
        cooked_file_name = ffi.string(file_name)
        try:
            self.can_delete(cooked_file_context, cooked_file_name)

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def can_delete(self, file_context, file_name: str) -> None:
        raise NotImplementedError()

    # ~~~ RENAME ~~~

    @_catch_unhandled_exceptions
    def ll_rename(self, file_context, file_name, new_file_name, replace_if_exists):
        """
        Renames a file or directory.
        """
        cooked_file_context = ffi.from_handle(file_context)
        cooked_file_name = ffi.string(file_name)
        cooked_new_file_name = ffi.string(new_file_name)

        try:
            self.rename(
                cooked_file_context,
                cooked_file_name,
                cooked_new_file_name,
                bool(replace_if_exists),
            )

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def rename(self, file_context, file_name: str, new_file_name: str, replace_if_exists: bool):
        raise NotImplementedError()

    # ~~~ GET_SECURITY ~~~

    @_catch_unhandled_exceptions
    def ll_get_security(self, file_context, security_descriptor, p_security_descriptor_size):
        """
        Get file or directory security descriptor.
        """
        cooked_file_context = ffi.from_handle(file_context)
        try:
            sd, sd_size = self.get_security(cooked_file_context)

        except NTStatusError as exc:
            return exc.value

        if p_security_descriptor_size != ffi.NULL:
            if sd_size > p_security_descriptor_size[0]:
                return NTSTATUS.STATUS_BUFFER_OVERFLOW
            p_security_descriptor_size[0] = sd_size

            if security_descriptor != ffi.NULL:
                ffi.memmove(security_descriptor, sd, sd_size)

        return NTSTATUS.STATUS_SUCCESS

    def get_security(self, file_context):
        """
        Returns: (security_descriptor, security_descriptor_size)
        """
        raise NotImplementedError()

    # ~~~ SET_SECURITY ~~~

    @_catch_unhandled_exceptions
    def ll_set_security(self, file_context, security_information, modification_descriptor):
        """
        Set file or directory security descriptor.
        """
        cooked_file_context = ffi.from_handle(file_context)
        try:
            self.set_security(cooked_file_context, security_information, modification_descriptor)

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def set_security(self, file_context, security_information, modification_descriptor):
        raise NotImplementedError()

    # ~~~ READ_DIRECTORY ~~~

    @_catch_unhandled_exceptions
    def ll_read_directory(self, file_context, pattern, marker, buffer, length, p_bytes_transferred):
        """
        Read a directory.
        """
        # `pattern` is already handle by winfsp
        cooked_file_context = ffi.from_handle(file_context)
        if marker:
            coocked_marker = ffi.string(marker)
        else:
            coocked_marker = None

        try:
            entries_info = self.read_directory(cooked_file_context, coocked_marker)

        except NTStatusError as exc:
            return exc.value

        for entry_info in entries_info:
            # Optimization FTW... FSP_FSCTL_DIR_INFO must be allocated along
            # with it last field (FileNameBuf which is a string)
            file_name = entry_info["file_name"]
            file_name_encoded = file_name.encode(_STRING_ENCODING)
            # FSP_FSCTL_DIR_INFO base struct + WCHAR[] string
            # Note: Windows does not use NULL-terminated string
            dir_info_size = ffi.sizeof("FSP_FSCTL_DIR_INFO") + len(file_name_encoded)
            dir_info_raw = ffi.new("char[]", dir_info_size)
            dir_info = ffi.cast("FSP_FSCTL_DIR_INFO*", dir_info_raw)
            dir_info.Size = dir_info_size
            ffi.memmove(dir_info.FileNameBuf, file_name_encoded, len(file_name_encoded))
            configure_file_info(dir_info.FileInfo, **entry_info)
            if not lib.FspFileSystemAddDirInfo(dir_info, buffer, length, p_bytes_transferred):
                return NTSTATUS.STATUS_SUCCESS

        lib.FspFileSystemAddDirInfo(ffi.NULL, buffer, length, p_bytes_transferred)
        return NTSTATUS.STATUS_SUCCESS

    def read_directory(self, file_context, marker: str) -> List[dict]:
        """
        Returns a list of info dict.
        Info dict fields:
            file_name
            creation_time
            last_access_time
            last_write_time
            change_time
            index_number
            file_attributes
            allocation_size
            file_size

        Only direct children should be included in this list.
        The special directories "." and ".." should ONLY be included if the queried directory is not root.
        The list has to be consistently sorted.
        The marker argument marks where in the directory to start reading.
        Files with names that are greater than (not equal to) this marker should be returned.
        Might be None, in which case the filtering is disabled.
        """
        raise NotImplementedError()

    # ~~~ RESOLVE_REPARSE_POINTS ~~~

    @_catch_unhandled_exceptions
    def ll_resolve_reparse_points(
        self,
        file_name,
        reparse_point_index: int,
        resolve_last_path_component: bool,
        p_io_status,
        buffer,
        p_size,
    ):
        """
        Resolve reparse points.
        """
        cooked_file_name = ffi.string(file_name)
        # TODO: handle p_io_status, buffer and p_size here
        try:
            self.resolve_reparse_points(
                cooked_file_name,
                reparse_point_index,
                resolve_last_path_component,
                p_io_status,
                buffer,
                p_size,
            )

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def resolve_reparse_points(
        self,
        file_name: str,
        reparse_point_index: int,
        resolve_last_path_component: bool,
        p_io_status,
        buffer,
        p_size,
    ):
        raise NotImplementedError()

    # ~~~ GET_REPARSE_POINT ~~~

    @_catch_unhandled_exceptions
    def ll_get_reparse_point(self, file_context, file_name, buffer, p_size):
        """
        Get reparse point.
        """
        cooked_file_context = ffi.from_handle(file_context)
        cooked_file_name = ffi.string(file_name)
        # TODO: handle buffer and p_size here
        try:
            self.get_reparse_point(cooked_file_context, cooked_file_name, buffer, p_size)

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def get_reparse_point(self, file_context, file_name: str, buffer, p_size):
        raise NotImplementedError()

    # ~~~ SET_REPARSE_POINT ~~~

    @_catch_unhandled_exceptions
    def ll_set_reparse_point(self, file_context, file_name, buffer, size):
        """
        Set reparse point.
        """
        cooked_file_context = ffi.from_handle(file_context)
        cooked_file_name = ffi.string(file_name)
        # TODO: handle buffer and size here
        try:
            self.set_reparse_point(cooked_file_context, cooked_file_name, buffer, size)

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def set_reparse_point(self, file_context, file_name: str, buffer, size: int):
        raise NotImplementedError()

    # ~~~ DELETE_REPARSE_POINT ~~~

    @_catch_unhandled_exceptions
    def ll_delete_reparse_point(self, file_context, file_name, buffer, size):
        """
        Delete reparse point.
        """
        cooked_file_context = ffi.from_handle(file_context)
        cooked_file_name = ffi.string(file_name)
        # TODO: handle buffer and size here
        try:
            self.delete_reparse_point(cooked_file_context, cooked_file_name, buffer, size)

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def delete_reparse_point(self, file_context, file_name: str, buffer, size: int):
        raise NotImplementedError()

    # ~~~ GET_STREAM_INFO ~~~

    @_catch_unhandled_exceptions
    def ll_get_stream_info(self, file_context, buffer, length, p_bytes_transferred):
        """
        Get named streams information.
        Must set `volum_params.named_streams` to 1 for this method to be used.
        """
        cooked_file_context = ffi.from_handle(file_context, buffer, length, p_bytes_transferred)
        # TODO: handle p_bytes_transferred here
        try:
            self.get_stream_info(cooked_file_context, buffer, length, p_bytes_transferred)

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def get_stream_info(self, file_context, buffer, length: int, p_bytes_transferred):
        raise NotImplementedError()

    # ~~~ GET_DIR_INFO_BY_NAME ~~~

    @_catch_unhandled_exceptions
    def ll_get_dir_info_by_name(self, file_context, file_name, dir_info):
        """
        Must set `volum_params.pass_query_directory_file_name` to 1 for
        this method to be used. This is the default when an `get_dir_info_by_name`
        implementation is provided.
        """
        cooked_file_context = ffi.from_handle(file_context)
        cooked_file_name = ffi.string(file_name)
        try:
            info = self.get_dir_info_by_name(cooked_file_context, cooked_file_name)

        except NTStatusError as exc:
            return exc.value

        file_name_bytesize = lib.wcslen(file_name) * 2  # WCHAR
        ffi.memmove(dir_info.FileNameBuf, file_name, file_name_bytesize)

        configure_file_info(dir_info.FileInfo, **info)

        # dir_info is already allocated for us with a 255 wchar buffer for file
        # name, but we have to set the actual used size here
        dir_info.Size = ffi.sizeof("FSP_FSCTL_DIR_INFO") + file_name_bytesize

        return NTSTATUS.STATUS_SUCCESS

    def get_dir_info_by_name(self, file_context, file_name: str) -> dict:
        """
        Returned dict fields:
            creation_time
            last_access_time
            last_write_time
            change_time
            index_number
            file_attributes
            allocation_size
            file_size
        """
        raise NotImplementedError()

    # ~~~ CONTROL ~~~

    @_catch_unhandled_exceptions
    def ll_control(
        self,
        file_context,
        control_code,
        input_buffer,
        input_buffer_length,
        output_buffer,
        output_buffer_length,
        p_bytes_transferred,
    ):
        cooked_file_context = ffi.from_handle(file_context)
        try:
            # TODO handle input/output buffers and p_bytes_transferred here
            self.control(
                cooked_file_context,
                control_code,
                input_buffer,
                input_buffer_length,
                output_buffer,
                output_buffer_length,
                p_bytes_transferred,
            )

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def control(
        self,
        file_context,
        control_code,
        input_buffer,
        input_buffer_length,
        output_buffer,
        output_buffer_length,
        p_bytes_transferred,
    ):
        """
        Must set `volum_params.device_control` to 1 for this method to be used.
        """
        raise NotImplementedError()

    # ~~~ SET_DELETE ~~~

    @_catch_unhandled_exceptions
    def ll_set_delete(self, file_context, file_name, delete_file):
        cooked_file_context = ffi.from_handle(file_context)
        cooked_file_name = ffi.string(file_name)
        try:
            self.set_delete(cooked_file_context, cooked_file_name, delete_file)

        except NTStatusError as exc:
            return exc.value

        return NTSTATUS.STATUS_SUCCESS

    def set_delete(self, file_context, file_name: str, delete_file: bool):
        """
        If not overloaded, WinFSP fallbacks on `can_delete` and never call this
        method.
        """
        pass
