/******************************************************
 *           Windows generic definitions              *
 ******************************************************/

typedef ULONG NTSTATUS;

typedef struct
{
    ...;
} SECURITY_DESCRIPTOR, *PSECURITY_DESCRIPTOR;

typedef struct {
    ...;
} SECURITY_INFORMATION;

typedef struct {
    ...;
} IO_STATUS_BLOCK, *PIO_STATUS_BLOCK;

typedef struct {
    ...;
} SERVICE_STATUS;
typedef HANDLE SERVICE_STATUS_HANDLE;


/******************************************************
 *                WinFSP fsctl.h stuff                *
 ******************************************************/


typedef struct {
    ...;
} FSP_FILE_SYSTEM;


typedef struct
{
    UINT64 TotalSize;
    UINT64 FreeSize;
    UINT16 VolumeLabelLength;
    WCHAR VolumeLabel[32];
} FSP_FSCTL_VOLUME_INFO;


typedef struct {
    ...;
} FSP_FSCTL_FILE_INFO;


typedef struct {
    ...;
} FSP_FSCTL_DIR_INFO;


/******************************************************
 *                WinFSP winfsp.h stuff               *
 ******************************************************/

/*
 * File system
 */

typedef enum
{
    FSP_FILE_SYSTEM_OPERATION_GUARD_STRATEGY_FINE = 0,
    FSP_FILE_SYSTEM_OPERATION_GUARD_STRATEGY_COARSE,
} FSP_FILE_SYSTEM_OPERATION_GUARD_STRATEGY;


enum
{
    FspCleanupDelete                    = 0x01,
    FspCleanupSetAllocationSize         = 0x02,
    FspCleanupSetArchiveBit             = 0x10,
    FspCleanupSetLastAccessTime         = 0x20,
    FspCleanupSetLastWriteTime          = 0x40,
    FspCleanupSetChangeTime             = 0x80,
};


typedef struct {

    NTSTATUS( * GetVolumeInfo)(FSP_FILE_SYSTEM * FileSystem,
      FSP_FSCTL_VOLUME_INFO * VolumeInfo);

    NTSTATUS( * SetVolumeLabel)(FSP_FILE_SYSTEM * FileSystem,
      PWSTR VolumeLabel,
      FSP_FSCTL_VOLUME_INFO * VolumeInfo);

    NTSTATUS( * GetSecurityByName)(FSP_FILE_SYSTEM * FileSystem,
      PWSTR FileName, PUINT32 PFileAttributes /* or ReparsePointIndex */ ,
      PSECURITY_DESCRIPTOR SecurityDescriptor, SIZE_T * PSecurityDescriptorSize);

    NTSTATUS( * Create)(FSP_FILE_SYSTEM * FileSystem,
      PWSTR FileName, UINT32 CreateOptions, UINT32 GrantedAccess,
      UINT32 FileAttributes, PSECURITY_DESCRIPTOR SecurityDescriptor, UINT64 AllocationSize,
      PVOID * PFileContext, FSP_FSCTL_FILE_INFO * FileInfo);

    NTSTATUS( * Open)(FSP_FILE_SYSTEM * FileSystem,
      PWSTR FileName, UINT32 CreateOptions, UINT32 GrantedAccess,
      PVOID * PFileContext, FSP_FSCTL_FILE_INFO * FileInfo);

    NTSTATUS( * Overwrite)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, UINT32 FileAttributes, BOOLEAN ReplaceFileAttributes, UINT64 AllocationSize,
      FSP_FSCTL_FILE_INFO * FileInfo);

    VOID( * Cleanup)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, PWSTR FileName, ULONG Flags);

    VOID( * Close)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext);

    NTSTATUS( * Read)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, PVOID Buffer, UINT64 Offset, ULONG Length,
      PULONG PBytesTransferred);

    NTSTATUS( * Write)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, PVOID Buffer, UINT64 Offset, ULONG Length,
      BOOLEAN WriteToEndOfFile, BOOLEAN ConstrainedIo,
      PULONG PBytesTransferred, FSP_FSCTL_FILE_INFO * FileInfo);

    NTSTATUS( * Flush)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext,
      FSP_FSCTL_FILE_INFO * FileInfo);

    NTSTATUS( * GetFileInfo)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext,
      FSP_FSCTL_FILE_INFO * FileInfo);

    NTSTATUS( * SetBasicInfo)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, UINT32 FileAttributes,
      UINT64 CreationTime, UINT64 LastAccessTime, UINT64 LastWriteTime, UINT64 ChangeTime,
      FSP_FSCTL_FILE_INFO * FileInfo);

    NTSTATUS( * SetFileSize)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, UINT64 NewSize, BOOLEAN SetAllocationSize,
      FSP_FSCTL_FILE_INFO * FileInfo);

    NTSTATUS( * CanDelete)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, PWSTR FileName);

    NTSTATUS( * Rename)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext,
      PWSTR FileName, PWSTR NewFileName, BOOLEAN ReplaceIfExists);

    NTSTATUS( * GetSecurity)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext,
      PSECURITY_DESCRIPTOR SecurityDescriptor, SIZE_T * PSecurityDescriptorSize);

    NTSTATUS( * SetSecurity)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext,
      SECURITY_INFORMATION SecurityInformation, PSECURITY_DESCRIPTOR ModificationDescriptor);

    NTSTATUS( * ReadDirectory)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, PWSTR Pattern, PWSTR Marker,
      PVOID Buffer, ULONG Length, PULONG PBytesTransferred);

    NTSTATUS( * ResolveReparsePoints)(FSP_FILE_SYSTEM * FileSystem,
      PWSTR FileName, UINT32 ReparsePointIndex, BOOLEAN ResolveLastPathComponent,
      PIO_STATUS_BLOCK PIoStatus, PVOID Buffer, PSIZE_T PSize);

    NTSTATUS( * GetReparsePoint)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext,
      PWSTR FileName, PVOID Buffer, PSIZE_T PSize);

    NTSTATUS( * SetReparsePoint)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext,
      PWSTR FileName, PVOID Buffer, SIZE_T Size);

    NTSTATUS( * DeleteReparsePoint)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext,
      PWSTR FileName, PVOID Buffer, SIZE_T Size);

    NTSTATUS( * GetStreamInfo)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, PVOID Buffer, ULONG Length,
      PULONG PBytesTransferred);

    NTSTATUS( * GetDirInfoByName)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, PWSTR FileName,
      FSP_FSCTL_DIR_INFO * DirInfo);

    NTSTATUS( * Control)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, UINT32 ControlCode,
      PVOID InputBuffer, ULONG InputBufferLength,
      PVOID OutputBuffer, ULONG OutputBufferLength, PULONG PBytesTransferred);

    NTSTATUS( * SetDelete)(FSP_FILE_SYSTEM * FileSystem,
      PVOID FileContext, PWSTR FileName, BOOLEAN DeleteFile);

    ...;

} FSP_FILE_SYSTEM_INTERFACE;


/*
 * Service Framework
 */


typedef struct _FSP_SERVICE FSP_SERVICE;
typedef NTSTATUS FSP_SERVICE_START(FSP_SERVICE *, ULONG, PWSTR *);
typedef NTSTATUS FSP_SERVICE_STOP(FSP_SERVICE *);
typedef NTSTATUS FSP_SERVICE_CONTROL(FSP_SERVICE *, ULONG, ULONG, PVOID);
typedef struct _FSP_SERVICE
{
    UINT16 Version;
    PVOID UserContext;
    FSP_SERVICE_START *OnStart;
    FSP_SERVICE_STOP *OnStop;
    FSP_SERVICE_CONTROL *OnControl;
    ...;
    ULONG AcceptControl;
    ULONG ExitCode;
    // SERVICE_STATUS_HANDLE StatusHandle;
    // SERVICE_STATUS ServiceStatus;
    // CRITICAL_SECTION ServiceStatusGuard;
    // CRITICAL_SECTION ServiceStopGuard;
    BOOLEAN AllowConsoleMode;
    WCHAR ServiceName[];
} FSP_SERVICE;


ULONG FspServiceRunEx(PWSTR ServiceName,
    FSP_SERVICE_START *OnStart,
    FSP_SERVICE_STOP *OnStop,
    FSP_SERVICE_CONTROL *OnControl,
    PVOID UserContext);
NTSTATUS FspServiceCreate(PWSTR ServiceName,
    FSP_SERVICE_START *OnStart,
    FSP_SERVICE_STOP *OnStop,
    FSP_SERVICE_CONTROL *OnControl,
    FSP_SERVICE **PService);
VOID FspServiceDelete(FSP_SERVICE *Service);
VOID FspServiceAllowConsoleMode(FSP_SERVICE *Service);
VOID FspServiceAcceptControl(FSP_SERVICE *Service, ULONG Control);
VOID FspServiceRequestTime(FSP_SERVICE *Service, ULONG Time);
VOID FspServiceSetExitCode(FSP_SERVICE *Service, ULONG ExitCode);
ULONG FspServiceGetExitCode(FSP_SERVICE *Service);
NTSTATUS FspServiceLoop(FSP_SERVICE *Service);
VOID FspServiceStop(FSP_SERVICE *Service);
BOOLEAN FspServiceIsInteractive(VOID);
NTSTATUS FspServiceContextCheck(HANDLE Token, PBOOLEAN PIsLocalSystem);
VOID FspServiceLog(ULONG Type, PWSTR Format, ...);
