# coding=utf-8
#!/usr/bin/env python2

# Welcome to {Game Title}
# This is a text based game inspired by Fallout written in Python
#
# @copyright   2015            Alexander Young, Noah Hayes
# @license     MIT Licence     <https://github.com/meun5/camel-game-python/blob/master/LICENSE>
# @link        Github          <https://github.com/meun5/camel-game-python/>
# @version     alpha-dev       0.1.1
#
# Credits:
# @author      Alexander Young <youngale@urbandaleschools.com>
# @designer    Noah Hayes      <hayesnoa@urbandaleschools.com>
#
# Fallout is Copyright Bethesda Game Studios
# Copyright infringement was not the intent of this game

from __future__ import print_function
from datetime import date, timedelta
from sys import exit
import random
import string
import time
import json
import os.path, os
import datetime

gameTitle = "sudo apt-get install a-virus.pyc#!=="
gameTitle += ''.join(random.choice(string.hexdigits) for i in range(36))

save_name = "save.json"

# The story begins on 23/10/2287
curr_date = datetime.date(2287, 10, 23)

maxTravel = {
    "user": {
        "max": 547,
        "min": 120,
    },
    "haters": {
        "max": 176,
        "min": 15,
    }
}

maxGain = 45

inv = {
    "cola": 3,
    "radroach": 3,
    "kilometres": 1212795138968,
    "haters_back": 150,
    "day": 1,
    "stats": {
        "health": 100,
        "thirst": 75,
        "bandwidth": 250,
    },
}

limits = {
    "eat": 1,
    "drink": 300,
    "deduct_min": {
        "health": 2,
        "thirst": 2,
        "bandwidth": 3,
    },
    "deduct_max": {
        "health": 7,
        "thirst": 9,
        "bandwidth": 6,
    },
}

senarios = {
    "general": {
        "haters": "The haters are {amount} kilometres behind you.",
        "travel": "You traveled {amount} kilometres",
        "call_isp": "You are out of Bandwidth. Call Bell Canada at 1 866 310-BELL."
    },
    "travel": {
        0: {
            "message": "Nothing interseting happened today.",
            "gained": "You traveled {amount} kilometres",
            "special": "kilometres|same",
            "type": "kilometres",
            "event": "none",
        },
        1: {
            "message": "You got stuck in a boring conversation and it took all day to get out.",
            "gained": "You didn't travel at all today",
            "special": "kilometres|none",
            "type": "kilometres",
            "event": "none"
        },
        2: {
            "message": "Whilst traveling you found a stash of food!",
            "gained": "You gained {amount} radroach meats",
            "special": "radroach|inc",
            "type": "radroach",
            "event": "none",
        },
        3: {
            "message": "While you where traveling you happened to find a vending machine with Nuka Cola in it!",
            "gained": "You gained {amount} litres of Nuka Cola",
            "special": "cola|inc",
            "type": "cola",
            "event": "none",
        },
        4: {
            "message": "Whilst traveling you where attacked by a deathclaw. Your travel distance was cut in half.",
            "gained": "You traveled {amount} kilometres",
            "special": "kilometres|half",
            "type": "kilometres",
            "event": "battle",
        },
        5: {
            "message": "Whilst traveling you passed by a friendly internet cafe. Some generous trolls gave some Nuka Cola",
            "gained": "You gain {amount} litres of Nuka Cola",
            "special": "cola|inc",
            "type": "cola",
            "event": "none",
        },
        6: {
            "message": "While you where traveling you where MITM'ed by a hatin' sysadmin. While you battled with him, the haters gained ground.",
            "gained": "You traveled {amount} kilometres",
            "special": "haters_back|inc",
            "type": "kilometres",
            "event": "battle",
        },
    },
}

isGame = True
need_bandwidth = False

def init():
    print()
    load()
    printBlank(2)
    print("Note: This game looks best when played in a fullscreen black and green terminal")
    printBlank(3)
    print("This game was heavily inspired by:")
    printBlank(3)
    printTitle()
    printBlank(5)
    print("Disclaimer: This game may contain one or more of the following:")
    print()
    print("1. Geroge Mush")
    print("2. Memes")
    print("3. Illuminate")
    print("4. Disclaimers")
    print("5. John Wayne")
    print("7. Codes")
    print("8. Serious Mispellings")
    print("9. Fallout Refrences")
    print("10. etc..")
    time.sleep(2)
    printBlank(2)
    print("Good. Now that that's out of the way we can continue")
    time.sleep(4)
    printBlank(3)
    print("Welcome to", gameTitle)
    print()
    print("This is a game about getting your C-- Cert.")
    print("You will travel across the great Internet to a place called Univeristy of Idaho in Denmark, Russia, Canada 6089234.")
    print("<{Insert Story Here}>")
    print()
    printStats()
    printMenu()
    gameRunner()

def printTitle():
    print("     ______            __    __                  __ ")
    print("    / ____/  ____ _   / /   / /  ____   __  __  / /_")
    print("   / /_     / __ `/  / /   / /  / __ \ / / / / / __/")
    print("  / __/    / /_/ /  / /   / /  / /_/ // /_/ / / /_  ")
    print(" /_/       \__,_/  /_/   /_/   \____/ \____/  \__/  ")

def printInv():
    print("Today's date:", curr_date)
    print()
    print("You have", "{:,}".format(inv["cola"]), "litres of Nuka Cola")
    print("You have", "{:,}".format(inv["radroach"]), "radroach meats")
    print("You have", "{:,}".format(inv["kilometres"]), "kilometres to go")
    print("The Haters are", "{:,}".format(inv["haters_back"]), "kilometres behind you")

def printEoD(obj):
    if isinstance(obj, object):
        for i in obj:
            print(obj[i])

def printMenu():
    printInv()
    printBlank(2)
    print("T: Travel")
    print("D: Drink")
    print("R: Eat")
    print("S: Scavange")
    if need_bandwidth:
        print("C: Call ISP")
    print("#: Sleep/Save")
    print("~: Reset")
    print("E: Exit")
    print()

def printStats():
    print()
    print("Your Stats:")
    for i in inv["stats"]:
        print(i.capitalize() + ":", inv["stats"][i],  "GBps" if i == "bandwidth" else "")

def printBlank(num):
    if isinstance(num, int):
        for i in range(num):
            print()

def save(false):
    with open(save_name, 'w') as fp:
        json.dump(inv, fp)
        if false:
            print()
            print("Save Successful")
            print()

def load():
    global curr_date
    if os.path.isfile(save_name):
        with open(save_name) as fp:
            data = json.load(fp)
            if data:
                print("Load Successful")
                curr_date += timedelta(days=data["day"])
                for i in data:
                    inv[i] = data[i]
    else:
        print("Load file not found. Creating file.")
        save(False)

def doReset():
    print()
    print("Are you absolutly certian you want to reset (All progress will be deleted!)?")
    print("Notice: This will exit the game")
    y_n = str(raw_input("(Y/N): ")).capitalize()
    if y_n == "Y":
        print()
        print("Removing save file...")
        os.remove(save_name)
        print("Cleaning Up...")
        isGame = False
        print("Exiting...")
        exit()

def switch(thing):
    if thing == "T":
        travel()
    elif thing == "#":
        save(True)
    elif thing == "E":
        exitGame()
    elif thing == "~":
        doReset()
    if need_bandwidth:
        if thing == "C":
            call_isp()

def exitGame():
    isGame = False
    save(True)
    exit()

def call_isp():
    printBlank(2)
    print("Calling Bell Canada at ")

def invControl(what, amount, mode = "add"):
    if mode == "subtract":
        inv[what] -= amount
    elif mode == "add":
        inv[what] += amount
    elif mode == "double":
        inv[what] *= 2
    elif mode == "half":
        inv[what] /= 2

def doAction(action, amount, doReturn = True):
    if isinstance(action, list):
        what = action[0].lower()
        much = action[1].lower()
        mode = "add"
        if much == "half":
            amount /= 2
        elif much == "none":
            amount = 0
        elif much == "inc":
            amount += random.randrange(maxGain)
        invControl(what, amount, mode)

        if doReturn:
            return amount
    else:
        return False

def healthCheck():
    for i in inv["stats"]:
        if inv["stats"][i] <= 0:
            print()
            if i == "health":
                print("You died due to the lack of health.")
                print()
                print("Start the game and reset to try again.")
                exitGame()
                print False
            elif i == "thirst":
                print("You died due to the lack of proper hydration")
                print()
                print("Start the game and reset to try again.")
                exitGame()
                return False
            elif i == "bandwidth":
                print("You ran out of bandwidth. Call you ISP to get more.")
                return 5
    return True

def dayTick(event = False):
    for i in inv["stats"]:
        amount = random.randint(limits["deduct_min"][i], limits["deduct_max"][i])
        if isinstance(event, str):
            if event == "battle":
                amount *= 3
        inv["stats"][i] -= amount
        print("You used", amount, "of", i.capitalize())

def travel():
    global curr_date

    kilo = random.randint(maxTravel["user"]["min"], maxTravel["user"]["max"])
    amount = random.randint(maxTravel["user"]["min"], maxTravel["user"]["max"])
    kilo_hater = random.randint(maxTravel["haters"]["min"], maxTravel["haters"]["max"])
    _local = senarios["travel"][random.randrange(1, len(senarios["travel"]))]

    printBlank(7)
    print(_local["message"])

    amount = doAction(_local["special"].split("|"), amount)

    if (_local["special"].split("|")[0] == "kilometres" and _local["special"].split("|")[1] == "none"):
        kilo = 0

    if _local["type"] is not "kilometres":
        print(senarios["general"]["travel"].format(amount = kilo))
        inv["kilometres"] -= kilo

    print(_local["gained"].format(amount = amount))
    print(senarios["general"]["haters"].format(amount = kilo_hater))
    printBlank(3)

    curr_date += timedelta(days=1)
    inv["day"] += 1
    inv["haters_back"] = kilo_hater

    dayTick(_local["event"])
    printStats()
    healthCheck()
    printMenu()

def gameRunner():
    while (isGame):
        what = str(raw_input("What would you like to do?: ")).capitalize()
        switch(what)

init()
exit()
