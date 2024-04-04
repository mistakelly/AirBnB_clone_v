"""
    responsible for persisting object state in file_db.
"""

import json
from os import path
from models.base_model import BaseModel
from models.user import User
from models.State import state
from models.City import city
from models.Place import place
from models.Amenity import amenity
from models.Review import review

__all__ = ['FileStorage']


class FileStorage:
    """
        FileStorage.
    """
    ALL_CLASSES = {
        'BaseModel': BaseModel,
        'User': User,
        'state': state,
        'city': city,
        'place': place,
        'amenity': amenity,
        'review': review
    }
    __objects = {}
    __filepath = 'file.json'

    def new(self, obj) -> None:
        print('inside new obj')

        """
            this adding New Object to file storage.
        """
        # construct key
        key = "{}.{}".format(
            obj.__class__.__name__, obj.id
        )
        self.__objects[key] = obj
        print('after new obj')

    def all(self) -> dict:
        """
            this method is responsible for returning the whole
            object in the file __objects dictionary.
        """
        return self.__objects

    def save_obj(self) -> None:
        print('inside save method')
        """
            for converting the python objects into python dictionary,
            so they can be stored into the file storage,this process is called
            serialization.
        """
        # declare dictionary.
        serialized_obj = {}

        for k, v in self.__objects.items():
            # call the to_dict method in the basemodel
            # to represent every object to dict.
            serialized_obj[k] = v.to_dict()

        # print(serialized_obj)
        # dump into file storage
        with open(self.__filepath, "w") as obj_dic:
            json.dump(serialized_obj, obj_dic, indent=2)

            print("outside the save_obj")

    def reload(self) -> None:
        """
            responsible for reloading the object in file storage and
            dynamically create objects out of the data in the file storage
        """

        # open file
        # split the key of the dictionary
        # dynamically create classes base on the class name.
        if path.exists(self.__filepath) and path.getsize(self.__filepath) > 0:
            with open(self.__filepath, "r") as db:

                file_content = json.load(db)

                for k, v in file_content.items():

                    # split the dictionary key
                    cls_name, cls_key = k.split('.')

                    # dynamically create the class object again according to the entry in db.

                    # same as doing.
                    global_class = self.ALL_CLASSES[cls_name]

                    result = global_class(**v)
                    # print(result)

                    self.__objects[k] = result
