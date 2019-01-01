from PIL import Image
from InstagramAPI import InstagramAPI
import time
import random
import _thread
import sys
import requests
from pathlib import Path


def login():
    username = input('username> ')
    password = input('password> ')

    print("Connecting...")
    global api
    api = (InstagramAPI(username, password))
    if api.login():
        print("Login successful.")
    else:
        print("Cannot login, please check your credentials.")
        login()

def spamhashtag(hashtag, spam):
    api.getHashtagFeed(hashtag)
    i=0
    try:
        for eachJsonObject in api.LastJson['items']:
            media_id = eachJsonObject['caption']['media_id']
            if not eachJsonObject['has_liked']:
                api.like(media_id)
                api.comment(media_id, spam)
                i = i + 1
            time.sleep(random.randint(20, 40))

    except:
        print(" ",end='')
        print("\t\tcomment Bot process over:\n {0} pictures commented".format(i))
        _thread.exit()


def profpic(u_name):
    try:
        api.searchUsername(u_name)
        user = api.LastJson['user']

        item = user['hd_profile_pic_versions']
        for eachit in item:
            print(str(eachit['height']) + " x " + str(eachit['width']))
            print(eachit['url'])
            print(str(user['hd_profile_pic_url_info']['height']) + " x " + str(user['hd_profile_pic_url_info']['width']))
            url_ = user['hd_profile_pic_url_info']['url']
            print(url_)

        Picture_request = requests.get(url_)
        home = str(Path.home())
        path_i= home + "\\Desktop\\temp.jpg"

        if Picture_request.status_code == 200:
            with open(path_i, 'wb') as f:
                f.write(Picture_request.content)
            hd_image = Image.open(path_i)
            Image._show(hd_image)

    except Exception as e:
        print("try again")
        print(str(e))



def start():
    while 1:
        cmd = input('instabot> ')
        if cmd == 'spam':
            try:
                _thread.start_new_thread(spamhashtag, (input('hashtag: '), input('spam: ')))
                print("spam started on another thread;\n you can continue using the program")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
        elif cmd == 'profpic':
                profpic(input('username: '))
        elif cmd == 'exit':
            api.logout()
            print("quiting...")
            sys.exit()
        else:
            print("Command unknown")



#RUN
login()
start()
