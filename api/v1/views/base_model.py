#!/usr/bin/python3
"""
This module defines the BaseModel class.
"""

import uuid
from datetime import datetime
import models
import hashlib


class BaseModel:
    """This class defines all common attributes/methods for other classes."""

    id = ""
    created_at = ""
    updated_at = ""

    def __init__(self, *args, **kwargs):
        """This method initializes a new instance of the BaseModel class."""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key,
                            datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                elif key == '__class__':
                    pass
                else:
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            time = datetime.now()
            if 'created_at' not in kwargs:
                self.created_at = time
            if 'updated_at' not in kwargs:
                self.updated_at = time
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
        models.storage.new(self)

    def __str__(self):
        """This method returns a string representation of the object."""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """This method updates the attribute updated_at with the current
        datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """This method returns a dictionary representation of the object."""
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in my_dict:
            del my_dict['_sa_instance_state']
        if save_to_disk is False and 'password' in my_dict:
            del my_dict['password']
        return my_dict


class User(BaseModel):
    """This class defines attributes/methods for the User class."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """This method initializes a new instance of the User class."""
        if kwargs:
            password = kwargs.get('password')
            if password:
                password = hashlib.md5(password.encode())
                password = password.hexdigest()
                kwargs['password'] = password
        super().__init__(*args, **kwargs)

    def __str__(self):
        """This method returns a string representation of the object."""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

