# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from lib.pybcrypt import bcrypt

from exceptions import IncorrectPasswordException
from exceptions import EntityDoesNotExistException


class User(ndb.Model):

    """Represents a Pins4Days app user.

    Attributes:
        password (StringProperty): The user's password. ENCRYPT BEFORE STORING!
        See User.encrypt_password() and User.create_with_encryption().
    """

    # The User entity's key.id is set to the username to maintain unique
    # constraint.
    password = ndb.StringProperty('pw', required=True)

    @staticmethod
    def compare_passwords(stored_pw, unencrypted_pw):
        """Compares a stored password with an unencrypted password to see if
        they match.

        Args:
            stored_pw (str): The password that is currently stored in the DB.
            unencrypted_pw (str): An unencrypted password to compare to the
            stored password.

        Returns:
            bool: Returns True if the passwords match. False, otherwise.
        """
        return bcrypt.hashpw(unencrypted_pw, stored_pw) == stored_pw

    @staticmethod
    def encrypt_password(password):
        """Encrypts (bcrypt) a given password.

        Args:
            password (str): The password to encrypt.

        Returns:
            str: The encrypted password.
        """
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @classmethod
    def create_with_encryption(cls, **kwargs):
        """Creates a new User, including encrypting their password, if that
        User doesn't already exist. Otherwise, does nothing.

        Args:
            **kwargs: The keyword args accepts by the User NDB model. These
            are currently: password.
        """
        if not cls.get_by_id(kwargs['id']):
            kwargs['password'] = cls.encrypt_password(kwargs['password'])
            user = cls(**kwargs)
            user.put()

    @classmethod
    def update_password(cls, username, new_pw):
        """Updates an existing User's password.

        Args:
            username (User): The user that will get the new password.
            new_pw (str): The new password, unencrypted.
        """
        user = ndb.Key(cls, username).get()
        user.password = cls.encrypt_password(new_pw)
        user.put()

    @classmethod
    def login(cls, username, submitted_pw):
        """Essentially looks for an existing User based on the given username
        and submitted_pw.

        Args:
            username (str): The username.
            submitted_pw (str): The password that corresponds with the given
            username.

        Returns:
            User:

        Raises:
            EntityDoesNotExistException: Thrown if the User does not exist.
            IncorrectPasswordException: Thrown is the User exists but the wrong password
            is given.
        """
        user = cls.get_by_id(username)
        if user is None:
            raise EntityDoesNotExistException(
                "User with username '{}' does not exist.".format(username))
        stored_pw = user.password
        is_correct_pw = cls.compare_passwords(stored_pw, submitted_pw)
        if not is_correct_pw:
            raise IncorrectPasswordException
        return user
