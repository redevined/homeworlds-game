#!/usr/bin/env python

import os
import hashlib
import cPickle as serializer

SESSIONS = dict()


class User() :

    def __init__(self, un, pw, mail) :
        self.username = un
        self.password = pw
        self.email = mail
        self.role = "USER"

    def isAdmin(self) :
        return self.role == "ADMIN"


def addSession(user) :
    usid = len(SESSIONS) + 100
    SESSIONS[usid] = user
    return usid

def getBySession(usid) :
    if SESSIONS.has_key(usid) :
        return SESSIONS[usid]
    return None

def getByLogin(credentials) :
    path = os.path.join("users", credentials["username"] + ".p")

    if os.path.exists(path) :
        with open(path, "r") as f :
            user = serializer.load(f)
        if user.password == hash(credentials["password"]) :
            return addSession(user)
    return None

def getByRegister(credentials) :
    un, pw, mail, nomail = credentials["username"], credentials["password"], credentials["email"], credentials.has_key("no_email")
    path = os.path.join("users", un + ".p")

    if un and pw and (mail or nomail) and not os.path.exists(path) :
        user = User(un, hash(pw), None if nomail else mail)
        with open(path, "w") as f :
            serializer.dump(user, f)
        return addSession(user)
    return None

def hash(msg) :
    sha = hashlib.sha1(msg)
    return sha.hexdigest()
