class Operations:
    def can_delete(self, file_context, file_name):
        """
		Determine whether a file or directory can be deleted.
		"""
        raise NotImplementedError()

    def cleanup(self, file_context, file_name, flags):
        """
		Cleanup a file.
		"""
        raise NotImplementedError()

    def close(self, file_context):
        """
		Close a file.
		"""
        raise NotImplementedError()

    def create(self,):  # TODO
        """
		Create new file or directory.
		"""
        raise NotImplementedError()

    def delete_reparse_point(self, file_context, file_name, buffer, size):
        """
		Delete reparse point.
		"""
        raise NotImplementedError()

    def flush(self, file_context, file_info):
        """
		Flush a file or volume.
		"""
        raise NotImplementedError()

    def get_file_info(self, file_context, file_info):
        """
		Get file or directory information.
		"""
        raise NotImplementedError()

    def get_reparse_point(self, file_context, file_name, buffer, size):
        """
		Get reparse point.
		"""
        raise NotImplementedError()

    def get_security(self, file_context):
        """
		Get file or directory security descriptor.
		"""
        raise NotImplementedError()

    def get_security_by_name(self, file_context):
        """
		Get file or directory attributes and security descriptor given a file name.
		"""
        raise NotImplementedError()

    def get_stream_info(self, file_context):
        """
		Get named streams information.
		"""
        raise NotImplementedError()

    def get_volume_info(self, p_volume_info):
        """
		Get volume information.
		"""
        raise NotImplementedError()

    def open(self, file_context):
        """
		Open a file or directory.
		"""
        raise NotImplementedError()

    def overwrite(self, file_context):
        """
		Overwrite a file.
		"""
        raise NotImplementedError()

    def read(self, file_context):
        """
		Read a file.
		"""
        raise NotImplementedError()

    def read_directory(self, file_context):
        """
		Read a directory.
		"""
        raise NotImplementedError()

    def rename(self, file_context):
        """
		Renames a file or directory.
		"""
        raise NotImplementedError()

    def resolve_reparse_points(self, file_context):
        """
		Resolve reparse points.
		"""
        raise NotImplementedError()

    def set_basic_info(self, file_context):
        """
		Set file or directory basic information.
		"""
        raise NotImplementedError()

    def set_file_size(self, file_context):
        """
		Set file/allocation size.
		"""
        raise NotImplementedError()

    def set_reparse_point(self, file_context):
        """
		Set reparse point.
		"""
        raise NotImplementedError()

    def set_security(self, file_context):
        """
		Set file or directory security descriptor.
		"""
        raise NotImplementedError()

    def set_volume_label(self, file_context):
        """
		Set volume label.
		"""
        raise NotImplementedError()

    def write(self, file_context):
        """
		Write a file.
		"""
        raise NotImplementedError()
