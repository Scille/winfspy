from .ntstatus import NTSTATUS

def joe_la_pocav(func):
    from functools import wraps
    @wraps(func)
    def _wrapper(*args, **kwargs):
        print(f"****** BASECALL => {func.__name__}({args}, {kwargs})")
        return func(*args, **kwargs)

    return _wrapper

class BaseFileSystemUserContext:
    @joe_la_pocav
    def get_volume_info(self, volume_info):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def set_volume_label(self, volume_label, volume_info):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def get_security_by_name(
        self,
        file_name,
        p_file_attributes_or_reparse_point_index,
        security_descriptor,
        p_security_descriptor_size,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def create(
        self,
        file_name,
        create_options,
        granted_access,
        file_attributes,
        security_descriptor,
        allocation_size,
        p_file_context,
        file_info,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def open(
        self, file_name, create_options, granted_access, p_file_context, file_info
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def overwrite(
        self,
        file_context,
        file_attributes,
        replace_file_attributes,
        allocation_size,
        file_info,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def cleanup(self, file_context, file_name, flags):
        pass

    @joe_la_pocav
    def close(self, file_context):
        pass

    @joe_la_pocav
    def read(self, file_context, buffer, offset, length, p_bytes_transferred):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def write(
        self,
        file_context,
        buffer,
        offset,
        length,
        write_to_end_of_file,
        constrained_io,
        p_bytes_transferred,
        file_info,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def flush(self, file_context, file_info):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def get_file_info(self, file_context, file_info):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def set_basic_info(
        self,
        file_context,
        file_attributes,
        creation_time,
        last_access_time,
        last_write_time,
        change_time,
        file_info,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def set_file_size(self, file_context, new_size, set_allocation_size, file_info):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def can_delete(self, file_context, file_name):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def rename(self, file_context, file_name, new_file_name, replace_if_exists):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def get_security(
        self, file_context, security_descriptor, p_security_descriptor_size
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def set_security(self, file_context, security_information, modification_descriptor):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def read_directory(
        self, file_context, pattern, marker, buffer, length, p_bytes_transferred
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def resolve_reparse_points(
        self,
        file_name,
        reparse_point_index,
        resolve_last_path_component,
        p_io_status,
        buffer,
        p_size,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def get_reparse_point(self, file_context, file_name, buffer, p_size):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def set_reparse_point(self, file_context, file_name, buffer, size):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def delete_reparse_point(self, file_context, file_name, buffer, size):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def get_stream_info(self, file_context, buffer, length, p_bytes_transferred):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    @joe_la_pocav
    def get_dir_info_by_name(self, file_context, file_name, dir_info):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    # winfsp version >= 1.4
    @joe_la_pocav
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
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    # winfsp version >= 1.4
    @joe_la_pocav
    def set_delete(self, file_context, file_name, delete_file):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED
