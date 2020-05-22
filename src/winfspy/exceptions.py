from .plumbing.winstuff import NTSTATUS


class WinFSPyError(Exception):
    pass


class FileSystemAlreadyStarted(WinFSPyError):
    pass


class FileSystemNotStarted(WinFSPyError):
    pass


class NTStatusError(WinFSPyError):
    @property
    def value(self):
        return self.args[0]


class NTStatusObjectNameNotFound(NTStatusError):
    value = NTSTATUS.STATUS_OBJECT_NAME_NOT_FOUND


class NTStatusObjectNameCollision(NTStatusError):
    value = NTSTATUS.STATUS_OBJECT_NAME_COLLISION


class NTStatusAccessDenied(NTStatusError):
    value = NTSTATUS.STATUS_ACCESS_DENIED


class NTStatusNotADirectory(NTStatusError):
    value = NTSTATUS.STATUS_NOT_A_DIRECTORY


class NTStatusEndOfFile(NTStatusError):
    value = NTSTATUS.STATUS_END_OF_FILE


class NTStatusDirectoryNotEmpty(NTStatusError):
    value = NTSTATUS.STATUS_DIRECTORY_NOT_EMPTY


class NTStatusMediaWriteProtected(NTStatusError):
    value = NTSTATUS.STATUS_MEDIA_WRITE_PROTECTED
