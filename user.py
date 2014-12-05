#!/usr/bin/env python

import os
import hashlib
import cPickle as serializer

# Dictionary of temporary session IDs and according users
SESSIONS = dict()


# User Class
class User() :

    # Constructor
    def __init__(self, un, pw, mail) :
        self.username = un
        self.password = hash(pw)
        self.email = mail
        self.role = "USER"

    # Compares password hashes
    def checkPassword(self, pw) :
        return self.password == hash(pw)

    # Checks for admin rights
    def isAdmin(self) :
        return self.role == "ADMIN"


# Improved hash function (SHA1)
def hash(msg) :
    sha = hashlib.sha1(msg)
    return sha.hexdigest()

# Returns a list of all existing users (for admin interface)
def getAllUsers() :
    users = []
    for path in os.listdir("users") :
        with open(os.path.join("users", path), "r") as f :
            users.append(serializer.load(f))
    return users

# Logs user in and returns his temporary session ID
def addSession(user) :
    usid = len(SESSIONS) + 100
    SESSIONS[usid] = user
    return usid

# Function to log user out
def removeSession(usid) :
    del(SESSIONS[usid])

# Returns a list of all temp session IDs and users
def getAllSessions() :
    return SESSIONS.items()

# Get a logged in user by his temp session ID
def getBySession(usid) :
    if SESSIONS.has_key(usid) :
        return SESSIONS[usid]
    return None

# Loads a user, logs him in and returns his temp session ID
def getByLogin(credentials) :
    path = os.path.join("users", credentials["username"] + ".p")

    if os.path.exists(path) :
        with open(path, "r") as f :
            user = serializer.load(f)
        if user.checkPassword(credentials["password"]) :
            return addSession(user)
    return None

# Creates a new user + same as above function
def getByRegister(credentials) :
    un, pw, mail, nomail = credentials["username"], credentials["password"], credentials["email"], credentials.has_key("no_email")
    path = os.path.join("users", un + ".p")

    if un and pw and (mail or nomail) and not os.path.exists(path) :
        user = User(un, pw, None if nomail else mail)
        with open(path, "w") as f :
            serializer.dump(user, f)
        return addSession(user)
    return None
