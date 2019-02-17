from .plumbing.winstuff import NTSTATUS


class WinFSPyError(Exception):
    pass


class FileSystemAlreadyStarted(WinFSPyError):
    pass


class FileSystemNotStarted(WinFSPyError):
    pass


class NTStatus(WinFSPyError):
    @property
    def value(self):
        return self.args[0]


class NTStatusObjectNameNotFound(NTStatus):
    value = NTSTATUS.STATUS_OBJECT_NAME_NOT_FOUND


class NTStatusObjectNameCollision(NTStatus):
    value = NTSTATUS.STATUS_OBJECT_NAME_COLLISION


class NTStatusAccessDenied(NTStatus):
    value = NTSTATUS.STATUS_ACCESS_DENIED


class NTStatusNotADirectory(NTStatus):
    value = NTSTATUS.STATUS_NOT_A_DIRECTORY


class NTStatusEndOfFile(NTStatus):
    value = NTSTATUS.STATUS_END_OF_FILE


class NTStatusDirectoryNotEmpty(NTStatus):
    value = NTSTATUS.STATUS_DIRECTORY_NOT_EMPTY
