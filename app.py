### only for personal use
### AUTHOR: github.com/jajosheni
### instaBot v2.1.1

import sys
from InstagramAPI import InstagramAPI
import time
import random
import _thread
import getpass
import os

def login():
    username = input('instabot> Username: ')
    password = getpass.getpass('instabot> Password: ')

    print("Connecting...")
    global api
    api = (InstagramAPI(username, password))
    if api.login():
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
    if len(unfollowersID)==0:
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
    for i in range(0, len(followinglonglist) - 1, 1):
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

            if checkTarget(postuserID):
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


def likeUserFeed(threadname, u_id):
    try:
        api.getUserFeed(u_id)
        feed = api.LastJson['items']
        howmanyposts = api.LastJson['num_results']
        if howmanyposts > 0:
            for i in range(0, howmanyposts, 1):
                if i == 3:
                    return
                media_id = feed[i]['pk']
                if not feed[i]['has_liked']:
                    api.like(media_id)
                    if i == 0:
                        addComment(media_id)
                    time.sleep(random.randint(1,3))
    except:
        print(" ", end='')

def addComment(m_id):
    writestuff = comments[random.randint(0, len(comments) - 1)]
    api.comment(m_id, writestuff)

def followLikers(m_id):
    try:
        print("Media Info:")
        api.mediaInfo(m_id)
        item = api.LastJson['items'][0]
        pub_time = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(item['caption']['created_at']))
        print("Published on: {0}".format(pub_time))
        print("{0} likes".format(item['like_count']))
        print("User: {0}".format(item['user']['username']))

        print("Loading likers...")
        api.getMediaLikers(m_id)
        indx=1
        for eachUser in api.LastJson['users']:
            pk=eachUser['pk']
            user_name=eachUser['username']
            if checkTarget(pk):
                api.follow(pk)
                _thread.start_new_thread(likeUserFeed, ("likeuserfeed",pk))
                print("{0}. ".format(indx),end='')
                print("{0}".format(user_name))
                indx=indx+1
                time.sleep(random.randint(5,10))
    except Exception as error:
        print("FollowLikers: {0}".format(error))

def likeExplore(threadName, multithread):
    api.explore()
    i=0
    for eachJsonObj in api.LastJson['items']:
        try:
            media_id = eachJsonObj['media']['pk']
            if not eachJsonObj['media']['has_liked']:
                api.like(media_id)
                i=i+1
                time.sleep(random.randint(2, 4))
                print(".",end = '')
        except:
            continue
    print("Liking from explore process ended. {0} pictures liked".format(i))

def likeFeed(threadName, multithread):
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
            print("*", end='')
    print("\nLiked {0} picture(s) from feed.".format(posts))

def commentHashtag(threadName, hashtag):
    api.getHashtagFeed(hashtag)
    i=0
    try:
        for eachJsonObject in api.LastJson['items']:
            media_id = eachJsonObject['caption']['media_id']

            if checkMedia("comment", media_id, 0, 50):
                if not eachJsonObject['has_liked']:
                    api.like(media_id)
                    addComment(media_id)
                    i=i+1
                time.sleep(random.randint(10, 30))
    except:
        print(" ",end='')
        print("commentHashtag process is over: {0} pictures commented".format(i))


def likeHashtag(threadName, hashtag):
    api.getHashtagFeed(hashtag)
    i =0
    try:
        for eachJsonObject in api.LastJson['items']:
            media_id = eachJsonObject['caption']['media_id']

            if checkMedia("like", media_id, 0, 1000):
                if not eachJsonObject['has_liked']:
                    api.like(media_id)
                    i=i+1
                    time.sleep(random.randint(3, 6))
    except:
        print(".",end='')
    print("likeHashtag process is over: {0} pictures liked".format(i))


def automatic(threadname,h_tag):
    try:
        api.getHashtagFeed(h_tag)
        media_array = []
        j=0

        print("Loading Media...")

        for eachJsonObject in api.LastJson['items']:
            try:
                media_id = eachJsonObject['caption']['media_id']
                if checkMedia("like", media_id, 200, 1000):
                    this_media = [media_id, checkQuality(media_id)]
                    media_array.append(this_media)
                    j = j + 1
            except TypeError:
                print("...", end='')
                continue

        print("{0} pictures choosed".format(j))
        maxpoint = media_array[0][1]
        chosenID = media_array[0][0]
        print("Media loaded, selecting the best choice...")
        for i in range(0, j, 1):
            if maxpoint < media_array[i][1]:
                chosenID = media_array[i][0]
                maxpoint = media_array[i][1]
        print("Chosen Media: {0} points".format(maxpoint))
        followLikers(chosenID)
        print("Automatic: done\ninstabot> ")
    except Exception as error:
        print("Automatic-error: {0}".format(error))




def checkTarget(u_id):

    api.getUsernameInfo(u_id)
    for i in range(0, len(followinglonglist) - 1,1):
        if u_id == followinglonglist[i][0]:
            return False
    try:
        flr = api.LastJson['user']['follower_count']
        flng = api.LastJson['user']['following_count']
        if flr > 1500 or flr <70 or flng > 1500 or flng <70:
            return False
        if (flr - flng > 600):
            return False
        if (flr/flng>4):
            return False
        return True
    except:
        return False

def checkMedia(threadName,m_id,minim,maxim):
    try:
        api.mediaInfo(m_id)
        item = api.LastJson['items'][0]
        post_like = int(item['like_count'])
        post_comment = int(item['comment_count'])
        if threadName == "like":
            if post_like in range(minim, maxim):
                return True
        if threadName == "comment":
            if post_comment in range(minim, maxim):
                return True
    except:
        print(" ")

    return False


def checkTime(timevalue, minim, maxim):
    ct = time.time()
    if ct-timevalue in range (minim, maxim):
            return True
    return False

def checkQuality(m_id):
    api.mediaInfo(m_id)
    try:
        media_points = 0
        description = api.LastJson['items'][0]['caption']['text']
        for eachHashtag in hashtagQuality:
            if eachHashtag in description:
                media_points = media_points + 1
        for eachHashtag in bannedHashtags:
            if eachHashtag in description:
                media_points = media_points - 1
        return media_points
    except:
        print(" ", end='')
        return 0

def closeapp():
    print("Shutting down bot...")
    savefiles()
    api.logout()
    sys.exit()

def start():
    helper()
    while 1:
        cmd = input('instabot> ')
        if cmd == 'exit':
            closeapp()
        if cmd == "hashtag":
            try:
                _thread.start_new_thread(followpeoplebyhashtag, ("hashtag", (input('hashtag: '))))
                print("hashtag started on another thread, you can continue using the program")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            print("instabot> ")
            continue
        if cmd == "hashtaglist":
            followhashtaglist()
            continue
        if cmd == 'feedlike':
            try:
                _thread.start_new_thread(likeFeed, ("feedlike", "thread1"))
                print("feedlike started on another thread, you can continue using the program")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            print("instabot> ")
            continue
        if cmd == 'explorelike':
            try:
                _thread.start_new_thread(likeExplore, ("explorelike", "thread1"))
                print("explorelike started on another thread, you can continue using the program")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            print("instabot> ")
            continue
        if cmd == 'likehashtag':
            try:
                _thread.start_new_thread(likeHashtag, ("thread1", (input('hashtag: '))))
                print("likehashtag started on another thread, you can continue using the program")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            print("instabot> ")
            continue
        if cmd == 'commenttag':
            try:
                _thread.start_new_thread(commentHashtag, ("comment", (input('hashtag: '))))
                print("commenttag started on another thread, you can continue using the program")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            print("instabot> ")
            continue
        if cmd == 'refresh':
            updatelists()
            continue
        if cmd == 'stats':
            showstats()
            continue
        if cmd == 'automatic':
            _thread.start_new_thread(automatic, ("automatic", (input('hashtag: '))))
            continue
        if cmd == 'unfollow':
            deleteunfollowers()
            continue
        if cmd == 'help':
            helper()
            continue
        if cmd == 'sys':
            os.system(input('Console: '))
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
    print("unfollow\t-\t Unfollow all unfollowers")
    print("-------------------------------------------------")
    print("hashtag\t\t-\t Follow people based on a hashtag")
    print("hashtaglist\t-\t Follow people based on a hashtag list")
    print("feedlike\t-\t Like posts from people you follow")
    print("explorelike\t-\t Like posts from explore page")
    print("likehashtag\t-\t Like posts from a hashtag")
    print("commenttag\t-\t Comment posts from a hashtag")
    print("automatic\t-\t Automatically follows all likers of a picture chosen by a smart algorithm")
    print("-------------------------------------------------")
    print("changeuser\t-\t Change the user")
    print("exit\t\t-\t Shut down the bot")
    print("help\t\t-\t Show this menu on the screen")
    print("-------------------------------------------------")
    print("-------------------------------------------------")



#### MAIN

comments = [
    "Awesome feed, keep it up! I would love it if you visited my page too. 🤩",
    "Great job! 👏👏",
    "Awesomeeee 👌👌",
    "Beautiful 😍😍",
    "Nice pictures, it would be awesome if you could check out my page. 😁😎🤗",
    "Like my comment, for no reason, be sure to check my feed too 😂😂😅 ",
    "Superb!",
    "Sooo nice 👌",
    "👏 marvelous",
    "This is beautiful, checkout my gallery too, i have some nice shots 📷📸✔"
]

hashtagQuality = [
    "photography", "art", "landscape",
    "photooftheday", "canon", "nikon",
    "olympus", "camera", "travel",
    "instagood", "sea", "sunset",
    "picoftheday", "nature", "composition",
    "autumn", "travelgram", "traveltheworld"
]

bannedHashtags = [
    "likeforfollow", "followforfollow", "like4follow", "follow4follow"
    "likeforlike", "like4like", "followers", "lfl", "fff", "lff", "ffl",
    "followme", "follow", "autofollow", "autolike", "peach", "sexy", "hot",
    "sexymom", "ass", "tattoedgirl", "nude", "boobs", "boobies", "model",
    "blonde", "victoriasecret", "lingerie", "legs", "bootie", "booty"
]

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

