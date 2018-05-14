# -*- coding: utf-8 -*-

from models import User
from flask_login.mixins import UserMixin


class AppUser(UserMixin):

    """Represents a Pins4Days user in Flask.

    Attributes:
        user_model (pins4days.models.User): The Pins4Days User model.
        username (str): The user's username.
    """

    def __init__(self, user):
        """Creates a Flask user.

        Args:
            user (pins4days.models.User): The Pins4Days User model.
        """
        self.user_model = user
        self.username = user.key.id()

    def get_id(self):
        """Gets the user's ID.

        Returns:
            str: The pins4days.models.User ID which is the user's username.
        """
        return self.user_model.key.id()
