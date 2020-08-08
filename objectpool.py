################################################################################
# Object pool pattern to manage database connection
#
# Purpose: The Redis Labs database connection is made into a reusable object.
# Object pool pattern is used to recycle the reusable object resource.
#
# Author: Kevin Chen
# Contact: chenk106@mcmaster.ca
# GitHub: https://github.com/CNIVEK/GW2-Project
#
################################################################################
import redis
from singleton import *

class ReusablePool(metaclass = Singleton):
    def __init__(self):
        self._reusables = [Reusable()]

    def acquire(self):
        return self._reusables.pop()

    def release(self, reusable):
        self._reusables.append(reusable)

# Reuseable Redis Labs database connection
class Reusable:
    def __init__(self):
        self.conn = redis.Redis(
            host = "redis-16791.c11.us-east-1-2.ec2.cloud.redislabs.com",
            port = 16791,
            password = "GtnvNVBEqmZEgDfOyiRLeFKGg95oNjEt",
            decode_responses = True
        )
