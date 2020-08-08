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


# Model handles interaction with database
class Model:
    def __init__(self):
        self._reusable_pool = ReusablePool()


    # Creates an report entry in the Redis database. Stores achievement name
    # description, requirement, and possible rewards with respective item name
    # and description.
    # Storage schema:
    #
    #   key         hash
    #   quest1      name == "Daily Maguuma Jungle Miner"
    #               description == "Fueling the engines of the economy."
    #               .
    #               .
    #               .
    def store_data(self,num,achivement):
        reusable = self._reusable_pool.acquire()

        questcount = "quest" + str(num + 1)
        reusable.conn.hset(questcount, "name", str(achivement.name))
        reusable.conn.hset(questcount, "description", str(achivement.description))
        reusable.conn.hset(questcount, "requirement", str(achivement.requirement))
        reusable.conn.hset(questcount, "num_of_items", len(achivement.items))
        for item_num in range(len(achivement.items)):
            item = "item" + str(item_num + 1)
            reusable.conn.hset(questcount, item, \
            str(achivement.items[item_num]["name"]))
            reusable.conn.hset(questcount, item + "desc", \
            str(achivement.items[item_num]["description"]))

        self._reusable_pool.release(reusable)


    # Creates and returns a dictionary of the achievements stored in database
    def retrieve_data(self, count):
        console_dict = {}
        reusable = self._reusable_pool.acquire()

        q_num = "quest" + str(int(count) + 1)
        console_dict["name"] = reusable.conn.hget(q_num, "name")
        console_dict["description"] = reusable.conn.hget(q_num, "description")
        console_dict["requirement"] = reusable.conn.hget(q_num, "requirement")
        num_of_items = int(reusable.conn.hget(q_num, "num_of_items"))
        console_dict["num_of_items"] = num_of_items
        for item_num in range(num_of_items):
            item = "item" + str(item_num + 1)
            console_dict[item] = \
            [reusable.conn.hget(q_num, item), \
            reusable.conn.hget(q_num, item + "desc")]

        self._reusable_pool.release(reusable)
        return console_dict

    # Records number of achivements to database for keeping track at
    # key num_of_quests:count
    def num_of_quest(self, *args):
        reusable = self._reusable_pool.acquire()
        if len(args) == 0:
            num = reusable.conn.get("num_of_quests")
            self._reusable_pool.release(reusable)
            return int(num)
        elif len(args) == 1:
            reusable.conn.set("num_of_quests", args[0])
            self._reusable_pool.release(reusable)

# View handles user interface relations
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
    def display_report(report):
        print("Achievement: " + report["name"])
        print("Description: " + report["description"])
        print("Requirement: " + report["requirement"])
        for x in range(report["num_of_items"]):
            print("Reward: " + report["item" + str(x+1)][0])
            print(report["item" + str(x+1)][1])
        print()


# Controller provides communication between View and Model
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

    # Calls the Model to store information about an achivement for corresponding
    # number of achivements
    def create_report(self, filtered_achievements):
        count = 0
        for ach_num in range(len(filtered_achievements)):
            self._model.store_data(ach_num, filtered_achievements[ach_num])
            count = count + 1
        self._model.num_of_quest(count)

    # Output report to console
    def print_report(self):
        count = self._model.num_of_quest()
        for ach_num in range (0, count):
            report = self._model.retrieve_data(ach_num)
            self._view.display_report(report)
