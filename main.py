from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from upcoming.steam.steam_main import steam_upcoming
from upcoming.playstation.playstation_main import playstation_upcoming
from upcoming.xbox.xbox_main import xbox_upcoming
from upcoming.switch.switch_main import switch_upcoming

from core.Webdriver import Webdriver
from core.database.Database import Database
from core.data.dataInsert import dataInsert
from core.notification.push_notification import send_message


import time

# ---Init---
db = Database()
wd = Webdriver()

# ---Start driver---
wd.startDriver()

# ---Collection---
steam_upcoming()
playstation_upcoming()
xbox_upcoming()
switch_upcoming()

# ---Quit driver---
wd.quitDriver()

# ---Upload---
dataInsert()
db.transferMongo()

# ---Push Notification---
send_message()




