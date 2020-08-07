from typing import NamedTuple, Any

from .status import NTSTATUS, cook_ntstatus
from .exceptions import NTStatusError

# Security descriptor conversion
# see https://docs.microsoft.com/en-us/windows/desktop/api/sddl/nf-sddl-convertstringsecuritydescriptortosecuritydescriptorw
from .bindings import lib, ffi


__all__ = ["SecurityDescriptor"]


class SecurityDescriptor(NamedTuple):

    handle: Any
    size: int

    @classmethod
    def from_cpointer(cls, handle):
        if handle == ffi.NULL:
            return cls(ffi.NULL, 0)
        size = lib.GetSecurityDescriptorLength(handle)
        pointer = lib.malloc(size)
        new_handle = ffi.cast("SECURITY_DESCRIPTOR*", pointer)
        ffi.memmove(new_handle, handle, size)
        return cls(new_handle, size)

    @classmethod
    def from_string(cls, string_format):
        # see https://docs.microsoft.com/fr-fr/windows/desktop/SecAuthZ/security-descriptor-string-format
        psd = ffi.new("SECURITY_DESCRIPTOR**")
        psd_size = ffi.new("ULONG*")
        if not lib.ConvertStringSecurityDescriptorToSecurityDescriptorW(
            string_format, lib.WFSPY_STRING_SECURITY_DESCRIPTOR_REVISION, psd, psd_size
        ):
            raise RuntimeError(
                f"Cannot create security descriptor `{string_format}`: "
                f"{cook_ntstatus(lib.GetLastError())}"
            )
        return cls(psd[0], psd_size[0])

    def evolve(self, security_information, modification_descriptor):
        psd = ffi.new("SECURITY_DESCRIPTOR**")
        status = lib.FspSetSecurityDescriptor(
            self.handle, security_information, modification_descriptor, psd
        )
        if status != NTSTATUS.STATUS_SUCCESS:
            raise NTStatusError(status)
        handle = psd[0]
        size = lib.GetSecurityDescriptorLength(handle)
        return type(self)(handle, size)

    def is_valid(self):
        return bool(lib.IsValidSecurityDescriptor(self.handle))

    def __del__(self):
        lib.LocalFree(self.handle)
