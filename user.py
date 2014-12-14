#!/usr/bin/env python

import os
import hashlib
import cPickle as serializer


# User Class
class User(object) :

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


# Get a logged in user by his temp session ID
def getBySession(code) :
    return serializer.loads(code)

# Loads a user, logs him in and returns his temp session ID
def getByLogin(credentials) :
    path = os.path.join("users", credentials["username"] + ".p")

    if os.path.exists(path) :
        with open(path, "r") as f :
            user = serializer.load(f)
        if user.checkPassword(credentials["password"]) :
            return serializer.dumps(user)
    return None

# Creates a new user + same as above function
def getByRegister(credentials) :
    un, pw, mail, nomail = credentials["username"], credentials["password"], credentials["email"], credentials.has_key("no_email")
    path = os.path.join("users", un + ".p")

    if un and pw and (mail or nomail) and not os.path.exists(path) :
        user = User(un, pw, None if nomail else mail)
        with open(path, "w") as f :
            serializer.dump(user, f)
        return serializer.dumps(user)
    return None


# Returns a list of all existing users (for admin interface)
def getAllUsers() :
    users = []
    for path in os.listdir("users") :
        with open(os.path.join("users", path), "r") as f :
            users.append(serializer.load(f))
    return users


# Highly experimental user wrapper
def createUser(cls) :
    class Wrapper(object) :
        content = cls()
        def __getattribute__(self, key) :
            Wrapper.content.touch()
            return Wrapper.content.__getattribute__(key)

    return Wrapper
