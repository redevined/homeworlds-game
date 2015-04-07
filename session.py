#!/usr/bin/env python

import time
from threading import Thread


# Parent class for session items
class SessionItem() :

    # Updates the timestamp to control last item activity
    def touch(self) :
        self.timestamp = time.time()

    # Returns timestamp as struct_time object or a pretty string
    def getLastSeen(self, pretty = False) :
        date = time.localtime(self.timestamp)
        if pretty :
            return "{}.{}.{} - {}:{}".format(
                date.tm_mday,
                date.tm_mon,
                date.tm_year,
                date.tm_hour,
                date.tm_min
            )
        else :
            return date


# Container class for sessions
class SessionContainer() :

    # Constructor
    def __init__(self, timeout = 60*30, interval = 60) :
        self.items = dict()
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
            for sid, item in self.items.items() :
                if now - item.timestamp > self.timeout :
                    self.remove(sid)
            time.sleep(interval)

    # Returns item by its session ID, if not present returns None
    def get(self, sid) :
        if self.items.has_key(sid) :
            return self.items[sid]
        return None

    # Adds item and returns its session ID
    def add(self, item) :
        sid = max(self.items.keys()) + 1 if self.count() > 0 else 100
        self.items[sid] = item
        return sid

    # Deletes item from container
    def remove(self, sid) :
        del(self.items[sid])

    # Returns number of current sessions
    def count(self) :
        return len(self.items)

    # Returns item by one of its attributes
    def getByAttr(self, **attrs) :
        for attr, val in attrs.items() :
            for item in self.items.values() :
                if getattr(item, attr) == val :
                    return item
        return None

    # Returns all sessions
    def getAll(self) :
        return self.items.items()
