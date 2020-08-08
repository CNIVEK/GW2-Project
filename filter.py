################################################################################
# API calls and filter data
#
# Purpose: The Filter class is responsible for API calls and to refine the
# obtained data. The FilteredData object is used to provide more abstraction.
#
# Author: Kevin Chen
# Contact: chenk106@mcmaster.ca
# GitHub: https://github.com/CNIVEK/GW2-Project
#
################################################################################
import requests
from decorator import *

class Filter:
    def __init__(self):
        self._base_api = BaseAPI()
        self._api_achievement = AchievementDecorator(self._base_api)

    # Calls API to get today or tommorows list of achievements
    def getRelevantDay(self,day):
        if (day == 1):
            self._api_day = DailyDecorator(self._api_achievement)
        elif (day == 2):
            self._api_day = TomorrowDecorator(DailyDecorator(self._api_achievement))

        list_of_achivements = requests.get(self._api_day.request()).json()
        return list_of_achivements

    # Filters day of achievements to specific type
    def getRelevantType(self,list,type):
        if (type == 1):
            return list["pve"]
        elif (type == 2):
            return list["pvp"]
        elif (type == 3):
            return list["wvw"]
        elif (type == 4):
            return list["fractals"]
        elif (type == 5):
            return list["special"]
        else:
            return list["pve"] + list["pvp"] + list["wvw"]+ list["fractals"] + list["special"]

    # Calls API to get information about specific achievements
    def getAchievementInfo(self,id):
        self._api_1achievement = AchievementIDDecorator(self._api_achievement)
        achivement = requests.get(self._api_1achievement.request(id)).json()
        return achivement

    # Calls API to get information about specific item
    def getItemInfo(self,id):
        self._api_item = ItemDecorator(self._base_api)
        item = requests.get(self._api_item.request(id)).json()
        return item

    # Makes FilteredData objects with relevant information
    def filterAchievements(self, achievements):
        self._list_of_data = []
        for ach in achievements:
            self._list_of_data.append(FilteredData(ach["id"], ach["name"], \
            ach["description"], ach["requirement"], ach["rewards"]))
        return self._list_of_data


class FilteredData:
    def __init__(self, id, name, description, requirement, rewards):
        self.id = id
        self.name = name
        self.description = description
        self.requirement = requirement
        self.rewards = rewards
        self.items = []
