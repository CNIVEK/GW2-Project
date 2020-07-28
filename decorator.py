################################################################################
# Decorator pattern for api customization
#
# Purpose: The Decorator pattern is used to customize the Guild Wars 2 API for
# calls. The API class defines the Component, the BaseAPI class defines the
# ConcreteComponent that will be decorated. APIDecorator defines the
# Decorator class. (something)Decorator defines the ConcreteDecorator classes
# that will "decorate" the API.
#
# API: https://wiki.guildwars2.com/wiki/API:Main
#
# Author: Kevin Chen
# Contact: chenk106@mcmaster.ca
# GitHub: https://github.com/CNIVEK/GW2-Project
#
################################################################################
from abc import ABC, abstractmethod

class API(ABC):
    @abstractmethod
    def request(self):
        pass

class BaseAPI(API):
    def request(self):
        return ("https://api.guildwars2.com/v2")

class APIDecorator(API):
    def __init__(self,baseapi):
        self._baseapi = baseapi

    def request(self):
        pass

class AchievementDecorator(APIDecorator):
    def request(self):
        return(self._baseapi.request() + "/achievements")

class DailyDecorator(APIDecorator):
    def request(self):
        return(self._baseapi.request() + "/daily")

class TomorrowDecorator(APIDecorator):
    def request(self):
        return(self._baseapi.request() + "/tomorrow")

class AchievementIDDecorator(APIDecorator):
    def request(self,id):
        return(self._baseapi.request() + "/" + str(id))

class ItemDecorator(APIDecorator):
    def request(self,id):
        return(self._baseapi.request() + "/items/" + str(id))
