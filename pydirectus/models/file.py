# TODO total=False verwenden?
from typing import TypedDict

from .folder import Folder


class File(TypedDict):
    """
    TODO: Add parameter descriptions here (?)
    """

    # Primary key of the file
    id: str
    # Storage adapter used for the file.
    storage: str
    # Name of the file as saved on the storage adapter.
    filename_disk: str
    # Preferred filename when file is downloaded.
    filename_download: str
    # Title for the file.
    title: str | None
    # Mimetype of the file.
    type: str
    # What (virtual) folder the file is in. Many-to-one to folders.
    folder: str | Folder | None  # TODO str wenn id, dict weil wenn deep dann objekt vorhanden, ist None oder ist es nur str dann?
    # Who uploaded the file. Many-to-one to users.
    uploaded_by: str | dict | None
    # When the file was uploaded.
    uploaded_on: str
    # Who updated the file last. Many-to-one to users.
    modified_by: str | dict | None
    # Size of the file in bytes.
    filesize: int
    # If the file is a(n) image/video, it's the width in px.
    width: int | None
    # If the file is a(n) image/video, it's the height in px.
    height: int | None
    # If the file contains audio/video, it's the duration in milliseconds.
    duration: int | None
    # Description of the file.
    description: str | None
    # Location of the file.
    location: str | None
    # Tags for the file.
    tags: list[str] | None  # TODO or empty dict ?
    # Any additional metadata Directus was able to scrape from the file. For images, this includes EXIF, IPTC, and ICC information.
    metadata: dict | None
