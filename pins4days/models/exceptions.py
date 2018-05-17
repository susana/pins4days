# -*- coding: utf-8 -*-


class EntityDoesNotExistException(Exception):
    """Should be thrown when an entity does not exist."""
    pass


class IncorrectPasswordException(Exception):
    """Should be thrown when an incorrect password is supplied."""
    pass
