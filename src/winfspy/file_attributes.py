import enum


class FILE_ATTRIBUTE(enum.IntEnum):

    FILE_ATTRIBUTE_ARCHIVE = 0x20
    """
    A file or directory that is an archive file or directory.
    Applications typically use this attribute to mark files for backup or removal.
    """

    FILE_ATTRIBUTE_COMPRESSED = 0x800
    """
    A file or directory that is compressed. For a file, all of the data in the
    file is compressed. For a directory, compression is the default for newly
    created files and subdirectories.
    """

    FILE_ATTRIBUTE_DEVICE = 0x40
    """
    This value is reserved for system use.
    """

    FILE_ATTRIBUTE_DIRECTORY = 0x10
    """
    The handle that identifies a directory.
    """

    FILE_ATTRIBUTE_ENCRYPTED = 0x4000
    """
    A file or directory that is encrypted. For a file, all data streams in the
    file are encrypted. For a directory, encryption is the default for newly
    created files and subdirectories.
    """

    FILE_ATTRIBUTE_HIDDEN = 0x2
    """
    The file or directory is hidden. It is not included in an ordinary
    directory listing.
    """

    FILE_ATTRIBUTE_INTEGRITY_STREAM = 0x8000
    """
    The directory or user data stream is configured with integrity (only
    supported on ReFS volumes). It is not included in an ordinary directory
    listing. The integrity setting persists with the file if it's renamed.
    If a file is copied the destination file will have integrity set if either
    the source file or destination directory have integrity set.

    Windows Server 2008 R2, Windows 7, Windows Server 2008, Windows Vista,
    Windows Server 2003 and Windows XP: This flag is not supported until
    Windows Server 2012.
    """

    FILE_ATTRIBUTE_NORMAL = 0x80
    """
    A file that does not have other attributes set.
    This attribute is valid only when used alone.
    """

    FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 0x2000
    """
    The file or directory is not to be indexed by the content indexing service.
    """

    FILE_ATTRIBUTE_NO_SCRUB_DATA = 0x20000
    """
    The user data stream not to be read by the background data integrity
    scanner (AKA scrubber). When set on a directory it only provides
    inheritance. This flag is only supported on Storage Spaces and ReFS
    volumes. It is not included in an ordinary directory listing.

    Windows Server 2008 R2, Windows 7, Windows Server 2008, Windows Vista,
    Windows Server 2003 and Windows XP: This flag is not supported until
    Windows 8 and Windows Server 2012.
    """

    FILE_ATTRIBUTE_OFFLINE = 0x1000
    """
    The data of a file is not available immediately. This attribute indicates
    that the file data is physically moved to offline storage. This attribute
    is used by Remote Storage, which is the hierarchical storage management
    software.
    Applications should not arbitrarily change this attribute.
    """

    FILE_ATTRIBUTE_READONLY = 0x1
    """
    A file that is read-only. Applications can read the file, but cannot
    write to it or delete it. This attribute is not honored on directories.
    For more information, see You cannot view or change the Read-only or the
    System attributes of folders in Windows Server 2003, in Windows XP,
    in Windows Vista or in Windows 7.
    """

    FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x400000
    """
    When this attribute is set, it means that the file or directory is not
    fully present locally. For a file that means that not all of its data is
    on local storage (e.g. it may be sparse with some data still in remote
    storage). For a directory it means that some of the directory contents are
    being virtualized from another location. Reading the file / enumerating the
    directory will be more expensive than normal, e.g. it will cause at least
    some of the file/directory content to be fetched from a remote store.
    Only kernel-mode callers can set this bit.
    """

    FILE_ATTRIBUTE_RECALL_ON_OPEN = 0x40000
    """
    This attribute only appears in directory enumeration classes
    (FILE_DIRECTORY_INFORMATION, FILE_BOTH_DIR_INFORMATION, etc.). When this
    attribute is set, it means that the file or directory has no physical
    representation on the local system; the item is virtual.
    Opening the item will be more expensive than normal, e.g. it will cause
    at least some of it to be fetched from a remote store.
    """

    FILE_ATTRIBUTE_REPARSE_POINT = 0x400
    """
    A file or directory that has an associated reparse point, or a file
    that is a symbolic link.
    """

    FILE_ATTRIBUTE_SPARSE_FILE = 0x200
    """
    A file that is a sparse file.
    """

    FILE_ATTRIBUTE_SYSTEM = 0x4
    """
    A file or directory that the operating system uses a part of,
    or uses exclusively.
    """

    FILE_ATTRIBUTE_TEMPORARY = 0x100
    """
    A file that is being used for temporary storage.
    File systems avoid writing data back to mass storage if sufficient cache
    memory is available, because typically, an application deletes a temporary
    file after the handle is closed. In that scenario, the system can entirely
    avoid writing the data. Otherwise, the data is written after the handle
    is closed.
    """

    FILE_ATTRIBUTE_VIRTUAL = 0x10000
    """
    This value is reserved for system use.
    """
