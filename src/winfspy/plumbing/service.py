from contextlib import contextmanager
import threading

from .bindings import ffi, lib
from .winstuff import NTSTATUS


# TODO: finish this...


@ffi.def_extern()
def _trampolin_svc_OnStart(service, argc, argv):
    user_context = ffi.from_handle(service.UserContext)
    user_context.__fsp_service_ptr = service
    if user_context.__allow_console_mode:
        lib.FspServiceAllowConsoleMode(service)
    ret = user_context.on_start(argc, argv)
    user_context.__service_ready.set()
    return ret


@ffi.def_extern()
def _trampolin_svc_OnStop(service):
    user_context = ffi.from_handle(service.UserContext)
    return user_context.on_stop()


@ffi.def_extern()
def _trampolin_svc_OnControl(service, a, b, c):
    user_context = ffi.from_handle(service.UserContext)
    return user_context.on_control(a, b, c)


class BaseServiceUserContext:
    def on_start(self, argc, argv):
        return NTSTATUS.STATUS_SUCCESS
        # return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def on_stop(self):
        return NTSTATUS.STATUS_SUCCESS
        # return NTSTATUS.STATUS_NOT_IMPLEMENTED

    def on_control(self, a, b, c):
        return NTSTATUS.STATUS_SUCCESS
        # return NTSTATUS.STATUS_NOT_IMPLEMENTED


# def service_factory(user_context):
#     if not isinstance(user_context, BaseServiceUserContext):
#         raise ValueError(
#             f"`user_context` must be of type `{BaseServiceUserContext.__qualname__}`"
#         )

#     service = ffi.new("FSP_SERVICE*")
#     service.UserContext = ffi.new_handle(user_context)
#     service.OnStart = lib._trampolin_svc_OnStart
#     service.OnStop = lib._trampolin_svc_OnStop
#     service.OnControl = lib._trampolin_svc_OnControl
#     return service


@contextmanager
def run_service(service_name, user_context, allow_console_mode=False):
    if not isinstance(user_context, BaseServiceUserContext):
        raise ValueError(f"`user_context` must be of type `{BaseServiceUserContext.__qualname__}`")
    # TODO: find a way to retrieve the FSP_SERVICE* here to avoid this ugliness
    user_context.__allow_console_mode = allow_console_mode
    user_context.__service_ready = threading.Event()

    service_thread = threading.Thread(
        target=lib.FspServiceRunEx,
        args=(
            service_name,
            lib._trampolin_svc_OnStart,
            lib._trampolin_svc_OnStop,
            lib._trampolin_svc_OnControl,
            ffi.new_handle(user_context),
        ),
    )
    service_thread.start()
    user_context.__service_ready.wait()
    try:
        yield
    finally:
        if hasattr(user_context, "__fsp_service_ptr"):
            lib.FspServiceStop(user_context.__fsp_service_ptr)
        service_thread.join()
