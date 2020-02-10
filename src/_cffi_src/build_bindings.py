import os
import re
import sys
from cffi import FFI


# see: https://docs.python.org/3/library/platform.html#platform.architecture
is_64bits = sys.maxsize > 2 ** 32


BASEDIR = os.path.dirname(os.path.abspath(__file__))

# import `get_winfsp_dir` the violent way given winfspy cannot be loaded yet
get_winfsp_dir = None
exec(open(f"{BASEDIR}/../winfspy/plumbing/get_winfsp_dir.py").read())
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
    "winfspy.plumbing._bindings",
    """
#include <windows.h>
#include <string.h>
#include <sddl.h>
#include <strsafe.h>
#include <winfsp/winfsp.h>


// Expose #define as const to be available at runtime

const DWORD WFSPY_SECURITY_DESCRIPTOR_REVISION = SECURITY_DESCRIPTOR_REVISION;
const DWORD WFSPY_STRING_SECURITY_DESCRIPTOR_REVISION = SDDL_REVISION_1;

const PWSTR WFSPY_FSP_FSCTL_DRIVER_NAME = L"" FSP_FSCTL_DRIVER_NAME;
const PWSTR WFSPY_FSP_FSCTL_DISK_DEVICE_NAME = L"" FSP_FSCTL_DISK_DEVICE_NAME;
const PWSTR WFSPY_FSP_FSCTL_NET_DEVICE_NAME = L"" FSP_FSCTL_NET_DEVICE_NAME;
const PWSTR WFSPY_FSP_FSCTL_MUP_DEVICE_NAME = L"" FSP_FSCTL_MUP_DEVICE_NAME;

const int WFSPY_FILE_DIRECTORY_FILE = FILE_DIRECTORY_FILE;
const int WFSPY_FILE_NON_DIRECTORY_FILE = FILE_NON_DIRECTORY_FILE;
const int WFSPY_FILE_WRITE_THROUGH = FILE_WRITE_THROUGH;
const int WFSPY_FILE_SEQUENTIAL_ONLY = FILE_SEQUENTIAL_ONLY;
const int WFSPY_FILE_RANDOM_ACCESS = FILE_RANDOM_ACCESS;
const int WFSPY_FILE_NO_INTERMEDIATE_BUFFERING = FILE_NO_INTERMEDIATE_BUFFERING;
const int WFSPY_FILE_SYNCHRONOUS_IO_ALERT = FILE_SYNCHRONOUS_IO_ALERT;
const int WFSPY_FILE_SYNCHRONOUS_IO_NONALERT = FILE_SYNCHRONOUS_IO_NONALERT;
const int WFSPY_FILE_CREATE_TREE_CONNECTION = FILE_CREATE_TREE_CONNECTION;
const int WFSPY_FILE_NO_EA_KNOWLEDGE = FILE_NO_EA_KNOWLEDGE;
const int WFSPY_FILE_OPEN_REPARSE_POINT = FILE_OPEN_REPARSE_POINT;
const int WFSPY_FILE_DELETE_ON_CLOSE = FILE_DELETE_ON_CLOSE;
const int WFSPY_FILE_OPEN_BY_FILE_ID = FILE_OPEN_BY_FILE_ID;
const int WFSPY_FILE_OPEN_FOR_BACKUP_INTENT = FILE_OPEN_FOR_BACKUP_INTENT;
const int WFSPY_FILE_RESERVE_OPFILTER = FILE_RESERVE_OPFILTER;
const int WFSPY_FILE_OPEN_REQUIRING_OPLOCK = FILE_OPEN_REQUIRING_OPLOCK;
const int WFSPY_FILE_COMPLETE_IF_OPLOCKED = FILE_COMPLETE_IF_OPLOCKED;

const UINT32 WFSPY_FILE_ATTRIBUTE_INVALID_FILE_ATTRIBUTES = INVALID_FILE_ATTRIBUTES;


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
    UINT32 allow_open_in_kernel_mode,
    UINT32 case_preserved_extended_attributes,
    UINT32 wsl_features,
    UINT32 directory_marker_as_next_offset,
    UINT32 reject_irp_prior_to_transact0,
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

    VolumeParams->AllowOpenInKernelMode = allow_open_in_kernel_mode;
    VolumeParams->CasePreservedExtendedAttributes = case_preserved_extended_attributes;
    VolumeParams->WslFeatures = wsl_features;
    VolumeParams->DirectoryMarkerAsNextOffset = directory_marker_as_next_offset;
    VolumeParams->RejectIrpPriorToTransact0 = reject_irp_prior_to_transact0;
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
    libraries=["winfsp-" + ("x64" if is_64bits else "x86"), "advapi32"],
    library_dirs=[f"{WINFSP_DIR}/lib"],
)


with open(BASEDIR + "/winfsp.cdef.h") as fd:
    ffibuilder.cdef(strip_by_shaif(fd.read()))

ffibuilder.cdef(
    """
// Trampolin functions to do the glue between WinFSP and Python

extern "Python" NTSTATUS _trampolin_svc_OnStart(FSP_SERVICE * Service, ULONG argc, PWSTR * argv);
extern "Python" NTSTATUS _trampolin_svc_OnStop(FSP_SERVICE * Service);
// TODO: better name for the params
extern "Python" NTSTATUS _trampolin_svc_OnControl(FSP_SERVICE * Service, ULONG a, ULONG b, PVOID c);

extern "Python" NTSTATUS _trampolin_fs_GetVolumeInfo(FSP_FILE_SYSTEM * FileSystem, FSP_FSCTL_VOLUME_INFO * VolumeInfo);
extern "Python" NTSTATUS _trampolin_fs_SetVolumeLabel(FSP_FILE_SYSTEM * FileSystem, PWSTR VolumeLabel, FSP_FSCTL_VOLUME_INFO * VolumeInfo);
extern "Python" NTSTATUS _trampolin_fs_GetSecurityByName(FSP_FILE_SYSTEM * FileSystem, PWSTR FileName, PUINT32 PFileAttributes /* or ReparsePointIndex */ , PSECURITY_DESCRIPTOR SecurityDescriptor, SIZE_T * PSecurityDescriptorSize);
extern "Python" NTSTATUS _trampolin_fs_Create(FSP_FILE_SYSTEM * FileSystem, PWSTR FileName, UINT32 CreateOptions, UINT32 GrantedAccess, UINT32 FileAttributes, PSECURITY_DESCRIPTOR SecurityDescriptor, UINT64 AllocationSize, PVOID * PFileContext, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_fs_Open(FSP_FILE_SYSTEM * FileSystem, PWSTR FileName, UINT32 CreateOptions, UINT32 GrantedAccess, PVOID * PFileContext, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_fs_Overwrite(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, UINT32 FileAttributes, BOOLEAN ReplaceFileAttributes, UINT64 AllocationSize, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" VOID _trampolin_fs_Cleanup(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, ULONG Flags);
extern "Python" VOID _trampolin_fs_Close(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext);
extern "Python" NTSTATUS _trampolin_fs_Read(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PVOID Buffer, UINT64 Offset, ULONG Length, PULONG PBytesTransferred);
extern "Python" NTSTATUS _trampolin_fs_Write(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PVOID Buffer, UINT64 Offset, ULONG Length, BOOLEAN WriteToEndOfFile, BOOLEAN ConstrainedIo, PULONG PBytesTransferred, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_fs_Flush(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_fs_GetFileInfo(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_fs_SetBasicInfo(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, UINT32 FileAttributes, UINT64 CreationTime, UINT64 LastAccessTime, UINT64 LastWriteTime, UINT64 ChangeTime, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_fs_SetFileSize(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, UINT64 NewSize, BOOLEAN SetAllocationSize, FSP_FSCTL_FILE_INFO * FileInfo);
extern "Python" NTSTATUS _trampolin_fs_CanDelete(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName);
extern "Python" NTSTATUS _trampolin_fs_Rename(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, PWSTR NewFileName, BOOLEAN ReplaceIfExists);
extern "Python" NTSTATUS _trampolin_fs_GetSecurity(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PSECURITY_DESCRIPTOR SecurityDescriptor, SIZE_T * PSecurityDescriptorSize);
extern "Python" NTSTATUS _trampolin_fs_SetSecurity(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, SECURITY_INFORMATION SecurityInformation, PSECURITY_DESCRIPTOR ModificationDescriptor);
extern "Python" NTSTATUS _trampolin_fs_ReadDirectory(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR Pattern, PWSTR Marker, PVOID Buffer, ULONG Length, PULONG PBytesTransferred);
extern "Python" NTSTATUS _trampolin_fs_ResolveReparsePoints(FSP_FILE_SYSTEM * FileSystem, PWSTR FileName, UINT32 ReparsePointIndex, BOOLEAN ResolveLastPathComponent, PIO_STATUS_BLOCK PIoStatus, PVOID Buffer, PSIZE_T PSize);
extern "Python" NTSTATUS _trampolin_fs_GetReparsePoint(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, PVOID Buffer, PSIZE_T PSize);
extern "Python" NTSTATUS _trampolin_fs_SetReparsePoint(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, PVOID Buffer, SIZE_T Size);
extern "Python" NTSTATUS _trampolin_fs_DeleteReparsePoint(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, PVOID Buffer, SIZE_T Size);
extern "Python" NTSTATUS _trampolin_fs_GetStreamInfo(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PVOID Buffer, ULONG Length, PULONG PBytesTransferred);
extern "Python" NTSTATUS _trampolin_fs_GetDirInfoByName(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, FSP_FSCTL_DIR_INFO * DirInfo);
extern "Python" NTSTATUS _trampolin_fs_Control(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, UINT32 ControlCode, PVOID InputBuffer, ULONG InputBufferLength, PVOID OutputBuffer, ULONG OutputBufferLength, PULONG PBytesTransferred);
extern "Python" NTSTATUS _trampolin_fs_SetDelete(FSP_FILE_SYSTEM * FileSystem, PVOID FileContext, PWSTR FileName, BOOLEAN DeleteFile);

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
    UINT32 allow_open_in_kernel_mode,
    UINT32 case_preserved_extended_attributes,
    UINT32 wsl_features,
    UINT32 directory_marker_as_next_offset,
    UINT32 reject_irp_prior_to_transact0,
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


// Expose #define as const to be available at runtime

extern const DWORD WFSPY_SECURITY_DESCRIPTOR_REVISION;
extern const DWORD WFSPY_STRING_SECURITY_DESCRIPTOR_REVISION;

extern const PWSTR WFSPY_FSP_FSCTL_DRIVER_NAME;
extern const PWSTR WFSPY_FSP_FSCTL_DISK_DEVICE_NAME;
extern const PWSTR WFSPY_FSP_FSCTL_NET_DEVICE_NAME;
extern const PWSTR WFSPY_FSP_FSCTL_MUP_DEVICE_NAME;

extern const int WFSPY_FILE_DIRECTORY_FILE;
extern const int WFSPY_FILE_NON_DIRECTORY_FILE;
extern const int WFSPY_FILE_WRITE_THROUGH;
extern const int WFSPY_FILE_SEQUENTIAL_ONLY;
extern const int WFSPY_FILE_RANDOM_ACCESS;
extern const int WFSPY_FILE_NO_INTERMEDIATE_BUFFERING;
extern const int WFSPY_FILE_SYNCHRONOUS_IO_ALERT;
extern const int WFSPY_FILE_SYNCHRONOUS_IO_NONALERT;
extern const int WFSPY_FILE_CREATE_TREE_CONNECTION;
extern const int WFSPY_FILE_NO_EA_KNOWLEDGE;
extern const int WFSPY_FILE_OPEN_REPARSE_POINT;
extern const int WFSPY_FILE_DELETE_ON_CLOSE;
extern const int WFSPY_FILE_OPEN_BY_FILE_ID;
extern const int WFSPY_FILE_OPEN_FOR_BACKUP_INTENT;
extern const int WFSPY_FILE_RESERVE_OPFILTER;
extern const int WFSPY_FILE_OPEN_REQUIRING_OPLOCK;
extern const int WFSPY_FILE_COMPLETE_IF_OPLOCKED;

extern const int WFSPY_FILE_ATTRIBUTE_INVALID_FILE_ATTRIBUTES;

size_t wcslen(const wchar_t *str);
"""
)


if __name__ == "__main__":
    ffibuilder.compile()
