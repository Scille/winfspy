class BaseFileSystemUserContext:
    def get_volume_info(self, VolumeInfo):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def set_volume_label(self, VolumeLabel, VolumeInfo):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def get_security_by_name(
        self,
        FileName,
        PFileAttributesOrReparsePointIndex,
        SecurityDescriptor,
        PSecurityDescriptorSize,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def create(
        self,
        FileName,
        CreateOptions,
        GrantedAccess,
        FileAttributes,
        SecurityDescriptor,
        AllocationSize,
        PFileContext,
        FileInfo,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def open(self, FileName, CreateOptions, GrantedAccess, PFileContext, FileInfo):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def overwrite(
        self,
        FileContext,
        FileAttributes,
        ReplaceFileAttributes,
        AllocationSize,
        FileInfo,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def cleanup(self, FileContext, FileName, Flags):
        pass

    def close(self, FileContext):
        pass

    def read(self, FileContext, Buffer, Offset, Length, PBytesTransferred):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def write(
        self,
        FileContext,
        Buffer,
        Offset,
        Length,
        WriteToEndOfFile,
        ConstrainedIo,
        PBytesTransferred,
        FileInfo,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def flush(self, FileContext, FileInfo):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def get_file_info(self, FileContext, FileInfo):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def set_basic_info(
        self,
        FileContext,
        FileAttributes,
        CreationTime,
        LastAccessTime,
        LastWriteTime,
        ChangeTime,
        FileInfo,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def set_file_size(self, FileContext, NewSize, SetAllocationSize, FileInfo):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def can_delete(self, FileContext, FileName):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def rename(self, FileContext, FileName, NewFileName, ReplaceIfExists):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def get_security(self, FileContext, SecurityDescriptor, PSecurityDescriptorSize):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def set_security(self, FileContext, SecurityInformation, ModificationDescriptor):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def read_directory(
        self, FileContext, Pattern, Marker, Buffer, Length, PBytesTransferred
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def resolve_reparse_points(
        self,
        FileName,
        ReparsePointIndex,
        ResolveLastPathComponent,
        PIoStatus,
        Buffer,
        PSize,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def get_reparse_point(self, FileContext, FileName, Buffer, PSize):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def set_reparse_point(self, FileContext, FileName, Buffer, Size):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def delete_reparse_point(self, FileContext, FileName, Buffer, Size):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def get_stream_info(self, FileContext, Buffer, Length, PBytesTransferred):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def get_dir_info_by_name(self, FileContext, FileName, DirInfo):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    # WINFSP VERSION >= 1.4
    def control(
        self,
        FileContext,
        ControlCode,
        InputBuffer,
        InputBufferLength,
        OutputBuffer,
        OutputBufferLength,
        PBytesTransferred,
    ):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED

    # WINFSP VERSION >= 1.4
    def set_delete(self, FileContext, FileName, DeleteFile):
        return NTSTATUS.STATUS_NOT_IMPLEMENTED
