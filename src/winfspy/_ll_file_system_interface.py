from .bindings import ffi, lib

from functools import wraps

def joe_la_pocav(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        print(f'POCAV=> {func.__name__}({args}, {kwargs})')
        return func(*args, **kwargs)
    return _wrapper

@ffi.def_extern()
@joe_la_pocav
def _trampolin_GetVolumeInfo(FileSystem, VolumeInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.get_volume_info(VolumeInfo)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_SetVolumeLabel(FileSystem, VolumeLabel, VolumeInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.set_volume_label(VolumeLabel, VolumeInfo)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_GetSecurityByName(
    FileSystem,
    FileName,
    PFileAttributesOrReparsePointIndex,
    SecurityDescriptor,
    PSecurityDescriptorSize,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.get_security_by_name(
        FileName,
        PFileAttributesOrReparsePointIndex,
        SecurityDescriptor,
        PSecurityDescriptorSize,
    )


@ffi.def_extern()
@joe_la_pocav
def _trampolin_Create(
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
    return user_context.create(
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
@joe_la_pocav
def _trampolin_Open(
    FileSystem, FileName, CreateOptions, GrantedAccess, PFileContext, FileInfo
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.open(
        FileName, CreateOptions, GrantedAccess, PFileContext, FileInfo
    )


@ffi.def_extern()
@joe_la_pocav
def _trampolin_Overwrite(
    FileSystem,
    FileContext,
    FileAttributes,
    ReplaceFileAttributes,
    AllocationSize,
    FileInfo,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.overwrite(
        FileContext, FileAttributes, ReplaceFileAttributes, AllocationSize, FileInfo
    )


@ffi.def_extern()
@joe_la_pocav
def _trampolin_Cleanup(FileSystem, FileContext, FileName, Flags):
    user_context = ffi.from_handle(FileSystem.UserContext)
    user_context.cleanup(FileContext, FileName, Flags)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_Close(FileSystem, FileContext):
    user_context = ffi.from_handle(FileSystem.UserContext)
    user_context.close(FileContext)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_Read(FileSystem, FileContext, Buffer, Offset, Length, PBytesTransferred):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.read(FileContext, Buffer, Offset, Length, PBytesTransferred)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_Write(
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
    return user_context.write(
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
@joe_la_pocav
def _trampolin_Flush(FileSystem, FileContext, FileInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.flush(FileContext, FileInfo)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_GetFileInfo(FileSystem, FileContext, FileInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.get_file_info(FileContext, FileInfo)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_SetBasicInfo(
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
    return user_context.set_basic_info(
        FileContext,
        FileAttributes,
        CreationTime,
        LastAccessTime,
        LastWriteTime,
        ChangeTime,
        FileInfo,
    )


@ffi.def_extern()
@joe_la_pocav
def _trampolin_SetFileSize(
    FileSystem, FileContext, NewSize, SetAllocationSize, FileInfo
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.set_file_size(FileContext, NewSize, SetAllocationSize, FileInfo)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_CanDelete(FileSystem, FileContext, FileName):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.can_delete(FileContext, FileName)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_Rename(FileSystem, FileContext, FileName, NewFileName, ReplaceIfExists):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.rename(FileContext, FileName, NewFileName, ReplaceIfExists)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_GetSecurity(
    FileSystem, FileContext, SecurityDescriptor, PSecurityDescriptorSize
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.get_security(
        FileContext, SecurityDescriptor, PSecurityDescriptorSize
    )


@ffi.def_extern()
@joe_la_pocav
def _trampolin_SetSecurity(
    FileSystem, FileContext, SecurityInformation, ModificationDescriptor
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.set_security(
        FileContext, SecurityInformation, ModificationDescriptor
    )


@ffi.def_extern()
@joe_la_pocav
def _trampolin_ReadDirectory(
    FileSystem, FileContext, Pattern, Marker, Buffer, Length, PBytesTransferred
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.read_directory(
        FileContext, Pattern, Marker, Buffer, Length, PBytesTransferred
    )


@ffi.def_extern()
@joe_la_pocav
def _trampolin_ResolveReparsePoints(
    FileSystem,
    FileName,
    ReparsePointIndex,
    ResolveLastPathComponent,
    PIoStatus,
    Buffer,
    PSize,
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.resolve_reparse_points(
        FileName, ReparsePointIndex, ResolveLastPathComponent, PIoStatus, Buffer, PSize
    )


@ffi.def_extern()
@joe_la_pocav
def _trampolin_GetReparsePoint(FileSystem, FileContext, FileName, Buffer, PSize):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.get_reparse_point(FileContext, FileName, Buffer, PSize)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_SetReparsePoint(FileSystem, FileContext, FileName, Buffer, Size):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.set_reparse_point(FileContext, FileName, Buffer, Size)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_DeleteReparsePoint(FileSystem, FileContext, FileName, Buffer, Size):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.delete_reparse_point(FileContext, FileName, Buffer, Size)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_GetStreamInfo(
    FileSystem, FileContext, Buffer, Length, PBytesTransferred
):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.get_stream_info(FileContext, Buffer, Length, PBytesTransferred)


@ffi.def_extern()
@joe_la_pocav
def _trampolin_GetDirInfoByName(FileSystem, FileContext, FileName, DirInfo):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.get_dir_info_by_name(FileContext, FileName, DirInfo)


# WINFSP VERSION >= 1.4
@ffi.def_extern()
@joe_la_pocav
def _trampolin_Control(
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
    return user_context.control(
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
@joe_la_pocav
def _trampolin_SetDelete(FileSystem, FileContext, FileName, DeleteFile):
    user_context = ffi.from_handle(FileSystem.UserContext)
    return user_context.set_delete(FileContext, FileName, DeleteFile)


def file_system_interface_factory():
    file_system_interface = ffi.new("FSP_FILE_SYSTEM_INTERFACE*")
    file_system_interface.GetVolumeInfo = lib._trampolin_GetVolumeInfo
    file_system_interface.SetVolumeLabel = lib._trampolin_SetVolumeLabel
    file_system_interface.GetSecurityByName = lib._trampolin_GetSecurityByName
    file_system_interface.Create = lib._trampolin_Create
    file_system_interface.Open = lib._trampolin_Open
    file_system_interface.Overwrite = lib._trampolin_Overwrite
    file_system_interface.Cleanup = lib._trampolin_Cleanup
    file_system_interface.Close = lib._trampolin_Close
    file_system_interface.Read = lib._trampolin_Read
    file_system_interface.Write = lib._trampolin_Write
    file_system_interface.Flush = lib._trampolin_Flush
    file_system_interface.GetFileInfo = lib._trampolin_GetFileInfo
    file_system_interface.SetBasicInfo = lib._trampolin_SetBasicInfo
    file_system_interface.SetFileSize = lib._trampolin_SetFileSize
    file_system_interface.CanDelete = lib._trampolin_CanDelete
    file_system_interface.Rename = lib._trampolin_Rename
    file_system_interface.GetSecurity = lib._trampolin_GetSecurity
    file_system_interface.SetSecurity = lib._trampolin_SetSecurity
    file_system_interface.ReadDirectory = lib._trampolin_ReadDirectory
    file_system_interface.ResolveReparsePoints = lib._trampolin_ResolveReparsePoints
    file_system_interface.GetReparsePoint = lib._trampolin_GetReparsePoint
    file_system_interface.SetReparsePoint = lib._trampolin_SetReparsePoint
    file_system_interface.DeleteReparsePoint = lib._trampolin_DeleteReparsePoint
    file_system_interface.GetStreamInfo = lib._trampolin_GetStreamInfo
    file_system_interface.GetDirInfoByName = lib._trampolin_GetDirInfoByName

    # requires  WINFSP VERSION >= 1.4
    try:
        file_system_interface.Control = lib._trampolin_Control
        file_system_interface.SetDelete = lib._trampolin_SetDelete
    except AttributeError:
        pass

    return file_system_interface
