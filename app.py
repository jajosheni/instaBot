### only for personal use
### AUTHOR: http://github.com/jajosheni
### Instagram BOT

import getpass
import sys
from InstagramAPI import InstagramAPI
import time
import random
import _thread


def login():
    username = input('instabot> Username: ')
    password = getpass.getpass('instabot> Password: ')

    print("Connecting...")
    global api
    api = (InstagramAPI(username, password))
    if (api.login()):
        print("Login successful.")
    else:
        print("Cannot login, please check your credentials.")
        login()


def peoplefollowingme():
    followers = []
    next_max_id = ''
    print("Scanning followers...")
    while 1:
        api.getUserFollowers(api.username_id, next_max_id)
        temp = api.LastJson

        for item in temp["users"]:
            followers.append(item)

        try:
            next_max_id = temp["next_max_id"]
        except:
            print("Followers scanned.")

            for follow in followers:
                followersID.append(follow["pk"])
                this_p = [follow["pk"], follow["username"]]
                followerslonglist.append(this_p)
            return


def peopleifollow():
    following = []
    next_max_id = ''
    print("Scanning followings...")
    while 1:
        api.getUserFollowings(api.username_id, next_max_id)
        temp = api.LastJson

        for item in temp["users"]:
            following.append(item)

        try:
            next_max_id = temp["next_max_id"]
        except:
            print("Followings scanned.")

            for follow in following:
                followingID.append(follow["pk"])
                this_p = [follow["pk"], follow["username"]]
                followinglonglist.append(this_p)
            return


def peoplenotfollowingme(fo_ing, fo_ers):
    exclude = set(fo_ers)
    new_list = [x for x in fo_ing if x not in exclude]
    for account in new_list:
        unfollowersID.append(account)
    return


def unfollowlist(ulist):
    i = 0
    print("Unfollowing list...")
    for account in ulist:
        try:
            printusername(account)
            api.unfollow(account)
            i = i+1
            if "Please wait" in str(api.LastJson):
                print("Can't unfollow, please wait a few minutes before you try again")
                return i
        except:
            print("Can't unfollow, please try later")
            return i
    print("Done.")
    return i


def deleteunfollowers():
    if(len(unfollowersID)==0):
        print("No unfollowers")
    else:
        print("{0} people unfollowed".format(unfollowlist(unfollowersID)))


def updatelists():
    followersID.clear()
    followingID.clear()
    unfollowersID.clear()
    peoplefollowingme()
    peopleifollow()
    peoplenotfollowingme(followingID,followersID)


def showstats():
    print("{0} followers".format(len(followersID)))
    print("{0} following".format(len(followingID)))
    print("{0} unfollowing".format(len(unfollowersID)))

def printusername(idnumber):
    for i in range(0, len(followinglonglist) - 1):
        if idnumber == followinglonglist[i][0]:
            print(str(followinglonglist[i][0]) + " : " + str(followinglonglist[i][1]))


def savefiles():
    try:
        followersfile = open("followers.txt", "w")
        for p in followersID:
            followersfile.write(str(p))
            followersfile.write("\n")
    except:
        print("Cannot create file.")

def followhashtaglist():
    print("Insert how many hashtags(max 9) you want to follow:")
    tagno = input('instabot> ')
    taglist = []
    if tagno.isnumeric():
        if int(tagno)>9 or int(tagno)<0:
            print("Max value should be between 1 and 9.")
        else:
            for i in range (1, int(tagno)+1, 1):
                taglist.append(input('{0}. hashtag: #'.format(i)))
            for eachtag in taglist:
                followpeoplebyhashtag("thread", eachtag)
    else:
        print("Please enter a numeric value")


def followpeoplebyhashtag(threadName, hashtag):
    total = 0
    print("Scanning: #{0}".format(hashtag))
    api.getHashtagFeed(hashtag)

    try:
        for eachJsonObject in api.LastJson['items']:
            postuserID = eachJsonObject['caption']['user_id']
            postID = eachJsonObject['caption']['media_id']
            userName = eachJsonObject['caption']['user']['username']

            if(checkTarget(postuserID)):
                api.follow(postuserID)
                this_p = [postuserID, userName]
                followinglonglist.append(this_p)
                api.like(postID)
                time.sleep(random.randint(1,3))
                print("Followed {0}".format(userName))
                total = total+1

    except:
        print(" ")
    print("Followed {0} accounts...".format(total))


def likePosts():
    posts = 0
    print("Liking Posts from Feed...")
    for i in range (0,5,1):
        api.timelineFeed()
        try:
            for eachJsonObject in api.LastJson['items']:
                postID = eachJsonObject['caption']['media_id']
                if not eachJsonObject['has_liked']:
                    api.like(postID)
                    posts = posts+1
                    time.sleep(random.randint(2,8))
        except:
            print(".", end='')
    print("\nLiked {0} picture(s).".format(posts))


def checkTarget(u_id):

    api.getUsernameInfo(u_id)
    for i in range(0, len(followinglonglist) - 1):
        if u_id == followinglonglist[i][0]:
            return False
    try:
        flr = api.LastJson['user']['follower_count']
        flng = api.LastJson['user']['following_count']
        if flr > 1500 or flng > 1500:
            return False
        if (flr - flng > 600):
            return False
        if (flr/flng>4):
            return False
        return True
    except:
        return False

def checkTime(timevalue, minim, maxim):
    ct = time.time()
    if(ct-timevalue > minim):
        if(ct-timevalue<maxim):
            return True
    return False

def start():
    helper()
    while 1:
        cmd = input('instabot> ')
        if cmd == 'exit':
            print("Shutting down bot...")
            savefiles()
            api.logout()
            sys.exit()
        if cmd == "hashtag":
            try:
                _thread.start_new_thread(followpeoplebyhashtag, ("thread1", (input('hashtag: '))))
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            print("instabot> ")
            continue
        if cmd == "hashtaglist":
            followhashtaglist()
            continue
        if cmd == 'randomlike':
            likePosts()
            continue
        if cmd == 'refresh':
            updatelists()
            continue
        if cmd == 'stats':
            showstats()
            continue
        if cmd == 'unfollow':
            deleteunfollowers()
            continue
        if cmd == 'help':
            helper()
            continue
        if cmd == 'changeuser':
            api.logout()
            login()
            updatelists()
            continue
        else:
            print("Command unrecognized, type 'help' to bring up the help menu.")

def helper():
    print("-------------------------------------------------")
    print("-------------------------------------------------")
    print("refresh\t\t-\t Refresh lists")
    print("stats\t\t-\t Show stats")
    print("hashtag\t\t-\t Follow people based on a hashtag")
    print("hashtaglist\t-\t Follow people based on a hashtag list")
    print("randomlike\t-\t Like posts from people you follow")
    print("unfollow\t-\t Unfollow all unfollowers")
    print("changeuser\t-\t Change the user")
    print("exit\t\t-\t Shut down the bot")
    print("help\t\t-\t Show this menu on the screen")
    print("-------------------------------------------------")
    print("-------------------------------------------------")



#### MAIN

### SET LISTS

followersID = []
followingID = []
unfollowersID = []

followerslonglist = []
followinglonglist = []

### RUN

login()
updatelists()
start()
