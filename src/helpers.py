from src.schemas import FileCategory

CONTENT_TYPE_MAPPING = {
    FileCategory.IMAGE: [
        'image/png',
        'image/jpeg',
        'image/gif',
        'image/bmp',
        'image/webp',
        'image/tiff',
        'image/svg+xml'
    ],
    FileCategory.DOCUMENT: [
        'application/vnd.oasis.opendocument.text',
        'application/rtf',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'text/plain',
        'text/html',
        'text/csv'
    ],
    FileCategory.VIDEO: [
        'video/mp4',
        'video/mpeg',
        'video/x-msvideo',
        'video/quicktime',
        'video/x-ms-wmv',
        'video/webm'
    ],
    FileCategory.AUDIO: [
        'audio/mpeg',
        'audio/wav',
        'audio/aac',
        'audio/ogg',
        'audio/flac',
        'audio/x-ms-wma'
    ],
    FileCategory.ARCHIVE: [
        'application/zip',
        'application/x-rar-compressed',
        'application/x-tar',
        'application/gzip',
        'application/x-7z-compressed'
    ],
    FileCategory.MISC: [
        'application/octet-stream'
    ]
}

def get_category(content_type: str | None) -> FileCategory:
    if content_type == None:
        return FileCategory.MISC

    for category, content_types in CONTENT_TYPE_MAPPING.items():
        if content_type in content_types:
            return category

    return FileCategory.MISC
