# -*- coding: utf-8 -*-

from models import User
from flask_login.mixins import UserMixin


class AppUser(UserMixin):

    def __init__(self, user):
        self.user_model = user
        self.username = user.key.id()

    def get_id(self):
        return self.user_model.key.id()
