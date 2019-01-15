### only for personal use
### AUTHOR: jajosheni.github.io
### Instagram BOT

import sys
from InstagramAPI import InstagramAPI
import time
import random
import _thread
import getpass
import os

def printart():
    art =[
        " .              +   .                .   . .     .  .",
        "                   .                    .       .     *",
        "  .       *                        . . . .  .   .  + .",
        "            'You Are Here'            .   .  +  . . .",
        ".                 |             .  .   .    .    . .",
        "                  |           .     .     . +.    +  .",
        "                 \|/              .       .   . .",
        "        . .       V          .    * . . .  .  +   .",
        "           +      .           .   .      +     .",
        "                            .       . +  .+. .",
        "  .                      .     . + .  . .     .    .",
        "           .      .    .     . .   . . .           .",
        "      *             .    . .  +    .  .     +      ;",
        "          .     .    .  +   . .  *  .    .    - --<+>- -",
        "               . + .  .  .  .. +  .   .            !",
        ".      .  .  .  *   .  *  . +..  ..                .   *",
        " .      .   . .   .   .   . .  +   .    .          .\n\n"
    ]
    for eachstr in art:
        print(eachstr)


def checkfiles():
    try:
        if not os.path.exists("check.txt"):
            file = open("check.txt", "w")
            file.close()
        if not os.path.exists("followings.txt"):
            file = open("followings.txt", "w")
            file.close()
        if not os.path.exists("whitelist.txt"):
            file = open("whitelist.txt", "w")
            file.close()
    except:
        pass


def login():
    username = input('instabot> Username: ')
    password = getpass.getpass('instabot> Password: ')

    if username=='YOUR_USERNAME' :
        loadfollowfile()

    print("Connecting...")
    global api
    api = (InstagramAPI(username, password))
    if api.login():
        print("Login successful.")
        time.sleep(1)
        os.system("cls")
    else:
        print("Cannot login, please check your credentials.")
        login()


def loadfollowfile():
    followingID.clear()
    try:
        followfile = open("followings.txt", "r")
        for eachfollowing in followfile:
            try:
                followingID.append(int(eachfollowing))
            except:
                pass
        followfile.close()
    except:
        print(" ")


def savefiles():
    if api.username=='YOUR_USERNAME':
        try:
            followingfile = open("followings.txt", "r")
            text = []
            for eachitem in followingfile:
                text.append(str(eachitem))
            followingfile.close()
            file = open("followings.txt", "a")
            for p in followingID:
                if not str(p)[:-1] in str(text):
                    file.write(str(p) + "\n")
            file.close()
        except:
            print("Cannot create file.")


def peoplefollowingme():
    try:
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
                if 'none' in str(next_max_id).lower():
                    print("Followers scanned.")

                    for follow in followers:
                        followersID.append(follow["pk"])
                        this_p = [follow["pk"], follow["username"]]
                        followerslonglist.append(this_p)
                    return
            except:
                print("Couldn't get next_max_id.")

    except Exception as e:
        print("couldn't refresh, please try later.")


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
            if 'none' in str(next_max_id).lower():
                print("Followings scanned.")

                for follow in following:
                    followingID.append(follow["pk"])
                    this_p = [follow["pk"], follow["username"]]
                    followinglonglist.append(this_p)
                return
        except:
            print("Couldn't get next_max_id.")


def peoplenotfollowingme(fo_ing, fo_ers):
    exclude = set(fo_ers)
    new_list = [x for x in fo_ing if x not in exclude]
    for account in new_list:
        unfollowersID.append(account)
    return


def whiteListed():
    usernamelist = []
    filex = open("whitelist.txt", "r")
    for eachacc in filex:
        usernamelist.append(str(eachacc)[:-1])
    filex.close()

    for eachwhite in usernamelist:
        for i in range(0, len(followinglonglist) - 1, 1):
            if eachwhite == followinglonglist[i][1]:
                whitelist.append(followinglonglist[i][0])


def unfollowlist(ulist):
    i = 0
    print("Unfollowing list...")
    for account in ulist:
        try:
            printusername(account)
            api.unfollow(account)
            i = i+1
            time.sleep(random.randint(0,2))
            if "Please wait" in str(api.LastResponse):
                print("Can't unfollow, please wait a few minutes before you try again")
                return i
        except:
            print("Can't unfollow, please try later")
            return i
    return i


def showunfollowers():
    for eachunfollow in unfollowersID:
        printusername(eachunfollow)


def deleteunfollowers():
    if len(unfollowersID)==0:
        print("No unfollowers")
    else:
        print("Done. {0} people unfollowed".format(unfollowlist(unfollowersID)))


def deleteList():
    updatelists()
    try:
        checkList = []
        file1 = open("check.txt", "r")
        for eachfollowing in file1:
            try:
                for i in range(0, len(followinglonglist) - 1, 1):
                    if str(eachfollowing[:-1]) in str(followinglonglist[i][1]):
                        checkList.append(followinglonglist[i][0])
            except:
                pass
        file1.close()
        unfollowlist(checkList)
    except Exception as e:
        print(e)


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
        print("{} people followed.".format(indx))
    except Exception as error:
        print("FollowLikers: {0}".format(error))


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
        pass
    print("Followed {0} accounts...".format(total))
    _thread.exit()


def profileFollow(threadName, username):
    loadfollowfile()
    try:
        api.searchUsername(username)
        if api.LastJson['user']['media_count'] == 0:
            print("no media")
            _thread.exit()
            return
        u_id = api.LastJson['user']['pk']
        api.getUserFeed(u_id)
        media_id = api.LastJson['items'][0]['pk']
        followLikers(media_id)
    except:
        pass
    _thread.exit()


def automatic(threadname,h_tag):
    loadfollowfile()
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
                print("...\t\t", end='\r')
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
    _thread.exit()


def likeUserFeed(threadname, u_id):
    try:
        api.getUsernameInfo(u_id)
        isPrivate = api.LastJson['user']['is_private']
        if not isPrivate:
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
        print("...", end='\r')
    _thread.exit()


def likeExplore(threadName, multithread):
    i=0
    next_max=' '

    while i<100:
        api.explore(next_max)
        next_max = api.LastJson['next_max_id']
        for eachJsonObj in api.LastJson['items']:
            try:
                media_id = eachJsonObj['media']['pk']
                if not eachJsonObj['media']['has_liked']:
                    api.like(media_id)
                    i=i+1
                    time.sleep(random.randint(2, 4))
                    print("...\t\t",end = '\r')
            except:
                continue
    print("Liking from explore process ended. {0} pictures liked".format(i))
    _thread.exit()


def likeFeed(threadName, multithread):
    posts = 0
    nextmax = ' '
    print("Liking Posts from Feed", end='\n')
    while posts < 100:
        api.timelineFeed(nextmax)
        nextmax = api.LastJson['next_max_id']

        try:
            for eachJsonObject in api.LastJson['items']:
                postID = eachJsonObject['caption']['media_id']
                if not eachJsonObject['has_liked']:
                    api.like(postID)
                    posts = posts+1
                    time.sleep(random.randint(2,6))
        except:
            print("...\t\t", end='\r')
    print("\nLiked {0} picture(s) from feed.".format(posts))
    _thread.exit()


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
        print("...\t\t", end='\r')
    print("likeHashtag process is over: {0} pictures liked".format(i))
    _thread.exit()


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
                time.sleep(random.randint(10, 20))
    except:
        print("...", end='\r')
    print("commentHashtag process is over: {0} pictures commented".format(i))
    _thread.exit()


def addComment(m_id):
    writestuff = comments[random.randint(0, len(comments) - 1)]

    try:
        api.mediaInfo(m_id)
        #albania coordinates
        lat = float(api.LastJson['items'][0]['location']['lat'])
        lng = float(api.LastJson['items'][0]['location']['lng'])

        if float(19.9) < lng < float(20.8):
            if float(39.6) < lat < float(42.6):
                writestuff = komente[random.randint(0, len(komente) - 1)]
    except:
        pass

    api.comment(m_id, writestuff)


def checkTarget(u_id):

    api.getUsernameInfo(u_id)

    for eachacc in followingID:
        if int(u_id) == eachacc:
            return False

    try:
        flr = api.LastJson['user']['follower_count']
        flng = api.LastJson['user']['following_count']
        if flr > 1500 or flr < 70 or flng > 1500 or flng < 70 :
            return False
        if flr - flng > 600 :
            return False
        if flr/flng > 4 :
            return False
        return True
    except:
        return False


def checkWhitelist(u_id):
    for eachacc in whitelist:
        if int(u_id) == int(eachacc):
            return False

    api.getUsernameInfo(u_id)

    try:
        flr = api.LastJson['user']['follower_count']
        flng = api.LastJson['user']['following_count']

        '''if flr > 1500 or flr < 70 or flng > 1500 or flng < 70:
            return True
        if (flr - flng > 600):
            return True
        if (flr / flng > 4):
            return True'''
        if flng - flr > 60:
            return True
        return False
    except:
        return True


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
                media_points = media_points - 2
        return media_points
    except:
        return 0


def checkThis():
    updatelists()

    filez = open("check.txt", "w")
    for eachitem in followinglonglist:
        if checkWhitelist(eachitem[0]):
                filez.write(str(eachitem[1])+ "\n")
    filez.close()


def closeapp():
    print("Shutting down bot...")
    savefiles()
    api.logout()
    sys.exit()


def updatelists():
    followinglonglist.clear()
    followinglonglist.clear()
    followersID.clear()
    followingID.clear()
    unfollowersID.clear()
    whitelist.clear()
    peoplefollowingme()
    peopleifollow()
    peoplenotfollowingme(followingID,followersID)
    whiteListed()


def showstats():
    print("{0} followers".format(len(followersID)))
    print("{0} following".format(len(followingID)))
    print("{0} unfollowing".format(len(unfollowersID)))


def printusername(idnumber):
    for i in range(0, len(followinglonglist) - 1, 1):
        if idnumber == followinglonglist[i][0]:
            print(str(followinglonglist[i][0]) + "\t:\t" + str(followinglonglist[i][1]))


def start():
    printart()
    print("Type 'help' to see available commands.\n")
    while 1:
        cmd = input('instabot> ')
        cmd = cmd.lower()
        if cmd == 'exit':
            closeapp()
        if cmd == "hashtag":
            try:
                _thread.start_new_thread(followpeoplebyhashtag, ("hashtag", (input('hashtag: '))))
                print("hashtag started on another thread.")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            continue
        if cmd == 'feedlike':
            try:
                _thread.start_new_thread(likeFeed, ("feedlike", "thread1"))
                print("feedlike started on another thread.")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            continue

        if cmd == 'explorelike':
            try:
                _thread.start_new_thread(likeExplore, ("explorelike", "thread1"))
                print("explorelike started on another thread.")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            continue
        if cmd == 'likehashtag':
            try:
                _thread.start_new_thread(likeHashtag, ("thread1", (input('hashtag: '))))
                print("likehashtag started on another thread.")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
            continue
        if cmd == 'commenttag':
            try:
                _thread.start_new_thread(commentHashtag, ("comment", (input('hashtag: '))))
                print("commenttag started on another thread.")
            except Exception as error:
                print("Error: unable to start thread\n{0}".format(error))
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
        if cmd == 'profile':
            _thread.start_new_thread(profileFollow, ("profile", (input('username: '))))
            continue
        if cmd == 'unfollow':
            deleteunfollowers()
            continue
        if cmd == 'unfollowers':
            showunfollowers()
            continue
        if cmd == 'help':
            helper()
            continue
        if cmd == 'clear':
            os.system('cls')
            printart()
            continue
        if cmd == 'check':
            checkThis()
            continue
        if cmd == 'deletelist':
            deleteList()
            continue
        if cmd == 'changeuser':
            api.logout()
            login()
            updatelists()
            continue
        if cmd == '?':
            print("check, deletelist")
            continue
        if cmd == '':
            pass
        else:
            print("Command unrecognized, type 'help' to bring up the help menu.")


def helper():
    print("---------------------------------------------------------------------")
    print("---------------------------------------------------------------------")
    print("refresh\t\t-   Refresh lists")
    print("stats\t\t-   Show stats")
    print("unfollow\t-   Unfollow all unfollowers")
    print("unfollowers\t-   Show all unfollowers")
    print("---------------------------------------------------------------------")
    print("hashtag\t\t-   Follow people based on a hashtag")
    print("feedlike\t-   Like posts from people you follow")
    print("explorelike\t-   Like posts from explore page")
    print("likehashtag\t-   Like posts from a hashtag")
    print("commenttag\t-   Comment posts from a hashtag")
    print("automatic\t-   Auto-follows likers of a smartly chosen picture")
    print("profile\t\t-   Auto-follow likers of last pic of an account")
    print("---------------------------------------------------------------------")
    print("changeuser\t-   Change the user")
    print("exit\t\t-   Shut down the bot")
    print("clear\t\t-   Clear the console screen")
    print("help\t\t-   Show this menu on the screen")
    print("?")
    print("---------------------------------------------------------------------")
    print("---------------------------------------------------------------------")


#### MAIN

printart()
checkfiles()

comments = [
    "👏 great jooob!",
    "Awesomeeee 👌👌",
    "Beautifuuul 😍😍",
    "Superb!",
    "Sooo nice 👌",
    "👏 marvellous",
    "Awesome feed, keep it up! I would love it if you visited my page too. 📷📸✔",
    "good pic 👍",
    "Such a nice composition 👏",
    "Perfect! 😎😍",
    "Super pic 🤟🤘",
    "Wow 😎",
    "This rocks 🤟🤘"
]

komente = [
    "Super foto 👏",
    "Kendshem 👌",
    "Sa bukur 👌",
    "Perfekt 😎😍",
    "Sooo nice 🤟🤘",
    "Profil plot gjalleri, sigurohu qe te vizitosh dhe faqen time gjithashtu. 📷📸✔",
    "Kompozicion interesant 👌",
]

hashtagQuality = [
    "photography", "art", "landscape",
    "photooftheday", "canon", "nikon",
    "olympus", "camera", "travel",
    "waves", "sea", "sunset",
    "picoftheday", "nature", "composition",
    "autumn", "travelgram", "traveltheworld",
    "longexposure", "milky", "stars",
    "earth", "albania"
]

bannedHashtags = [
    "likeforfollow", "followforfollow", "like4follow", "follow4follow"
    "likeforlike", "like4like", "followers", "lfl", "fff", "lff", "ffl",
    "followme", "follow", "autofollow", "autolike", "peach", "sexy", "hot",
    "sexymom", "ass", "tattoedgirl", "nude", "boobs", "boobies", "model",
    "blonde", "victoriasecret", "lingerie", "legs", "bootie", "booty",
    "makeup", "fitness", "coachella", "cosmetics", "makeuptutorial", "serbia",
    "politican", "edirama", "rilindja", "erioveliaj"
]

### SET LISTS

followersID = []
followingID = []
unfollowersID = []

followerslonglist = []
followinglonglist = []

whitelist = []

### RUN

login()
start()
