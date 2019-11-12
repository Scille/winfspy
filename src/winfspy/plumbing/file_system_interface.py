from .bindings import ffi, lib


@ffi.def_extern()
def _trampolin_fs_GetVolumeInfo(FileSystem, VolumeInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_get_volume_info(VolumeInfo)


@ffi.def_extern()
def _trampolin_fs_SetVolumeLabel(FileSystem, VolumeLabel, VolumeInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_set_volume_label(VolumeLabel, VolumeInfo)


@ffi.def_extern()
def _trampolin_fs_GetSecurityByName(
    FileSystem,
    FileName,
    PFileAttributesOrReparsePointIndex,
    SecurityDescriptor,
    PSecurityDescriptorSize,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_get_security_by_name(
        FileName, PFileAttributesOrReparsePointIndex, SecurityDescriptor, PSecurityDescriptorSize,
    )


@ffi.def_extern()
def _trampolin_fs_Create(
    FileSystem,
    FileName,
    CreateOptions,
    GrantedAccess,
    FileAttributes,
    SecurityDescriptor,
    AllocationSize,
    PFileContext,
    FileInfo,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_create(
        FileName,
        CreateOptions,
        GrantedAccess,
        FileAttributes,
        SecurityDescriptor,
        AllocationSize,
        PFileContext,
        FileInfo,
    )


@ffi.def_extern()
def _trampolin_fs_Open(FileSystem, FileName, CreateOptions, GrantedAccess, PFileContext, FileInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_open(FileName, CreateOptions, GrantedAccess, PFileContext, FileInfo)


@ffi.def_extern()
def _trampolin_fs_Overwrite(
    FileSystem, FileContext, FileAttributes, ReplaceFileAttributes, AllocationSize, FileInfo,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_overwrite(
        FileContext, FileAttributes, ReplaceFileAttributes, AllocationSize, FileInfo
    )


@ffi.def_extern()
def _trampolin_fs_Cleanup(FileSystem, FileContext, FileName, Flags):
    user_context = ffi.from_handle(FileSystem.UserContext)
    user_context.ll_cleanup(FileContext, FileName, Flags)


@ffi.def_extern()
def _trampolin_fs_Close(FileSystem, FileContext):
    user_context = ffi.from_handle(FileSystem.UserContext)
    user_context.ll_close(FileContext)


@ffi.def_extern()
def _trampolin_fs_Read(FileSystem, FileContext, Buffer, Offset, Length, PBytesTransferred):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_read(FileContext, Buffer, Offset, Length, PBytesTransferred)


@ffi.def_extern()
def _trampolin_fs_Write(
    FileSystem,
    FileContext,
    Buffer,
    Offset,
    Length,
    WriteToEndOfFile,
    ConstrainedIo,
    PBytesTransferred,
    FileInfo,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_write(
        FileContext,
        Buffer,
        Offset,
        Length,
        WriteToEndOfFile,
        ConstrainedIo,
        PBytesTransferred,
        FileInfo,
    )


@ffi.def_extern()
def _trampolin_fs_Flush(FileSystem, FileContext, FileInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_flush(FileContext, FileInfo)


@ffi.def_extern()
def _trampolin_fs_GetFileInfo(FileSystem, FileContext, FileInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_get_file_info(FileContext, FileInfo)


@ffi.def_extern()
def _trampolin_fs_SetBasicInfo(
    FileSystem,
    FileContext,
    FileAttributes,
    CreationTime,
    LastAccessTime,
    LastWriteTime,
    ChangeTime,
    FileInfo,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_set_basic_info(
        FileContext,
        FileAttributes,
        CreationTime,
        LastAccessTime,
        LastWriteTime,
        ChangeTime,
        FileInfo,
    )


@ffi.def_extern()
def _trampolin_fs_SetFileSize(FileSystem, FileContext, NewSize, SetAllocationSize, FileInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_set_file_size(FileContext, NewSize, SetAllocationSize, FileInfo)


@ffi.def_extern()
def _trampolin_fs_CanDelete(FileSystem, FileContext, FileName):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_can_delete(FileContext, FileName)


@ffi.def_extern()
def _trampolin_fs_Rename(FileSystem, FileContext, FileName, NewFileName, ReplaceIfExists):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_rename(FileContext, FileName, NewFileName, ReplaceIfExists)


@ffi.def_extern()
def _trampolin_fs_GetSecurity(FileSystem, FileContext, SecurityDescriptor, PSecurityDescriptorSize):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_get_security(FileContext, SecurityDescriptor, PSecurityDescriptorSize)


@ffi.def_extern()
def _trampolin_fs_SetSecurity(FileSystem, FileContext, SecurityInformation, ModificationDescriptor):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_set_security(FileContext, SecurityInformation, ModificationDescriptor)


@ffi.def_extern()
def _trampolin_fs_ReadDirectory(
    FileSystem, FileContext, Pattern, Marker, Buffer, Length, PBytesTransferred
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_read_directory(
        FileContext, Pattern, Marker, Buffer, Length, PBytesTransferred
    )


@ffi.def_extern()
def _trampolin_fs_ResolveReparsePoints(
    FileSystem, FileName, ReparsePointIndex, ResolveLastPathComponent, PIoStatus, Buffer, PSize,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_resolve_reparse_points(
        FileName, ReparsePointIndex, ResolveLastPathComponent, PIoStatus, Buffer, PSize
    )


@ffi.def_extern()
def _trampolin_fs_GetReparsePoint(FileSystem, FileContext, FileName, Buffer, PSize):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_get_reparse_point(FileContext, FileName, Buffer, PSize)


@ffi.def_extern()
def _trampolin_fs_SetReparsePoint(FileSystem, FileContext, FileName, Buffer, Size):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_set_reparse_point(FileContext, FileName, Buffer, Size)


@ffi.def_extern()
def _trampolin_fs_DeleteReparsePoint(FileSystem, FileContext, FileName, Buffer, Size):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_delete_reparse_point(FileContext, FileName, Buffer, Size)


@ffi.def_extern()
def _trampolin_fs_GetStreamInfo(FileSystem, FileContext, Buffer, Length, PBytesTransferred):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_get_stream_info(FileContext, Buffer, Length, PBytesTransferred)


@ffi.def_extern()
def _trampolin_fs_GetDirInfoByName(FileSystem, FileContext, FileName, DirInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_get_dir_info_by_name(FileContext, FileName, DirInfo)


# WINFSP VERSION >= 1.4
@ffi.def_extern()
def _trampolin_fs_Control(
    FileSystem,
    FileContext,
    ControlCode,
    InputBuffer,
    InputBufferLength,
    OutputBuffer,
    OutputBufferLength,
    PBytesTransferred,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_control(
        FileContext,
        ControlCode,
        InputBuffer,
        InputBufferLength,
        OutputBuffer,
        OutputBufferLength,
        PBytesTransferred,
    )


# WINFSP VERSION >= 1.4
@ffi.def_extern()
def _trampolin_fs_SetDelete(FileSystem, FileContext, FileName, DeleteFile):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.ll_set_delete(FileContext, FileName, DeleteFile)


def file_system_interface_trampoline_factory(set_delete_available: bool):
    file_system_interface = ffi.new("FSP_FILE_SYSTEM_INTERFACE*")
    file_system_interface.GetVolumeInfo = lib._trampolin_fs_GetVolumeInfo
    file_system_interface.SetVolumeLabel = lib._trampolin_fs_SetVolumeLabel
    file_system_interface.GetSecurityByName = lib._trampolin_fs_GetSecurityByName
    file_system_interface.Create = lib._trampolin_fs_Create
    file_system_interface.Open = lib._trampolin_fs_Open
    file_system_interface.Overwrite = lib._trampolin_fs_Overwrite
    file_system_interface.Cleanup = lib._trampolin_fs_Cleanup
    file_system_interface.Close = lib._trampolin_fs_Close
    file_system_interface.Read = lib._trampolin_fs_Read
    file_system_interface.Write = lib._trampolin_fs_Write
    file_system_interface.Flush = lib._trampolin_fs_Flush
    file_system_interface.GetFileInfo = lib._trampolin_fs_GetFileInfo
    file_system_interface.SetBasicInfo = lib._trampolin_fs_SetBasicInfo
    file_system_interface.SetFileSize = lib._trampolin_fs_SetFileSize
    file_system_interface.CanDelete = lib._trampolin_fs_CanDelete
    file_system_interface.Rename = lib._trampolin_fs_Rename
    file_system_interface.GetSecurity = lib._trampolin_fs_GetSecurity
    file_system_interface.SetSecurity = lib._trampolin_fs_SetSecurity
    file_system_interface.ReadDirectory = lib._trampolin_fs_ReadDirectory
    file_system_interface.ResolveReparsePoints = lib._trampolin_fs_ResolveReparsePoints
    file_system_interface.GetReparsePoint = lib._trampolin_fs_GetReparsePoint
    file_system_interface.SetReparsePoint = lib._trampolin_fs_SetReparsePoint
    file_system_interface.DeleteReparsePoint = lib._trampolin_fs_DeleteReparsePoint
    file_system_interface.GetStreamInfo = lib._trampolin_fs_GetStreamInfo
    file_system_interface.GetDirInfoByName = lib._trampolin_fs_GetDirInfoByName

    # requires  WINFSP VERSION >= 1.4
    try:
        file_system_interface.Control = lib._trampolin_fs_Control

        if set_delete_available:
            # If not available, WinFSP fallback to CanDelete
            file_system_interface.SetDelete = lib._trampolin_fs_SetDelete

    except AttributeError:
        pass

    return file_system_interface
