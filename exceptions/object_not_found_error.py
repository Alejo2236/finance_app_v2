class ObjectNotFoundError(Exception):
    """
    Exception raised when an expected object is not found in the database.

    :raises ObjectNotFoundError: When an object retrieval fails due to the object not being present.
    """
    pass
