#!/usr/bin/python3
"""
A module for cmd interpreter for AirBnB clone
"""

import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """A console class for the AirBnB-Clone project"""

    prompt: str = '(hbnb)'
    __class_lst = {
        BaseModel.__name__: BaseModel,
        User.__name__: User,
        State.__name__: State,
        City.__name__: City,
        Place.__name__: Place,
        Amenity.__name__: Amenity,
        Review.__name__: Review
    }
    __class_funcs = ["all", "count", "show", "destroy", "update"]

    @staticmethod
    def parse(arg, id=" "):
        """
        Returns. alist containg the parsed arguments from the string
        """

        arg_list = arg.split(id)
        narg_list = []

        for x in arg_list:
            if x != '':
                narg_list.append(x)
        return narg_list

    def do_quit(self, arg):
        """Command to Exit the program"""

        return True

    def help_quit(self):
        """Prints help doc for the quit command"""

        print("Quit command to exit the program\n")

    def do_EOF(self, arg):
        """Command to Exit the program"""

        print("")
        return True

    def do_create(self, arg):
        """
            Creates a new instance of BaseModel,
            saves it (to the JSON file) and prints
            the id.
                Ex: $ create BaseModel
        """

        arg_s = HBNBCommand.parse(arg)
        if len(arg_s) == 0:
            print("** class name missing **")
            return False

        if len(arg_s) > 1:
            print("** to many arguments **")
            return False

        if (arg_s[0] in HBNBCommand.__class_lst.keys()):
            new_obj = HBNBCommand.__class_lst[arg_s[0]]()
            new_obj.save()
            print(new_obj.id)
        else:
            print("** class doesn't exist **")

    def help_create(self):
        """
            prints Help info for the create function
        """
        print("""Creates a new instance of the first argument,
              stores it in the JSON file and prints its id""")

    def do_show(self, arg):
        """
            Prints the string representation of an instance based
            on the class name and id.
                Ex: $ show BaseModel 1234-1234-1234
        """
        arg_s = HBNBCommand.parse(arg)
        db = models.storage.all()
        if not len(arg_s):
            print("** class name missing **")
        elif (arg_s[0] not in HBNBCommand.__class_lst.keys()):
            print("** class doesn't exist **")
        elif len(arg_s) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_s[0], arg_s[1]) not in db:
            print("** no instance found **")
        else:
            print(db["{}.{}".format(arg_s[0], arg_s[1])])


    def help_show(self):
        """
            Prints Help for for the create command function
        """
        print("""Prints the string representation of an instance based
            on the class name and id.
                Ex: $ show BaseModel 1234-1234-1234
            """)

    def do_destroy(self, arg):
        """
            Deletes an instance based on the class name and id
            (save the change into the JSON file).
                Ex: $ destroy BaseModel 1234-1234-1234
        """
        arg_s = HBNBCommand.parse(arg)
        models.storage.reload()
        db = models.storage.all()
        if not len(arg_s):
            print("** class name missing **")
        elif (arg_s[0] not in HBNBCommand.__class_lst.keys()):
            print("** class doesn't exist **")
        elif len(arg_s) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_s[0], arg_s[1]) not in db:
            print("** no instance found **")
        else:
            del db["{}.{}".format(arg_s[0], arg_s[1])]
            models.storage.save()

    def help_destroy(self):
        """
            Prints Help for the destroy command function
        """
        print("""Deletes an instance based on the class name and id
              (save the change into the JSON file).
                Ex: $ destroy BaseModel 1234-1234-1234""")

    def do_all(self, arg):
        """
            Prints all string representation of all instances based or
            not on the class name.
                Ex: $ all BaseModel or $ all
        """
        arg_list = HBNBCommand.parse(arg)
        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.__class_lst:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in models.storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arg_list) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def help_all(self):
        """
            prints help for the all command function
        """
        print("""Prints all string representation of all instances based or
            not on the class name.
                Ex: $ all BaseModel or $ all""")

    def do_update(self, arg):
        """
            Updates an instance based on the class name and id by adding or
            updating attribute (save the change into the JSON file).
                Ex: $ update BaseModel 1234-1234-1234 email
                      "aibnb@holbertonschool.com"
        """
        arg_list = HBNBCommand.parse(arg)
        objdict = models.storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False
        if arg_list[0] not in HBNBCommand.__class_lst:
            print("** class doesn't exist **")
            return False
        if len(arg_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_list[0], arg_list[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arg_list) == 4:
            obj = objdict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = valtype(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = objdict["{}.{}".format(arg_list[0], arg_list[1])]
            for k, v in eval(arg_list[2]).items():
                if (k in obj.__class__.__dict__.keys() and type(
                        obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        models.storage.save()

    def help_update(self):
        """
            prints Help for the update command function
        """
        print(
            """Updates an instance based on the class name and id by adding or
            updating attribute (save the change into the JSON file).
                Ex: $ update BaseModel 1234-1234-1234
                      email "aibnb@holbertonschool.com""")

    def emptyline(self):
        """
            Does nothing if Empty line + enter is inserted.
            Used for overriding the emptyline function
        """
        pass

    def do_count(self, arg):
        """
            Prnits the number of elements inside the FileStorage that
            are of instances of cls
        """
        arg_list = HBNBCommand.parse(arg)
        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.__class_lst:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in models.storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arg_list) == 0:
                    objl.append(obj.__str__())
            print(len(objl))


if __name__ == "__main__":
    console = HBNBCommand()
    console.cmdloop()
