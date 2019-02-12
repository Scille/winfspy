import os
import re
import sys
from cffi import FFI


# see: https://docs.python.org/3/library/platform.html#platform.architecture
is_64bits = sys.maxsize > 2 ** 32


BASEDIR = os.path.dirname(os.path.abspath(__file__))

# import `get_winfsp_dir` the violent way given winfspy cannot be loaded yet
exec(open(f"{BASEDIR}/../winfspy/utils.py").read())
WINFSP_DIR = get_winfsp_dir()


def strip_by_shaif(src):
    kept_src = []
    skipping = 0
    for line_count, line in enumerate(src.split("\n")):
        requirement = re.match(r"^#if(.*)", line)
        if requirement:
            # TODO: find a way to get WinFSP version...
            if not eval(requirement.groups()[0], {}, {"WINFSP_VERSION": 0}):
                skipping += 1
            continue
        elif re.match(r"^#endif", line):
            skipping -= 1
            assert skipping >= 0, f"Error at line {line_count}: {line}"
            continue
        if not skipping:
            kept_src.append(line)
    assert skipping == 0, "#if and #endif not equally balanced"
    return "\n".join(kept_src)


ffibuilder = FFI()


ffibuilder.set_source(
    "winfspy._bindings",
    """
#include <windows.h>
#include <sddl.h>
#include <strsafe.h>
#include <winfsp/winfsp.h>


// InitializeSecurityDescriptor must be called with SECURITY_DESCRIPTOR_REVISION
// which is a #define (hence cannot be accessed directly by cffi)
DWORD getSecurityDescriptorRevision() {
    return SECURITY_DESCRIPTOR_REVISION;
}
DWORD getStringSecurityDescriptorRevision() {
    return SDDL_REVISION_1;
}

// Bitfields are not handled with CFFI, hence this big hack...
void configure_FSP_FSCTL_VOLUME_PARAMS(
    FSP_FSCTL_VOLUME_PARAMS *VolumeParams,
    UINT16 sector_size,
    UINT16 sectors_per_allocation_unit,
    UINT16 max_component_length,
    UINT64 volume_creation_time,
    UINT32 volume_serial_number,
    UINT32 transact_timeout,
    UINT32 irp_timeout,
    UINT32 irp_capacity,
    UINT32 file_info_timeout,
    UINT32 case_sensitive_search,
    UINT32 case_preserved_names,
    UINT32 unicode_on_disk,
    UINT32 persistent_acls,
    UINT32 reparse_points,
    UINT32 reparse_points_access_check,
    UINT32 named_streams,
    UINT32 hard_links,
    UINT32 extended_attributes,
    UINT32 read_only_volume,
    UINT32 post_cleanup_when_modified_only,
    UINT32 pass_query_directory_pattern,
    UINT32 always_use_double_buffering,
    UINT32 pass_query_directory_file_name,
    UINT32 flush_and_purge_on_cleanup,
    UINT32 device_control,
    UINT32 um_file_context_is_user_context2,
    UINT32 um_file_context_is_full_context,
    UINT32 um_reserved_flags,
    UINT32 km_reserved_flags,
    WCHAR *prefix,
    WCHAR *file_system_name,
    UINT32 volume_info_timeout_valid,
    UINT32 dir_info_timeout_valid,
    UINT32 security_timeout_valid,
    UINT32 stream_info_timeout_valid,
    UINT32 km_additional_reserved_flags,
    UINT32 volume_info_timeout,
    UINT32 dir_info_timeout,
    UINT32 security_timeout,
    UINT32 stream_info_timeout
) {
    VolumeParams->Version = sizeof(FSP_FSCTL_VOLUME_PARAMS);
    VolumeParams->SectorSize = sector_size;
    VolumeParams->SectorsPerAllocationUnit = sectors_per_allocation_unit;
    VolumeParams->MaxComponentLength = max_component_length;
    VolumeParams->VolumeCreationTime = volume_creation_time;
    VolumeParams->VolumeSerialNumber = volume_serial_number;
    VolumeParams->TransactTimeout = transact_timeout;
    VolumeParams->IrpTimeout = irp_timeout;
    VolumeParams->IrpCapacity = irp_capacity;
    VolumeParams->FileInfoTimeout = file_info_timeout;
    VolumeParams->CaseSensitiveSearch = case_sensitive_search;
    VolumeParams->CasePreservedNames = case_preserved_names;
    VolumeParams->UnicodeOnDisk = unicode_on_disk;
    VolumeParams->PersistentAcls = persistent_acls;
    VolumeParams->ReparsePoints = reparse_points;
    VolumeParams->ReparsePointsAccessCheck = reparse_points_access_check;
    VolumeParams->NamedStreams = named_streams;
    VolumeParams->HardLinks = hard_links;
    VolumeParams->ExtendedAttributes = extended_attributes;
    VolumeParams->ReadOnlyVolume = read_only_volume;
    VolumeParams->PostCleanupWhenModifiedOnly = post_cleanup_when_modified_only;
    VolumeParams->PassQueryDirectoryPattern = pass_query_directory_pattern;
    VolumeParams->AlwaysUseDoubleBuffering = always_use_double_buffering;
    VolumeParams->PassQueryDirectoryFileName = pass_query_directory_file_name;
    VolumeParams->FlushAndPurgeOnCleanup = flush_and_purge_on_cleanup;
    VolumeParams->DeviceControl = device_control;
    VolumeParams->UmFileContextIsUserContext2 = um_file_context_is_user_context2;
    VolumeParams->UmFileContextIsFullContext = um_file_context_is_full_context;
    VolumeParams->UmReservedFlags = um_reserved_flags;
    VolumeParams->KmReservedFlags = km_reserved_flags;

    StringCbCopyW(VolumeParams->Prefix, FSP_FSCTL_VOLUME_PREFIX_SIZE / sizeof(WCHAR), prefix);
    StringCbCopyW(VolumeParams->FileSystemName, FSP_FSCTL_VOLUME_FSNAME_SIZE / sizeof(WCHAR), file_system_name);

    VolumeParams->VolumeInfoTimeoutValid = volume_info_timeout_valid;
    VolumeParams->DirInfoTimeoutValid = dir_info_timeout_valid;
    VolumeParams->SecurityTimeoutValid = security_timeout_valid;
    VolumeParams->StreamInfoTimeoutValid = stream_info_timeout_valid;
    VolumeParams->KmAdditionalReservedFlags = km_additional_reserved_flags;
    VolumeParams->VolumeInfoTimeout = volume_info_timeout;
    VolumeParams->DirInfoTimeout = dir_info_timeout;
    VolumeParams->SecurityTimeout = security_timeout;
    VolumeParams->StreamInfoTimeout = stream_info_timeout;
}
    """,
    include_dirs=[f"{WINFSP_DIR}/inc"],
    libraries=["winfsp-" + ("x64" if is_64bits else "x86"), 'advapi32'],
    library_dirs=[f"{WINFSP_DIR}/lib"],
)


with open(BASEDIR + "/winfsp.cdef.h") as fd:
    ffibuilder.cdef(strip_by_shaif(fd.read()))

ffibuilder.cdef(
    """
// Trampolin functions to do the glue between WinFSP and Python

extern "Python" NTSTATUS _trampolin_OnStart(FSP_SERVICE * Service, ULONG argc, PWSTR * argv);
extern "Python" NTSTATUS _trampolin_OnStop(FSP_SERVICE * Service);
// TODO: better name for the params
extern "Python" NTSTATUS _trampolin_OnControl(FSP_SERVICE * Service, ULONG a, ULONG b, PVOID c);

extern "Python" NTSTATUS _trampolin_GetVolumeInfo(FSP_FILE_SYSTEM * FileSystem, FSP_FSCTL_VOLUME_INFO * VolumeInfo);
extern "Python" NTSTATUS _trampolin_SetVolumeLabel(FSP_FILE_SYSTEM * FileSystem, PWSTR VolumeLabel, FSP_FSCTL_VOLUME_INFO * VolumeInfo);
extern "Python" NTSTATUS _trampolin_GetSecurityByName(FSP_FILE_SYSTEM * FileSystem, PWSTR FileName, PUINT32 PFileAttributes /* or ReparsePointIndex */ , PSECURITY_DESCRIPTOR SecurityDescriptor, SIZE_T * PSecurityDescriptorSize);
extern "Python" NTSTATUS _trampolin_Create(FSP_FILE_SYSTEM * FileSystem, PWSTR FileName, UINT32 CreateOptions, UINT32 GrantedAccess, UINT32 FileAttributes, PSECURITY_DESCRIPTOR SecurityDescriptor, UINT64 AllocationSize, PVOID * PFileContext, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_Open(FSP_FILE_SYSTEM * FileSystem, PWSTR FileName, UINT32 CreateOptions, UINT32 GrantedAccess, PVOID * PFileContext, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_Overwrite(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, UINT32 FileAttributes, BOOLEAN ReplaceFileAttributes, UINT64 AllocationSize, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" VOID _trampolin_Cleanup(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, ULONG Flags);
extern "Python" VOID _trampolin_Close(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext);
extern "Python" NTSTATUS _trampolin_Read(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PVOID Buffer, UINT64 Offset, ULONG Length, PULONG PBytesTransferred);
extern "Python" NTSTATUS _trampolin_Write(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PVOID Buffer, UINT64 Offset, ULONG Length, BOOLEAN WriteToEndOfFile, BOOLEAN ConstrainedIo, PULONG PBytesTransferred, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_Flush(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_GetFileInfo(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_SetBasicInfo(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, UINT32 FileAttributes, UINT64 CreationTime, UINT64 LastAccessTime, UINT64 LastWriteTime, UINT64 ChangeTime, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_SetFileSize(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, UINT64 NewSize, BOOLEAN SetAllocationSize, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_CanDelete(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName);
extern "Python" NTSTATUS _trampolin_Rename(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, PWSTR NewFileName, BOOLEAN ReplaceIfExists);
extern "Python" NTSTATUS _trampolin_GetSecurity(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PSECURITY_DESCRIPTOR SecurityDescriptor, SIZE_T * PSecurityDescriptorSize);
extern "Python" NTSTATUS _trampolin_SetSecurity(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, SECURITY_INFORMATION SecurityInformation, PSECURITY_DESCRIPTOR ModificationDescriptor);
extern "Python" NTSTATUS _trampolin_ReadDirectory(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR Pattern, PWSTR Marker, PVOID Buffer, ULONG Length, PULONG PBytesTransferred);
extern "Python" NTSTATUS _trampolin_ResolveReparsePoints(FSP_FILE_SYSTEM * FileSystem, PWSTR FileName, UINT32 ReparsePointIndex, BOOLEAN ResolveLastPathComponent, PIO_STATUS_BLOCK PIoStatus, PVOID Buffer, PSIZE_T PSize);
extern "Python" NTSTATUS _trampolin_GetReparsePoint(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, PVOID Buffer, PSIZE_T PSize);
extern "Python" NTSTATUS _trampolin_SetReparsePoint(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, PVOID Buffer, SIZE_T Size);
extern "Python" NTSTATUS _trampolin_DeleteReparsePoint(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, PVOID Buffer, SIZE_T Size);
extern "Python" NTSTATUS _trampolin_GetStreamInfo(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PVOID Buffer, ULONG Length, PULONG PBytesTransferred);
extern "Python" NTSTATUS _trampolin_GetDirInfoByName(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, FSP_FSCTL_DIR_INFO * DirInfo);
extern "Python" NTSTATUS _trampolin_Control(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, UINT32 ControlCode, PVOID InputBuffer, ULONG InputBufferLength, PVOID OutputBuffer, ULONG OutputBufferLength, PULONG PBytesTransferred);
extern "Python" NTSTATUS _trampolin_SetDelete(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, BOOLEAN DeleteFile);

// Bitfields are not handled with CFFI, hence this big hack...
void configure_FSP_FSCTL_VOLUME_PARAMS(
    FSP_FSCTL_VOLUME_PARAMS * VolumeParams,
    UINT16 sector_size,
    UINT16 sectors_per_allocation_unit,
    UINT16 max_component_length,
    UINT64 volume_creation_time,
    UINT32 volume_serial_number,
    UINT32 transact_timeout,
    UINT32 irp_timeout,
    UINT32 irp_capacity,
    UINT32 file_info_timeout,
    UINT32 case_sensitive_search,
    UINT32 case_preserved_names,
    UINT32 unicode_on_disk,
    UINT32 persistent_acls,
    UINT32 reparse_points,
    UINT32 reparse_points_access_check,
    UINT32 named_streams,
    UINT32 hard_links,
    UINT32 extended_attributes,
    UINT32 read_only_volume,
    UINT32 post_cleanup_when_modified_only,
    UINT32 pass_query_directory_pattern,
    UINT32 always_use_double_buffering,
    UINT32 pass_query_directory_file_name,
    UINT32 flush_and_purge_on_cleanup,
    UINT32 device_control,
    UINT32 um_file_context_is_user_context2,
    UINT32 um_file_context_is_full_context,
    UINT32 um_reserved_flags,
    UINT32 km_reserved_flags,
    WCHAR * prefix,
    WCHAR * file_system_name,
    UINT32 volume_info_timeout_valid,
    UINT32 dir_info_timeout_valid,
    UINT32 security_timeout_valid,
    UINT32 stream_info_timeout_valid,
    UINT32 km_additional_reserved_flags,
    UINT32 volume_info_timeout,
    UINT32 dir_info_timeout,
    UINT32 security_timeout,
    UINT32 stream_info_timeout
);


// InitializeSecurityDescriptor must be called with SECURITY_DESCRIPTOR_REVISION
// which is a #define (hence cannot be accessed directly by cffi)
DWORD getSecurityDescriptorRevision();
DWORD getStringSecurityDescriptorRevision();

"""
)


if __name__ == "__main__":
    ffibuilder.compile()
