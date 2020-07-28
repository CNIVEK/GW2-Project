################################################################################
# Facade pattern to wrap the subsystem
#
# Purpose: Intent is to provide a unified interface to a set of interface in
# this system.
#
# Author: Kevin Chen
# Contact: chenk106@mcmaster.ca
# GitHub: https://github.com/CNIVEK/GW2-Project
#
################################################################################
from singleton import *
from filter import *
from mvc import *
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

import time

class SystemWrapper(metaclass = Singleton):
    def __init__(self):
        self._controller = Controller()
        self._filter = Filter()

    def daily(self):
        day = self._controller.start()
        dict_of_achivements = self._filter.getRelevantDay(day)
        type = self._controller.type()
        dict_of_achivements = self._filter.getRelevantType(dict_of_achivements,type)

        start = time.perf_counter() #testing

        id = []
        for achivement in dict_of_achivements:
            id.append(achivement["id"])

        with concurrent.futures.ThreadPoolExecutor(max_workers = 1) as executor:
            achievements_detailed = executor.map(self._filter.getAchievementInfo, id)

        filtered_achievements = self._filter.filterAchievements(achievements_detailed)

        for ach_num in range(len(filtered_achievements)):
            for reward_num in range(len(filtered_achievements[ach_num].rewards)):
                filtered_achievements[ach_num].items.append \
                (self._filter.getItemInfo((filtered_achievements[ach_num].rewards[reward_num]["id"])))

            self._controller.create_report(ach_num,filtered_achievements[ach_num])

        finish = time.perf_counter()
        print(f'Finished in {round(finish-start, 2)} second(s)')
