#!/usr/bin/env python

import os, time
import hashlib
import cPickle as serializer
from session import UserSessions

# Object containing all user sessions
session = UserSessions()



# User Class
class User() :

    # Constructor
    def __init__(self, un, pw, mail, role = "USER") :
        self.username = un
        self.password = self._hash(pw)
        self.email = mail
        self.role = role

        self.touch()
        _save(self)

    # Triggers save before deleting the user instance
    def __del__(self) :
        _save(self)

    # Improved hash function (SHA1)
    def _hash(self, msg) :
        sha = hashlib.sha1(msg)
        return sha.hexdigest()

    # Updates the timestamp to control last user activity
    def touch(self) :
        self.timestamp = time.time()

    # Compares password hashes
    def checkPassword(self, pw) :
        return self.password == self._hash(pw)

    # Checks for admin rights
    def isAdmin(self) :
        return self.role == "ADMIN"

    # Returns timestamp as strtuct_time object or a pretty string
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



# Saves the modified user
def _save(user) :
    path = os.path.join("users", user.username + ".p")
    with open(path, "w") as f :
        serializer.dump(f, user)

# Loads a serialized user and returns him
def _load(name) :
    path = os.path.join("users", name + ".p")
    if os.path.exists(path) :
        with open(path, "r") as f :
            return serializer.load(f)
    return None



# Get a logged in user by his session ID
def getBySession(sid) :
    user = session.get(sid)
    user.touch()
    return user

# Removes user from sessions
def removeSession(sid) :
    session.remove(sid)

# Loads a user, logs him in and returns his session ID
def getByLogin(credentials) :
    user = _load(credentials["username"])
    if user :
        if user.checkPassword(credentials["password"]) :
            return session.add(user)
    return None

# Creates a new user + same as above function
def getByRegister(credentials) :
    un, pw, mail, nomail = credentials["username"], credentials["password"], credentials["email"], credentials.has_key("no_email")
    if un and pw and (mail or nomail) and not _load(un) :
        return session.add(User(un, pw, None if nomail else mail))
    return None



# Returns a list of all existing users (for admin interface)
def getAllUsers() :
    users = []
    for path in os.listdir("users") :
        with open(os.path.join("users", path), "r") as f :
            users.append(serializer.load(f))
    return users

# Returns a dictionary of logged in users, along with their session IDs (for admin interface)
def getCurrentUsers() :
    return session.getAll()
