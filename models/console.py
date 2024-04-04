import datetime
import models
import cmd
import re
from models.base_model import BaseModel
from user import User
from State import state
from City import city
from Place import place
from Amenity import amenity
from Review import review


class HBNBCommand(cmd.Cmd):

    Storage = models.storage
    all_obj = Storage.all()

    ALL_CLASSES = {
        'BaseModel': BaseModel,
        'User': User,
        'state': state,
        'city': city,
        'place': place,
        'amenity': amenity,
        'review': review
    }
    prompt = "(hbnb) "

    def do_custom_command(self, arg):
        print('custom')

    # dynamically strip quotes of the update method (obj_value)
    def strip_quotes(self, value) -> str:
        if value is not None:
            if "\'" in value:
                value = value.strip("'")
                return value
            elif '\"' in value:
                value = value.strip('"')
                return value
            else:
                return value

    def emptyline(self) -> bool:
        pass

    def do_EOF(self, arg):
        print()
        return True

    def do_create(self, arg) -> None:
        usr_input = arg.split()
        if len(usr_input) < 1:
            print('** class name missing **')
            return
        elif usr_input[0] not in self.ALL_CLASSES:
            print('** class doesn\'t exist **')
            return

        if usr_input[0] in self.ALL_CLASSES:
            obj = self.ALL_CLASSES[usr_input[0]]()
            obj.save()
            print(f"Please Keep your id private if lost, can't access account ({obj.id})")

    def do_show(self, arg) -> None:
        """
            shows the str repre of the object
        """
        usr_input = arg.split()
        all_obj = self.Storage.all()

        # Define the regex pattern to match the desired format
        pattern = r'\w+\s\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$'

        # Compile the regex pattern
        regex = re.compile(pattern)

        match = regex.match(arg)

        # validate user_input length
        if len(usr_input) < 1:
            print('** class name missing **')
            return
        elif usr_input[0] not in self.ALL_CLASSES:
            print('** class doesn\'t exist **')
            return
        elif len(usr_input) < 2:
            print('** instance id missing **')
            return

        key = f"{usr_input[0]}.{usr_input[1]}"

        if match:
            if key in self.all_obj.keys():
                print(all_obj[key])
            else:
                print('** no instance found **')
        else:
            print("Invalid input format "
                  "<show class-name xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx>")


    def do_delete(self, arg) -> None:
        usr_input = arg.split()
        all_obj = self.Storage.all()

        # Define the regex pattern to match the desired format
        pattern = r'(\w+)?\s?(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})?$'

        # Compile the regex pattern
        regex = re.compile(pattern)

        match = regex.match(arg)

        if match is not None:
            match_grp = match.groups()
            cls_name, cls_id = match_grp

        # validate user_input length
            if not cls_name:
                print('** class name missing **')
                return
            elif cls_name not in self.ALL_CLASSES:
                print('** class doesn\'t exist **')
                return
            elif not cls_id:
                print('** instance id missing **')
                return

            # construct a key using the users info
            key = "{}.{}".format(usr_input[0], usr_input[1])
            if key in all_obj:
                    del all_obj[key]
                    self.Storage.save_obj()
                    return
            else:
                print('** no instance found **')
        else:
            print("Invalid input format "
                      "<delete class-name xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx>")

    def do_all(self, arg):
        pattern = r'([a-zA-Z]+|[.])'
        regex = re.compile(pattern)

        match = regex.match(arg)

        # if match:
        if not arg or arg in self.ALL_CLASSES :
            obj = self.all_obj

            for k, v in obj.items():
                cls_name, cls_key = k.split('.')
                if arg in cls_name:
                    print(v)
        else:
                    print('** class doesn\'t exist **')
        # else:
        #     print('Invalid Input format Try Again <(all .) or all (object)>')


    def calc_updated_at_last(self, model) -> None:
        model_updated_at = getattr(model, 'updated_at')
        current_time = datetime.datetime.now()
        time_difference = current_time - model_updated_at
        if not time_difference > datetime.timedelta(minutes=1):
            print("sorry you have to wait for 1minute before you can update account again")
            return


    def match_pattern(self, arg) -> re.Match:
        # pattern matches string with (single apostrophe <'> or with double <"> or without an apostrophe)
        pattern =  r"([a-zA-Z_-]+\S+)?\s?([a-zA-Z0-9-]+)?\s?([a-zA-Z_]+)?\s?" \
                   r"(\'\w+\s?\w+\'|\"\w+\s?\w+|\w+\s?\w+)?"
#          update BaseModel 7cec092c-83c0-4c56-9415-e60219debab
        regex = re.compile(pattern)
        match_object = regex.search(arg)

        return match_object

    def check_arg(self, key, match_arg_group:tuple) -> None:
        if match_arg_group[0] is None:
            print('** class name missing **')
            return
        else:
            if match_arg_group[0] not in self.ALL_CLASSES:
                print('** class doesn\'t exist ** ')
                return

        if match_arg_group[1] is None:
            print('** instance id missing **')
            return
        else:
            if key not in  self.all_obj:
                print('** no instance found **')
                return

        if match_arg_group[2] is None:
            print('** attribute name missing **')
            return
        elif match_arg_group[3] is None:
            print('** value missing **')
            return

        return match_arg_group

    def do_update(self, arg) -> None:
        """
            update <class name> <id> <attribute name> "<attribute value>"
        """
        obj_dict = self.all_obj
        matches = self.match_pattern(arg)
        match_obj = matches.groups()
        key = f"{match_obj[0]}.{match_obj[1]}"
        all_obj = self.check_arg(key, match_obj)

        if all_obj is not None:
            obj_name, obj_id, obj_attri, obj_value = all_obj
            print(all_obj)
            # print(match_obj)

            model = obj_dict[key]

            if hasattr(model, obj_attri):
                # only update str, int and float
                if not isinstance(getattr(model, obj_attri), (str, int, float)):
                    print(f"Sorry can't update attribute of type {type(getattr(model, obj_attri))}")
                    return

                if obj_attri not in ['name', 'age', 'email', 'DOB']:
                    print('sorry you can only update your name, age and email only! ')
                    return
                else:
                    try:
                        if obj_attri == 'age':
                            if self.strip_quotes(obj_value):
                                obj_value = self.strip_quotes(obj_value) # strip method.
                                obj_value = int(obj_value)
                                # self.calc_updated_at_last(model)         # updated_at time differece method
                                setattr(model, obj_attri, obj_value)
                                self.Storage.save_obj() # call the save method of the FileStorage to write object back to file.json.
                                model.save()            # update the updated_at from the BaseModel save method.
                                print(f'({obj_attri}) Updated successfully!')
                                return
                        else:
                            obj_value = self.strip_quotes(obj_value)
                            # self.calc_updated_at_last(model)
                            setattr(model, obj_attri, obj_value) # strip out ("") from the value.
                            self.Storage.save_obj() # call the save method of the file storage to write back object to file_db
                            model.save()
                    except ValueError:
                        print(f'Input <{obj_value}> not a valid format for attribute [age],'
                              f' must be type int!, eg: (18, 19 40)')
                        return
            else:
                print(f"attribute <{obj_attri}> does not exist")
                return

    def do_quit(self, arg) -> bool:
        print("Thank you for having an account with us! 🚀")
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()





# Rough work
"""
if key not in all_obj:
            print('** no instance found **')
            print('** class name missing **')
            return
        elif obj_id is None:
            print('** instance id missing **')
            return
        elif obj_attri is None:
            print('** attribute name missing **')
            return
        elif obj_value is None:
            print('** value missing **')
            return

        key = f"{obj_id}.{obj_name}"

        if obj_name not in self.ALL_CLASSES:
        if obj_name not in self.ALL_CLASSES:
            print('** class doesn\'t exist ** ')
            return
        if key not in all_obj:
            print('** no instance found **')
            return


 pattern = r'(\w+\s\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\s\w+\s\w+$)'
        id_pattern = r'^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$'

        regex_id = re.compile(id_pattern)
        regex = re.compile(pattern)

        match = regex.match(arg)

        if len(usr_input) < 1:
            print('** class name missing **')
            return
        elif usr_input[0] not in self.ALL_CLASSES:
            print('** class doesn\'t exist **')
            return
        elif len(usr_input) < 2:
            print('** instance id missing **')
            return
        elif len(usr_input) < 3:
            match_id = regex_id.match(usr_input[1])
            if not match_id:
                print("invalid id format <xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx>")
            else:
                print('** attribute name missing**')
            return
        elif len(usr_input) < 4:
            print('** attribute value missing**')
            return


        # print(all_obj)
        key = f"{usr_input[1]}.{usr_input[0]}"

        # for k, v in all_obj.items():
        if key in all_obj.keys():
            object = all_obj[usr_input[0]]()
            print(object)

        #
        # key = f"{usr_input[1]}.{usr_input[0]}"
        # if match:
        #     if key in all_obj.keys():
        #         dic_repr = all_obj[key].__dict__
        #
        #         if usr_input[2] in dic_repr.keys():
        #             if isinstance(dic_repr[usr_input[2]], (int, str)):
        #                 dic_repr[usr_input[2]] = usr_input[3]
        #             else:
        #                 print("Sorry only attribute str, int can be updated")
        #         else:
        #             print("Sorry attribute {} dose not exist".format(usr_input[2]))
        #         self.Storage.save_obj()
        # else:
        #     print('invalid input update '
        #           '<class name> <xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx>'
        #           ' <attribute name> "<attribute value>')
"""
