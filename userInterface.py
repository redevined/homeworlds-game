#!/usr/bin/env python

import os, hashlib, re
import cPickle as serializer
from flask import redirect, session as cookie

# Server side session management classes
from session import SessionItem, SessionContainer

# Object containing all active user sessions
session = SessionContainer()


# User Class
class User(SessionItem) :

    # Constructor
    def __init__(self, un, pw, mail, role = "USER") :
        self.username = un
        self.password = self._hash(pw)
        self.email = mail
        self.role = role
        self.games = []

        self.touch()
        _save(self)

    # Triggers save before deleting the user instance
    def __del__(self) :
        _save(self)

    # Improved hash function (SHA1)
    def _hash(self, msg) :
        sha = hashlib.sha1(msg)
        return sha.hexdigest()

    # Compares password hashes
    def checkPassword(self, pw) :
        return self.password == self._hash(pw)

    # Checks for admin rights
    def isAdmin(self, elevate = None) :
        if elevate is not None :
            self.role = "ADMIN" if elevate else "USER"
        return self.role == "ADMIN"


# Saves the modified user
def _save(user) :
    path = os.path.join("users", user.username + ".p")
    with open(path, "w") as f :
        serializer.dump(user, f)

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
    if user :
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
    if re.match(r"[\w\s._()]+", un) and pw and (mail or nomail) and not _load(un) :
        return session.add(User(un, pw, None if nomail else mail))
    return None

# Returns an user by his username
def getByName(name) :
    user = session.getByAttr(username = name)
    return user or _load(name)

# Deletes an user
def deleteByName(name) :
    os.remove(os.path.join("users", name + ".p"))

# Returns a list of all existing users
def getAllUsers() :
    names = [path.rsplit(".", 1)[0] for path in os.listdir("users")]
    return [getByName(name) for name in names]

# Returns a dictionary of logged in users, along with their session IDs
def getCurrentUsers() :
    return session.getAll()


# Decorator to check if user is logged in
def auth(action) :
    def decorator(*args, **kwargs) :
        user = getBySession(cookie.get("user"))
        if user :
            return action(*args, **kwargs)
        return redirect("/login")
    decorator.__name__ = action.__name__
    return decorator

# Check if user is logged in and has admin rights
def authAdmin(action) :
    def decorator(*args, **kwargs) :
        user = getBySession(cookie.get("user"))
        if user :
            if user.isAdmin() :
                return action(*args, **kwargs)
        return redirect("/login")
    decorator.__name__ = action.__name__
    return decorator
