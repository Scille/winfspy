from .ntstatus import NTSTATUS, nt_success
from .filetime import filetime_now
from .bindings import ffi, lib


def start_fs(mountpoint, debug=False):
    # import pdb; pdb.set_trace()
    lib.FspServiceRunEx("passthrough", lib.SvcStart, lib.SvcStop, ffi.NULL, ffi.NULL)

    # result = PtfsCreate(PassThrough, VolumePrefix, mountpoint, debug, &Ptfs)
    # if not nt_success(result):
    #     raise RuntimeError(f"Cannot create file system: {result!r}")

    # result = FspFileSystemStartDispatcher(Ptfs->FileSystem, 0);
    # if not nt_success(result):
    #     raise RuntimeError(f"Cannot start file system: {result!r}")


def create_file_system(fs_name, volume_prefix=None):
    file_system = ffi.new("FSP_FILE_SYSTEM*")

    volume_params = ffi.new("FSP_FSCTL_VOLUME_PARAMS*")
    volume_params.SectorSize = ALLOCATION_UNIT
    volume_params.SectorsPerAllocationUnit = 1
    volume_params.VolumeCreationTime = filetime_now()
    volume_params.VolumeSerialNumber = 0
    volume_params.FileInfoTimeout = 1000
    volume_params.CaseSensitiveSearch = 0
    volume_params.CasePreservedNames = 1
    volume_params.UnicodeOnDisk = 1
    volume_params.PersistentAcls = 1
    volume_params.PostCleanupWhenModifiedOnly = 1
    volume_params.UmFileContextIsUserContext2 = 1
    if volume_prefix:
        volume_params.Prefix = volume_prefix

    volume_params.FileSystemName = fs_name

    return file_system


@ffi.def_extern()
def SvcStart(Service, argc, argv):
    return NTSTATUS.STATUS_NOT_IMPLEMENTED
    # # Create file system
    # # fs = create_fs()
    # file_system = create_file_system()

    # try:
    #     # Start dispatcher
    #     result = FspFileSystemStartDispatcher(file_system, 0);
    #     if not nt_success(result):
    #         raise RuntimeError(f"Cannot start file system: {result!r}")

    #     # Mount file system
    #     mountpoint = FspFileSystemMountPoint(file_system);

    # finally:
    #     pass
    #     # destroy_fs(fs)

    # return NTSTATUS.STATUS_SUCCESS


@ffi.def_extern()
def SvcStop(Service):
    return NTSTATUS.STATUS_NOT_IMPLEMENTED
