#!/usr/bin/env python

import time
from threading import Thread



# Container class for user sessions
class UserSessions() :

    # Constructor
    def __init__(self, timeout = 60*30, interval = 60) :
        self.users = dict()
        if timeout :
            self.timeout = timeout
            self.startCleaner(interval)

    # Stop thread on delete
    def __del__(self) :
        self.stopCleaner()

    # Starts cleanup thread
    def startCleaner(self, interval) :
        self.cleaning = True
        Thread(target = self.clean, args = (interval,)).start()

    # Stops cleanup thread
    def stopCleaner(self) :
        self.cleaning = False

    # Cleanup thread, deleting old sessions
    def clean(self, interval) :
        while self.cleaning:
            now = time.time()
            for sid, user in self.users.items() :
                if now - user.timestamp > self.timeout :
                    self.remove(sid)
            time.sleep(interval)

    # Returns user by his session ID, if not present returns None
    def get(self, sid) :
        if self.users.has_key(sid) :
            return self.users[sid]
        return None

    # Adds user and returns his session ID
    def add(self, user) :
        sid = max(self.users.keys()) + 1 if self.count() > 0 else 100
        self.users[sid] = user
        return sid

    # Deletes user from container
    def remove(sid) :
        del(self.users[sid])

    # Returns number of current sessions
    def count(self) :
        return len(self.users)

    # Returns all sessions
    def getAll(self) :
        return self.users.items()
