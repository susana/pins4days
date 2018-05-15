# -*- coding: utf-8 -*-


class EntityDoesNotExist(Exception):
    """Should be thrown when an entity does not exist."""
    pass


class IncorrectPassword(Exception):
    """Should be thrown when an incorrect password is supplied."""
    pass
