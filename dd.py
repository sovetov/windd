import ctypes
from ctypes.wintypes import DWORD
import _winapi

_file_flags = DWORD(0xA0000000)  # FILE_FLAG_WRITE_THROUGH | FILE_FLAG_NO_BUFFERING
GENERIC_READ = DWORD(0x80000000)
GENERIC_WRITE = DWORD(0x40000000)
_generic_rw = DWORD(GENERIC_READ.value | GENERIC_WRITE.value)
NULL = DWORD(0)
OPEN_EXISTING = DWORD(3)
FILE_SHARE_WRITE = DWORD(2)

input_path = ctypes.create_unicode_buffer(u'D:\\Downloads\\linuxmint-19-cinnamon-64bit-v2.iso')
input_file = ctypes.windll.kernel32.CreateFileW(
    input_path,
    GENERIC_READ,
    DWORD(0),  # dwShareMode
    NULL,  # lpSecurityAttributes
    OPEN_EXISTING,  # dwCreationDisposition
    _file_flags,  # Not overlapped. # dwFlagsAndAttributes
    NULL,  # hTemplateFile
)
assert input_file > 0, (input_file, _winapi.GetLastError())

# output_path = ctypes.create_unicode_buffer(u'\\\\.\\f:')
output_path = ctypes.create_unicode_buffer(u'\\\\.\\PHYSICALDRIVE3')
output_file = ctypes.windll.kernel32.CreateFileW(
    output_path,
    _generic_rw,
    FILE_SHARE_WRITE,  # dwShareMode
    NULL,  # lpSecurityAttributes
    OPEN_EXISTING,  # dwCreationDisposition
    _file_flags,  # Not overlapped. # dwFlagsAndAttributes
    NULL,  # hTemplateFile
)
# assert output_file > 0, (output_file, _winapi.GetLastError())

buf_size = DWORD(1024 * 1024 * 16)
buf = ctypes.c_char_p(ctypes.windll.kernel32.HeapAlloc(
    ctypes.windll.kernel32.GetProcessHeap(),
    DWORD(0),  # Flags.
    buf_size,
))

while True:
    bytes_read = DWORD()
    assert ctypes.windll.kernel32.ReadFile(
        input_file,
        buf,
        buf_size,
        ctypes.byref(bytes_read),
        NULL,
    ), _winapi.GetLastError()
    print('read {}'.format(bytes_read.value))
    bytes_left = DWORD(bytes_read.value)
    bytes_written = DWORD()
    while bytes_left.value > 0:
        assert ctypes.windll.kernel32.WriteFile(
            output_file,
            buf,
            bytes_left,
            ctypes.byref(bytes_written),
            NULL,
        ), _winapi.GetLastError()
        bytes_left.value -= bytes_written.value
        print('written {}'.format(bytes_written.value))
    if bytes_read.value < buf_size.value:
        break
