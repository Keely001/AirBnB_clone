#!/usr/bin/python3
import cmd
import shlex
from models.base_model import BaseModel
from models.user import User
from models import storage
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review
import json

models_dict = {
    "BaseModel": BaseModel,
    "User": User,
}

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def emptyline(self):
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it to the JSON file, and prints the id."""
        if not arg:
            print("** class name missing **")
            return
        if arg not in models_dict:
            print("** class doesn't exist **")
            return
        obj = models_dict[arg]()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id."""
        if not arg:
            print("** class name missing **")
            return
        args = shlex.split(arg)
        if args[0] not in models_dict:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id (save the change into the JSON file)."""
        if not arg:
            print("** class name missing **")
            return
        args = shlex.split(arg)
        if args[0] not in models_dict:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[key]
            storage.save()

    def do_all(self, line):
        """
        Retrieve all instances of a class.
        Usage: all <class_name> or <class_name>.all()
        """
        args = line.split()
        if args and args[0] and args[0] in models_dict:
            cls_name = args[0]
            if '.' in cls_name:
                cls_name = cls_name.split('.')[0]

            # Use the storage.all method to retrieve instances by class name
            instances = storage.all(models_dict[cls_name])

            if not instances:
                print("** No instances found **")
                return

            for instance_id, instance in instances.items():
                print(instance)
        else:
            print("** class doesn't exist **")


    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file)."""
        if not arg:
            print("** class name missing **")
            return
        args = shlex.split(arg)
        if args[0] not in models_dict:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        obj = storage.all()[key]
        setattr(obj, args[2], args[3])
        obj.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()

