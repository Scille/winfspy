from .bindings import ffi, lib
from .ntstatus import cook_ntstatus


def security_descriptor_factory(str_security_descriptor):
    psd = ffi.new('SECURITY_DESCRIPTOR**')
    psd_size = ffi.new("ULONG*")
    if not lib.ConvertStringSecurityDescriptorToSecurityDescriptorW(
        str_security_descriptor, lib.XXX_STRING_SECURITY_DESCRIPTOR_REVISION,
        psd, psd_size):
        print(':-(((((((((((((((((((((((')
        raise RuntimeError(f'error: {cook_ntstatus(lib.GetLastError())}')
    print('Created SD:', psd[0])
    assert lib.IsValidSecurityDescriptor(psd[0])
    return psd[0], psd_size[0]
