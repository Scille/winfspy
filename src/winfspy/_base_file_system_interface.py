from .ntstatus import NTSTATUS


class BaseFileSystemUserContext:
    def get_volume_info(self, volume_info):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def set_volume_label(self, volume_label, volume_info):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def get_security_by_name(
        self,
        file_name,
        p_file_attributes_or_reparse_point_index,
        security_descriptor,
        p_security_descriptor_size,
    ):
        return ntstatus.STATUS_NOT_IMPLEMENTED

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
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def open(
        self, file_name, create_options, granted_access, p_file_context, file_info
    ):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def overwrite(
        self,
        file_context,
        file_attributes,
        replace_file_attributes,
        allocation_size,
        file_info,
    ):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def cleanup(self, file_context, file_name, flags):
        pass

    def close(self, file_context):
        pass

    def read(self, file_context, buffer, offset, length, p_bytes_transferred):
        return ntstatus.STATUS_NOT_IMPLEMENTED

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
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def flush(self, file_context, file_info):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def get_file_info(self, file_context, file_info):
        return ntstatus.STATUS_NOT_IMPLEMENTED

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
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def set_file_size(self, file_context, new_size, set_allocation_size, file_info):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def can_delete(self, file_context, file_name):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def rename(self, file_context, file_name, new_file_name, replace_if_exists):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def get_security(
        self, file_context, security_descriptor, p_security_descriptor_size
    ):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def set_security(self, file_context, security_information, modification_descriptor):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def read_directory(
        self, file_context, pattern, marker, buffer, length, p_bytes_transferred
    ):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def resolve_reparse_points(
        self,
        file_name,
        reparse_point_index,
        resolve_last_path_component,
        p_io_status,
        buffer,
        p_size,
    ):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def get_reparse_point(self, file_context, file_name, buffer, p_size):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def set_reparse_point(self, file_context, file_name, buffer, size):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def delete_reparse_point(self, file_context, file_name, buffer, size):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def get_stream_info(self, file_context, buffer, length, p_bytes_transferred):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    def get_dir_info_by_name(self, file_context, file_name, dir_info):
        return ntstatus.STATUS_NOT_IMPLEMENTED

    # winfsp version >= 1.4
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
        return ntstatus.STATUS_NOT_IMPLEMENTED

    # winfsp version >= 1.4
    def set_delete(self, file_context, file_name, delete_file):
        return ntstatus.STATUS_NOT_IMPLEMENTED
