
from InstagramAPI import InstagramAPI
import time
import random
import _thread

def login():
    username = input('instabot> Username: ')
    password = input('instabot> Password: ')

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
            time.sleep(random.randint(10, 30))

    except:
        print(" ",end='')
        print("comment Bot process over: {0} pictures commented".format(i))

def start():
    while 1:
        cmd = input('instabot> ')
        if cmd == 'spam':
            try:
                _thread.start_new_thread(spamhashtag, (input('hashtag: '), input('spam: ')))
                print("spam started on another thread, you can continue using the program")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
        else:
            print("command unknown")



#RUN
login()
start()
