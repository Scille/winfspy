/******************************************************
 *           Windows generic definitions              *
 ******************************************************/

typedef ULONG NTSTATUS;
typedef NTSTATUS* PNTSTATUS;


DWORD GetLastError(void);


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


typedef struct {
    ...;
} SRWLOCK;


typedef struct {
    ...;
} GENERIC_MAPPING;
typedef GENERIC_MAPPING* PGENERIC_MAPPING;


typedef struct {
    ...;
} SID;
typedef SID* PSID;


typedef struct {
    ...;
} CRITICAL_SECTION;


typedef struct {
    ...;
} FILETIME;
typedef FILETIME* PFILETIME;



HANDLE GetStdHandle(DWORD nStdHandle);
enum {
    STD_INPUT_HANDLE = -10,
    STD_OUTPUT_HANDLE = -11,
    STD_ERROR_HANDLE = -12
};


/*
 * Windows security descriptor API
 */


typedef struct
{
    // Security descriptor structure is not guarantee so better leave it this way
    // See https://docs.microsoft.com/en-us/windows/desktop/api/winnt/ns-winnt-_security_descriptor
    ...;
} SECURITY_DESCRIPTOR, *PSECURITY_DESCRIPTOR;


BOOL InitializeSecurityDescriptor(
  PSECURITY_DESCRIPTOR pSecurityDescriptor,
  DWORD                dwRevision
);


typedef WORD SECURITY_DESCRIPTOR_CONTROL, *PSECURITY_DESCRIPTOR_CONTROL;


BOOL GetSecurityDescriptorControl(
  PSECURITY_DESCRIPTOR         pSecurityDescriptor,
  PSECURITY_DESCRIPTOR_CONTROL pControl,
  LPDWORD                      lpdwRevision
);


// BOOL GetSecurityDescriptorDacl(
//   PSECURITY_DESCRIPTOR pSecurityDescriptor,
//   LPBOOL               lpbDaclPresent,
//   PACL                 *pDacl,
//   LPBOOL               lpbDaclDefaulted
// );


BOOL GetSecurityDescriptorGroup(
  PSECURITY_DESCRIPTOR pSecurityDescriptor,
  PSID                 *pGroup,
  LPBOOL               lpbGroupDefaulted
);


BOOL GetSecurityDescriptorOwner(
  PSECURITY_DESCRIPTOR pSecurityDescriptor,
  PSID                 *pOwner,
  LPBOOL               lpbOwnerDefaulted
);


DWORD GetSecurityDescriptorLength(
  PSECURITY_DESCRIPTOR pSecurityDescriptor
);


DWORD GetSecurityDescriptorRMControl(
  PSECURITY_DESCRIPTOR SecurityDescriptor,
  PUCHAR               RMControl
);


// BOOL GetSecurityDescriptorSacl(
//   PSECURITY_DESCRIPTOR pSecurityDescriptor,
//   LPBOOL               lpbSaclPresent,
//   PACL                 *pSacl,
//   LPBOOL               lpbSaclDefaulted
// );


BOOL IsValidSecurityDescriptor(
  PSECURITY_DESCRIPTOR pSecurityDescriptor
);


// BOOL SetSecurityDescriptorDacl(
//   PSECURITY_DESCRIPTOR pSecurityDescriptor,
//   BOOL                 bDaclPresent,
//   PACL                 pDacl,
//   BOOL                 bDaclDefaulted
// );


BOOL SetSecurityDescriptorGroup(
  PSECURITY_DESCRIPTOR pSecurityDescriptor,
  PSID                 pGroup,
  BOOL                 bGroupDefaulted
);


BOOL SetSecurityDescriptorOwner(
  PSECURITY_DESCRIPTOR pSecurityDescriptor,
  PSID                 pOwner,
  BOOL                 bOwnerDefaulted
);


DWORD SetSecurityDescriptorRMControl(
  PSECURITY_DESCRIPTOR SecurityDescriptor,
  PUCHAR               RMControl
);


// BOOL WINAPI SetSecurityDescriptorSacl(
//   PSECURITY_DESCRIPTOR pSecurityDescriptor,
//   BOOL                 bSaclPresent,
//   PACL                 pSacl,
//   BOOL                 bSaclDefaulted
// );


BOOL ConvertStringSecurityDescriptorToSecurityDescriptorW(
  LPCWSTR              StringSecurityDescriptor,
  DWORD                StringSDRevision,
  PSECURITY_DESCRIPTOR *SecurityDescriptor,
  PULONG               SecurityDescriptorSize
);


HLOCAL LocalFree(
  HLOCAL hMem
);


void* malloc(size_t);

/******************************************************
 *                WinFSP fsctl.h stuff                *
 ******************************************************/


typedef struct
{
    UINT64 TotalSize;
    UINT64 FreeSize;
    UINT16 VolumeLabelLength;
    WCHAR VolumeLabel[32];
} FSP_FSCTL_VOLUME_INFO;


typedef struct
{
    UINT32 FileAttributes;
    UINT32 ReparseTag;
    UINT64 AllocationSize;
    UINT64 FileSize;
    UINT64 CreationTime;
    UINT64 LastAccessTime;
    UINT64 LastWriteTime;
    UINT64 ChangeTime;
    UINT64 IndexNumber;
    UINT32 HardLinks;                   /* unimplemented: set to 0 */
} FSP_FSCTL_FILE_INFO;


typedef struct
{
    FSP_FSCTL_FILE_INFO FileInfo;
    PWSTR NormalizedName;
    UINT16 NormalizedNameSize;
} FSP_FSCTL_OPEN_FILE_INFO;


typedef struct
{
    UINT16 Size;
    FSP_FSCTL_FILE_INFO FileInfo;
    UINT8 Padding[24];
        /* make struct as big as FILE_ID_BOTH_DIR_INFORMATION; allows for in-place copying */
    WCHAR FileNameBuf[];
} FSP_FSCTL_DIR_INFO;


typedef struct {
    ...;
} FSP_FSCTL_TRANSACT_REQ;


typedef struct {
    ...;
} FSP_FSCTL_TRANSACT_RSP;


typedef struct {

    UINT16 Version;                     /* set to 0 or sizeof(FSP_FSCTL_VOLUME_PARAMS) */
    /* volume information */
    UINT16 SectorSize;
    UINT16 SectorsPerAllocationUnit;
    UINT16 MaxComponentLength;          /* maximum file name component length (bytes) */
    UINT64 VolumeCreationTime;
    UINT32 VolumeSerialNumber;
    /* I/O timeouts, capacity, etc. */
    UINT32 TransactTimeout;             /* FSP_FSCTL_TRANSACT timeout (millis; 1 sec - 10 sec) */
    UINT32 IrpTimeout;                  /* pending IRP timeout (millis; 1 min - 10 min) */
    UINT32 IrpCapacity;                 /* maximum number of pending IRP's (100 - 1000)*/
    UINT32 FileInfoTimeout;             /* FileInfo/Security/VolumeInfo timeout (millis) */

    // Bitfields not supported by cffi...

    // /* FILE_FS_ATTRIBUTE_INFORMATION::FileSystemAttributes */
    // UINT32 CaseSensitiveSearch:1;       /* file system supports case-sensitive file names */
    // UINT32 CasePreservedNames:1;        /* file system preserves the case of file names */
    // UINT32 UnicodeOnDisk:1;             /* file system supports Unicode in file names */
    // UINT32 PersistentAcls:1;            /* file system preserves and enforces access control lists */
    // UINT32 ReparsePoints:1;             /* file system supports reparse points */
    // UINT32 ReparsePointsAccessCheck:1;  /* file system performs reparse point access checks */
    // UINT32 NamedStreams:1;              /* file system supports named streams */
    // UINT32 HardLinks:1;                 /* unimplemented; set to 0 */
    // UINT32 ExtendedAttributes:1;        /* unimplemented; set to 0 */
    // UINT32 ReadOnlyVolume:1;
    // /* kernel-mode flags */
    // UINT32 PostCleanupWhenModifiedOnly:1;   /* post Cleanup when a file was modified/deleted */
    // UINT32 PassQueryDirectoryPattern:1;     /* pass Pattern during QueryDirectory operations */
    // UINT32 AlwaysUseDoubleBuffering:1;
    // UINT32 PassQueryDirectoryFileName:1;    /* pass FileName during QueryDirectory (GetDirInfoByName) */
    // UINT32 FlushAndPurgeOnCleanup:1;        /* keeps file off "standby" list */
    // UINT32 DeviceControl:1;                 /* support user-mode ioctl handling */
    // /* user-mode flags */
    // UINT32 UmFileContextIsUserContext2:1;   /* user mode: FileContext parameter is UserContext2 */
    // UINT32 UmFileContextIsFullContext:1;    /* user mode: FileContext parameter is FullContext */
    // UINT32 UmReservedFlags:6;
    // /* additional kernel-mode flags */\
    // UINT32 AllowOpenInKernelMode:1;         /* allow kernel mode to open files when possible */\
    // UINT32 CasePreservedExtendedAttributes:1;   /* preserve case of EA (default is UPPERCASE) */\
    // UINT32 WslFeatures:1;                   /* support features required for WSLinux */\
    // UINT32 DirectoryMarkerAsNextOffset:1;   /* directory marker is next offset instead of last name */\
    // UINT32 RejectIrpPriorToTransact0:1;     /* reject IRP's prior to FspFsctlTransact with 0 buffers */\
    // UINT32 KmReservedFlags:3;
    WCHAR Prefix[]; /* UNC prefix (ServerShare) */
    WCHAR FileSystemName[];

    // /* additional fields; specify .Version == sizeof(FSP_FSCTL_VOLUME_PARAMS) */
    // UINT32 VolumeInfoTimeoutValid:1;    /* VolumeInfoTimeout field is valid */
    // UINT32 DirInfoTimeoutValid:1;       /* DirInfoTimeout field is valid */
    // UINT32 SecurityTimeoutValid:1;      /* SecurityTimeout field is valid*/
    // UINT32 StreamInfoTimeoutValid:1;    /* StreamInfoTimeout field is valid */
    // UINT32 KmAdditionalReservedFlags:28;
    UINT32 VolumeInfoTimeout;           /* volume info timeout (millis); overrides FileInfoTimeout */
    UINT32 DirInfoTimeout;              /* dir info timeout (millis); overrides FileInfoTimeout */
    UINT32 SecurityTimeout;             /* security info timeout (millis); overrides FileInfoTimeout */
    UINT32 StreamInfoTimeout;           /* stream info timeout (millis); overrides FileInfoTimeout */

    ...;

} FSP_FSCTL_VOLUME_PARAMS;


typedef struct {
    ...;
} FSP_FSCTL_STREAM_INFO;


/******************************************************
 *                WinFSP winfsp.h stuff               *
 ******************************************************/
typedef struct _FSP_FILE_SYSTEM FSP_FILE_SYSTEM;
typedef NTSTATUS FSP_FILE_SYSTEM_OPERATION_GUARD(FSP_FILE_SYSTEM *,
    FSP_FSCTL_TRANSACT_REQ *, FSP_FSCTL_TRANSACT_RSP *);
typedef NTSTATUS FSP_FILE_SYSTEM_OPERATION(FSP_FILE_SYSTEM *,
    FSP_FSCTL_TRANSACT_REQ *, FSP_FSCTL_TRANSACT_RSP *);

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

typedef struct _FSP_FILE_SYSTEM_INTERFACE
{
    NTSTATUS (*GetVolumeInfo)(FSP_FILE_SYSTEM *FileSystem,
        FSP_FSCTL_VOLUME_INFO *VolumeInfo);
    NTSTATUS (*SetVolumeLabel)(FSP_FILE_SYSTEM *FileSystem,
        PWSTR VolumeLabel,
        FSP_FSCTL_VOLUME_INFO *VolumeInfo);
    NTSTATUS (*GetSecurityByName)(FSP_FILE_SYSTEM *FileSystem,
        PWSTR FileName, PUINT32 PFileAttributes/* or ReparsePointIndex */,
        PSECURITY_DESCRIPTOR SecurityDescriptor, SIZE_T *PSecurityDescriptorSize);
    NTSTATUS (*Create)(FSP_FILE_SYSTEM *FileSystem,
        PWSTR FileName, UINT32 CreateOptions, UINT32 GrantedAccess,
        UINT32 FileAttributes, PSECURITY_DESCRIPTOR SecurityDescriptor, UINT64 AllocationSize,
        PVOID *PFileContext, FSP_FSCTL_FILE_INFO *FileInfo);
    NTSTATUS (*Open)(FSP_FILE_SYSTEM *FileSystem,
        PWSTR FileName, UINT32 CreateOptions, UINT32 GrantedAccess,
        PVOID *PFileContext, FSP_FSCTL_FILE_INFO *FileInfo);
    NTSTATUS (*Overwrite)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, UINT32 FileAttributes, BOOLEAN ReplaceFileAttributes, UINT64 AllocationSize,
        FSP_FSCTL_FILE_INFO *FileInfo);
    VOID (*Cleanup)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, PWSTR FileName, ULONG Flags);
    VOID (*Close)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext);
    NTSTATUS (*Read)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, PVOID Buffer, UINT64 Offset, ULONG Length,
        PULONG PBytesTransferred);
    NTSTATUS (*Write)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, PVOID Buffer, UINT64 Offset, ULONG Length,
        BOOLEAN WriteToEndOfFile, BOOLEAN ConstrainedIo,
        PULONG PBytesTransferred, FSP_FSCTL_FILE_INFO *FileInfo);
    NTSTATUS (*Flush)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext,
        FSP_FSCTL_FILE_INFO *FileInfo);
    NTSTATUS (*GetFileInfo)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext,
        FSP_FSCTL_FILE_INFO *FileInfo);
    NTSTATUS (*SetBasicInfo)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, UINT32 FileAttributes,
        UINT64 CreationTime, UINT64 LastAccessTime, UINT64 LastWriteTime, UINT64 ChangeTime,
        FSP_FSCTL_FILE_INFO *FileInfo);
    NTSTATUS (*SetFileSize)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, UINT64 NewSize, BOOLEAN SetAllocationSize,
        FSP_FSCTL_FILE_INFO *FileInfo);
    NTSTATUS (*CanDelete)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, PWSTR FileName);
    NTSTATUS (*Rename)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext,
        PWSTR FileName, PWSTR NewFileName, BOOLEAN ReplaceIfExists);
    NTSTATUS (*GetSecurity)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext,
        PSECURITY_DESCRIPTOR SecurityDescriptor, SIZE_T *PSecurityDescriptorSize);
    NTSTATUS (*SetSecurity)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext,
        SECURITY_INFORMATION SecurityInformation, PSECURITY_DESCRIPTOR ModificationDescriptor);
    NTSTATUS (*ReadDirectory)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, PWSTR Pattern, PWSTR Marker,
        PVOID Buffer, ULONG Length, PULONG PBytesTransferred);
    NTSTATUS (*ResolveReparsePoints)(FSP_FILE_SYSTEM *FileSystem,
        PWSTR FileName, UINT32 ReparsePointIndex, BOOLEAN ResolveLastPathComponent,
        PIO_STATUS_BLOCK PIoStatus, PVOID Buffer, PSIZE_T PSize);
    NTSTATUS (*GetReparsePoint)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext,
        PWSTR FileName, PVOID Buffer, PSIZE_T PSize);
    NTSTATUS (*SetReparsePoint)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext,
        PWSTR FileName, PVOID Buffer, SIZE_T Size);
    NTSTATUS (*DeleteReparsePoint)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext,
        PWSTR FileName, PVOID Buffer, SIZE_T Size);
    NTSTATUS (*GetStreamInfo)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, PVOID Buffer, ULONG Length,
        PULONG PBytesTransferred);
    NTSTATUS (*GetDirInfoByName)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, PWSTR FileName,
        FSP_FSCTL_DIR_INFO *DirInfo);
#if WINFSP_VERSION >= 1.4
    NTSTATUS (*Control)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, UINT32 ControlCode,
        PVOID InputBuffer, ULONG InputBufferLength,
        PVOID OutputBuffer, ULONG OutputBufferLength, PULONG PBytesTransferred);
    NTSTATUS (*SetDelete)(FSP_FILE_SYSTEM *FileSystem,
        PVOID FileContext, PWSTR FileName, BOOLEAN DeleteFile);
#endif

    ...;

} FSP_FILE_SYSTEM_INTERFACE;

typedef struct _FSP_FILE_SYSTEM
{
    UINT16 Version;
    PVOID UserContext;
    WCHAR VolumeName[];
    HANDLE VolumeHandle;
    FSP_FILE_SYSTEM_OPERATION_GUARD *EnterOperation, *LeaveOperation;
    FSP_FILE_SYSTEM_OPERATION *Operations[];
    const FSP_FILE_SYSTEM_INTERFACE *Interface;
    HANDLE DispatcherThread;
    ULONG DispatcherThreadCount;
    NTSTATUS DispatcherResult;
    PWSTR MountPoint;
    HANDLE MountHandle;
    UINT32 DebugLog;
    FSP_FILE_SYSTEM_OPERATION_GUARD_STRATEGY OpGuardStrategy;
    SRWLOCK OpGuardLock;
    BOOLEAN UmFileContextIsUserContext2, UmFileContextIsFullContext;
} FSP_FILE_SYSTEM;

typedef struct _FSP_FILE_SYSTEM_OPERATION_CONTEXT
{
    FSP_FSCTL_TRANSACT_REQ *Request;
    FSP_FSCTL_TRANSACT_RSP *Response;
} FSP_FILE_SYSTEM_OPERATION_CONTEXT;

NTSTATUS FspFileSystemPreflight(PWSTR DevicePath,
    PWSTR MountPoint);

NTSTATUS FspFileSystemCreate(PWSTR DevicePath,
    const FSP_FSCTL_VOLUME_PARAMS *VolumeParams,
    const FSP_FILE_SYSTEM_INTERFACE *Interface,
    FSP_FILE_SYSTEM **PFileSystem);

VOID FspFileSystemDelete(FSP_FILE_SYSTEM *FileSystem);

NTSTATUS FspFileSystemSetMountPoint(FSP_FILE_SYSTEM *FileSystem, PWSTR MountPoint);
NTSTATUS FspFileSystemSetMountPointEx(FSP_FILE_SYSTEM *FileSystem, PWSTR MountPoint,
    PSECURITY_DESCRIPTOR SecurityDescriptor);

VOID FspFileSystemRemoveMountPoint(FSP_FILE_SYSTEM *FileSystem);

NTSTATUS FspFileSystemStartDispatcher(FSP_FILE_SYSTEM *FileSystem, ULONG ThreadCount);

VOID FspFileSystemStopDispatcher(FSP_FILE_SYSTEM *FileSystem);

VOID FspFileSystemSendResponse(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_RSP *Response);

FSP_FILE_SYSTEM_OPERATION_CONTEXT *FspFileSystemGetOperationContext(VOID);

PWSTR FspFileSystemMountPointF(FSP_FILE_SYSTEM *FileSystem);

NTSTATUS FspFileSystemEnterOperationF(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);

NTSTATUS FspFileSystemLeaveOperationF(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);

VOID FspFileSystemSetOperationGuardF(FSP_FILE_SYSTEM *FileSystem,
    FSP_FILE_SYSTEM_OPERATION_GUARD *EnterOperation,
    FSP_FILE_SYSTEM_OPERATION_GUARD *LeaveOperation);

VOID FspFileSystemSetOperationGuardStrategyF(FSP_FILE_SYSTEM *FileSystem,
    FSP_FILE_SYSTEM_OPERATION_GUARD_STRATEGY GuardStrategy);

VOID FspFileSystemSetOperationF(FSP_FILE_SYSTEM *FileSystem,
    ULONG Index,
    FSP_FILE_SYSTEM_OPERATION *Operation);

VOID FspFileSystemGetDispatcherResultF(FSP_FILE_SYSTEM *FileSystem,
    NTSTATUS *PDispatcherResult);

VOID FspFileSystemSetDispatcherResultF(FSP_FILE_SYSTEM *FileSystem,
    NTSTATUS DispatcherResult);

VOID FspFileSystemSetDebugLogF(FSP_FILE_SYSTEM *FileSystem,
    UINT32 DebugLog);

BOOLEAN FspFileSystemIsOperationCaseSensitiveF(VOID);

UINT32 FspFileSystemOperationProcessIdF(VOID);

/*
 * Operations
 */
NTSTATUS FspFileSystemOpEnter(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpLeave(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpCreate(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpOverwrite(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpCleanup(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpClose(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpRead(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpWrite(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpQueryInformation(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpSetInformation(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpFlushBuffers(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpQueryVolumeInformation(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpSetVolumeInformation(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpQueryDirectory(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpFileSystemControl(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
#if WINFSP_VERSION >= 1.4
NTSTATUS FspFileSystemOpDeviceControl(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
#endif
NTSTATUS FspFileSystemOpQuerySecurity(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpSetSecurity(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspFileSystemOpQueryStreamInformation(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request, FSP_FSCTL_TRANSACT_RSP *Response);

/*
 * Helpers
 */


BOOLEAN FspFileSystemAddDirInfo(FSP_FSCTL_DIR_INFO *DirInfo,
    PVOID Buffer, ULONG Length, PULONG PBytesTransferred);

BOOLEAN FspFileSystemFindReparsePoint(FSP_FILE_SYSTEM *FileSystem,
    NTSTATUS (*GetReparsePointByName)(
        FSP_FILE_SYSTEM *FileSystem, PVOID Context,
        PWSTR FileName, BOOLEAN IsDirectory, PVOID Buffer, PSIZE_T PSize),
    PVOID Context,
    PWSTR FileName, PUINT32 PReparsePointIndex);

NTSTATUS FspFileSystemResolveReparsePoints(FSP_FILE_SYSTEM *FileSystem,
    NTSTATUS (*GetReparsePointByName)(
        FSP_FILE_SYSTEM *FileSystem, PVOID Context,
        PWSTR FileName, BOOLEAN IsDirectory, PVOID Buffer, PSIZE_T PSize),
    PVOID Context,
    PWSTR FileName, UINT32 ReparsePointIndex, BOOLEAN ResolveLastPathComponent,
    PIO_STATUS_BLOCK PIoStatus, PVOID Buffer, PSIZE_T PSize);

NTSTATUS FspFileSystemCanReplaceReparsePoint(
    PVOID CurrentReparseData, SIZE_T CurrentReparseDataSize,
    PVOID ReplaceReparseData, SIZE_T ReplaceReparseDataSize);

BOOLEAN FspFileSystemAddStreamInfo(FSP_FSCTL_STREAM_INFO *StreamInfo,
    PVOID Buffer, ULONG Length, PULONG PBytesTransferred);


FSP_FSCTL_OPEN_FILE_INFO *FspFileSystemGetOpenFileInfo(FSP_FSCTL_FILE_INFO *FileInfo);

/*
 * Directory buffering
 */


BOOLEAN FspFileSystemAcquireDirectoryBuffer(PVOID *PDirBuffer,
    BOOLEAN Reset, PNTSTATUS PResult);

BOOLEAN FspFileSystemFillDirectoryBuffer(PVOID *PDirBuffer,
    FSP_FSCTL_DIR_INFO *DirInfo, PNTSTATUS PResult);

VOID FspFileSystemReleaseDirectoryBuffer(PVOID *PDirBuffer);

VOID FspFileSystemReadDirectoryBuffer(PVOID *PDirBuffer,
    PWSTR Marker,
    PVOID Buffer, ULONG Length, PULONG PBytesTransferred);

VOID FspFileSystemDeleteDirectoryBuffer(PVOID *PDirBuffer);

/*
 * Security
 */


PGENERIC_MAPPING FspGetFileGenericMapping(VOID);

NTSTATUS FspAccessCheckEx(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request,
    BOOLEAN CheckParentOrMain, BOOLEAN AllowTraverseCheck,
    UINT32 DesiredAccess, PUINT32 PGrantedAccess/* or ReparsePointIndex */,
    PSECURITY_DESCRIPTOR *PSecurityDescriptor);

NTSTATUS FspCreateSecurityDescriptor(FSP_FILE_SYSTEM *FileSystem,
    FSP_FSCTL_TRANSACT_REQ *Request,
    PSECURITY_DESCRIPTOR ParentDescriptor,
    PSECURITY_DESCRIPTOR *PSecurityDescriptor);

NTSTATUS FspSetSecurityDescriptor(
    PSECURITY_DESCRIPTOR InputDescriptor,
    SECURITY_INFORMATION SecurityInformation,
    PSECURITY_DESCRIPTOR ModificationDescriptor,
    PSECURITY_DESCRIPTOR *PSecurityDescriptor);

VOID FspDeleteSecurityDescriptor(PSECURITY_DESCRIPTOR SecurityDescriptor,
    NTSTATUS (*CreateFunc)());


/*
 * POSIX Interop
 */


NTSTATUS FspPosixMapUidToSid(UINT32 Uid, PSID *PSid);
NTSTATUS FspPosixMapSidToUid(PSID Sid, PUINT32 PUid);
VOID FspDeleteSid(PSID Sid, NTSTATUS (*CreateFunc)());
NTSTATUS FspPosixMapPermissionsToSecurityDescriptor(
    UINT32 Uid, UINT32 Gid, UINT32 Mode,
    PSECURITY_DESCRIPTOR *PSecurityDescriptor);
NTSTATUS FspPosixMapSecurityDescriptorToPermissions(
    PSECURITY_DESCRIPTOR SecurityDescriptor,
    PUINT32 PUid, PUINT32 PGid, PUINT32 PMode);
NTSTATUS FspPosixMapWindowsToPosixPathEx(PWSTR WindowsPath, char **PPosixPath,
    BOOLEAN Translate);
NTSTATUS FspPosixMapPosixToWindowsPathEx(const char *PosixPath, PWSTR *PWindowsPath,
    BOOLEAN Translate);
VOID FspPosixDeletePath(void *Path);
VOID FspPosixEncodeWindowsPath(PWSTR WindowsPath, ULONG Size);
VOID FspPosixDecodeWindowsPath(PWSTR WindowsPath, ULONG Size);


/*
 * Path Handling
 */


VOID FspPathPrefix(PWSTR Path, PWSTR *PPrefix, PWSTR *PRemain, PWSTR Root);
VOID FspPathSuffix(PWSTR Path, PWSTR *PRemain, PWSTR *PSuffix, PWSTR Root);
VOID FspPathCombine(PWSTR Prefix, PWSTR Suffix);

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
    ULONG AcceptControl;
    ULONG ExitCode;
    SERVICE_STATUS_HANDLE StatusHandle;
    SERVICE_STATUS ServiceStatus;
    CRITICAL_SECTION ServiceStatusGuard;
    CRITICAL_SECTION ServiceStopGuard;
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

//VOID FspServiceLogV(ULONG Type, PWSTR Format, va_list ap);


/*
 * Utility
 */


NTSTATUS FspNtStatusFromWin32(DWORD Error);
DWORD FspWin32FromNtStatus(NTSTATUS Status);
VOID FspEventLog(ULONG Type, PWSTR Format, ...);
//VOID FspEventLogV(ULONG Type, PWSTR Format, va_list ap);
VOID FspDebugLogSetHandle(HANDLE Handle);
VOID FspDebugLog(const char *Format, ...);
VOID FspDebugLogSD(const char *Format, PSECURITY_DESCRIPTOR SecurityDescriptor);
VOID FspDebugLogSid(const char *format, PSID Sid);
VOID FspDebugLogFT(const char *Format, PFILETIME FileTime);
VOID FspDebugLogRequest(FSP_FSCTL_TRANSACT_REQ *Request);
VOID FspDebugLogResponse(FSP_FSCTL_TRANSACT_RSP *Response);
NTSTATUS FspCallNamedPipeSecurely(PWSTR PipeName,
    PVOID InBuffer, ULONG InBufferSize, PVOID OutBuffer, ULONG OutBufferSize,
    PULONG PBytesTransferred, ULONG Timeout,
    PSID Sid);
NTSTATUS FspVersion(PUINT32 PVersion);
