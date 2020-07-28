################################################################################
# Model-View-Controller pattern for user interaction
#
# Purpose: The user interface is implemented with a view, database access with a
# model, and communication between view and model with a controller.
#
# Author: Kevin Chen
# Contact: chenk106@mcmaster.ca
# GitHub: https://github.com/CNIVEK/GW2-Project
#
################################################################################
from objectpool import *

class Model:
    #
    #
    #
    #
    def __init__(self):
        self._reusable_pool = ReusablePool()

    def store_data(self,num,name):
        reusable = self._reusable_pool.acquire()
        reusable.conn.set('quest'+str(num) ,(name))
        self._reusable_pool.release(reusable)
        pass

    def retrieve_data(self,):
        reusable = self._reusable_pool.acquire()
        self._reusable_pool.release(reusable)
        pass

class View:

    @staticmethod
    def start_page():
        print("\nSelect either today's or tomorrow's daily achievements:")
        print("(1) Today")
        print("(2) Tomorrow")
        print("(3) Exit")
        return int(input("Enter number to select day: "))

    @staticmethod
    def type_page():
        print("\nSelect which achievements to view:")
        print("(1) PvE")
        print("(2) PvP")
        print("(3) WvW")
        print("(4) Fractals")
        print("(5) Special")
        print("(6) All")
        return int(input("Enter number to select type: "))

    @staticmethod
    def display_report(self, achivement):
        print(achivement.name)
        print(achivement.requirement)

class Controller:
    def __init__(self):
        self._view = View()
        self._model = Model()

    def start(self):
        choice = self._view.start_page()
        if (choice == 3):
            print("Closing...")
            exit()
        else:
            return choice

    def type(self):
        return self._view.type_page()

    def create_report(self,ach_num, achivement):
        self._model.store_data(ach_num,achivement.name)
        print(achivement.name)
        print(achivement.requirement)
        print()

    def print_report(self):
        self._model.retrieve_data()
