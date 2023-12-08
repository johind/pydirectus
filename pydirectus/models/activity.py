from typing import TypedDict


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
