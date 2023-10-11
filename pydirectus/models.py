from typing import TypedDict


class Folder(TypedDict):
    # Primary key of the folder.
    id: str
    # Name of the folder.
    name: str
    # Parent folder. Many-to-one to folders (recursive).
    parent: str | dict | None  # TODO gibt es none oder ist es dann string??


class Item(TypedDict):
    # Primary key of the item
    id: str


class File(TypedDict):
    # Primary key of the file
    id: str
    # Storage adapter used for the file.
    storage: str
    # Name of the file as saved on the storage adapter.
    filename_disk: str
    # Preferred filename when file is downloaded.
    filename_download: str
    # Title for the file.
    title: str
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
    tags: list[str] | None  # oder leeres dict ??
    # Any additional metadata Directus was able to scrape from the file. For images, this includes EXIF, IPTC, and ICC information.
    metadata: dict | None


class Activity(TypedDict):
    # Action that was performed.
    action: str
    # Collection identifier in which the item resides.
    collection: str
    # User comment. This will store the comments that show up in the right sidebar of the item edit page in the admin app.
    comment: str
    # Unique identifier for the object.
    id: int
    # The IP address of the user at the time the action took place.
    ip: str
    # Unique identifier for the item the action applied to. This is always a string, even for integer primary keys.
    item: str  # TODO kann wahrscheinlich auch ein dict sein wenn man nested moechte --> ueberpruefen
    # When the action happened.
    timestamp: str
    # The user who performed this action. Many-to-one to users.
    user: str
    # User agent string of the browser the user used when the action took place.
    user_agent: str
    # Any changes that were made in this activity. One-to-many to revisions.
    revisions: list  # TODO liste von strings oder objekten?
