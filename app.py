"""
###    only for personal use
###    AUTHOR: github.com/jajosheni
###    Instagram BOT
"""

import sys
from InstagramAPI import InstagramAPI
import time
import random
import _thread
import getpass
import os

YOUR_USERNAME = 'PUT_YOUR_USERNAME_HERE'


def printart():
    art = [
        " .              +   .                .   . .     .  .",
        "                   .                    .       .     *",
        "  .       *                        . . . .  .   .  + .",
        "            'You Are Here'            .   .  +  . . .",
        ".                 |             .  .   .    .    . .",
        "                  |           .     .     . +.    +  .",
        "                 \\|/              .       .   . .",
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
    except Exception as error:
        print(str(error))


def login():
    username = input('instabot> Username: ')
    password = getpass.getpass('instabot> Password: ')

    if username == YOUR_USERNAME:
        loadfollowfile()

    print("Connecting...")
    global api
    api = (InstagramAPI(username, password))
    if api.login():
        print("Login successful.")
        api.getSelfUsernameInfo()
        user = api.LastJson['user']
        global followers_count, following_count
        followers_count = user['follower_count']
        following_count = user['following_count']
        time.sleep(0.5)
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
        pass


def savefiles():
    if api.username == YOUR_USERNAME:
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


def progressbar(percentage, info=''):

    if percentage > float(0.99):
        percentage = 1.0
    percent = 100 * percentage

    if percent > 2:
        percent /= 2

    percent = int(percent) + 1
    perstr = "█"
    for _ in range(percent):
        perstr += "█"

    print("%{:.2f} {}{:51.51}{} {:17.17}".format(percentage*100, "[", perstr, "]", info), end='\r')


def peoplefollowingme():
    try:
        progressbar(0, 'Followers')
        i = 0
        followers = []
        next_max_id = ''
        while 1:
            api.getUserFollowers(api.username_id, next_max_id)
            temp = api.LastJson

            for item in temp["users"]:
                followers.append(item)
                i += 1
                progressbar(i / followers_count, str(i) + ' Followers')

            try:
                next_max_id = temp["next_max_id"]
                if 'none' in str(next_max_id).lower():
                    print("\n")
                    for follow in followers:
                        followersID.append(follow["pk"])
                        this_p = [follow["pk"], follow["username"]]
                        followerslonglist.append(this_p)
                    return
            except Exception as e:
                print("Couldn't get next_max_id." + str(e))
    except:
        print("couldn't refresh, please try later.")


def peopleifollow():
    try:
        progressbar(0, 'Followings')
        i = 0
        following = []
        next_max_id = ''
        while 1:
            api.getUserFollowings(api.username_id, next_max_id)
            temp = api.LastJson

            for item in temp["users"]:
                following.append(item)
                i += 1
                progressbar(i / following_count, str(i) + ' Followings')

            try:
                next_max_id = temp["next_max_id"]
                if 'none' in str(next_max_id).lower():
                    print("\n")
                    for follow in following:
                        followingID.append(follow["pk"])
                        this_p = [follow["pk"], follow["username"]]
                        followinglonglist.append(this_p)
                    return
            except:
                print("Couldn't get next_max_id.")
    except:
        print("couldn't refresh, please try later.")


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
            api.unfollow(account)
            i += 1
            progressbar(i/len(ulist), getusername(account))
            time.sleep(random.randint(0, 2))
            if "Please wait" in str(api.LastResponse):
                print("Can't unfollow, please wait a few minutes before you try again")
                return i
        except Exception as e:
            print("\nCan't unfollow, please try later")
            return i
    print('\n')
    return i


def showunfollowers():
    for eachunfollow in unfollowersID:
        printusername(eachunfollow)


def deleteunfollowers():
    if len(unfollowersID) == 0:
        print("No unfollowers")
    else:
        print("\n Done. {0} people unfollowed\n".format(unfollowlist(unfollowersID)))


def deleteList():
    updatelists()
    try:
        checklist = []
        file1 = open("check.txt", "r")
        for eachfollowing in file1:
            try:
                for i in range(0, len(followinglonglist) - 1, 1):
                    if str(eachfollowing[:-1]) in str(followinglonglist[i][1]):
                        checklist.append(followinglonglist[i][0])
            except:
                pass
        file1.close()
        unfollowlist(checklist)
    except Exception as e:
        print(e)


def followLikers(m_id):
    try:
        i = 0
        print("Loading likers...")
        api.getMediaLikers(m_id)
        likers = api.LastJson['user_count']
        print("{} Likers".format(likers))
        indx = 1
        for eachUser in api.LastJson['users']:
            i += 1
            pk = eachUser['pk']
            user_name = eachUser['username']
            progressbar(i / likers)
            if checkTarget(pk):
                progressbar(i / likers, str(indx) + ". " + str(user_name))
                api.follow(pk)
                _thread.start_new_thread(likeUserFeed, ("likeuserfeed", pk))
                indx = indx+1
                time.sleep(random.randint(5, 15))
        print("{} people followed.".format(indx))
    except Exception as error:
        print("FollowLikers: {}".format(error))


def followpeoplebyhashtag(threadName, hashtag):
    total = 0
    print("Scanning: #{}".format(hashtag))
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
                time.sleep(random.randint(1, 3))
                print("Followed {0}".format(userName))
                total = total+1

    except:
        pass

    print("Followed {} accounts.".format(total))
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


def automatic(threadname, h_tag):
    loadfollowfile()
    try:
        api.getHashtagFeed(h_tag)
        media_array = []
        j = 0

        selectedindex = 0

        print("Loading Media...")

        for eachJsonObject in api.LastJson['items']:
            try:
                media_id = str(eachJsonObject['caption']['media_id'])
                pub_time = int(eachJsonObject['taken_at'])
                owner = str(eachJsonObject['caption']['user']['username'])
                if checkMedia("like", eachJsonObject, 200, 1000):
                    this_media = [media_id, checkQuality(eachJsonObject), pub_time, owner]
                    media_array.append(this_media)
                    j = j + 1
            except TypeError:
                pass

        print("{} pictures choosed".format(j))
        maxpoint = media_array[0][1]
        print("Media loaded, selecting the best choice...")
        for i in range(0, j, 1):
            if maxpoint < media_array[i][1]:
                maxpoint = media_array[i][1]
                selectedindex = i

        print("Chosen Media: {0} points".format(media_array[selectedindex][1]))
        print("Published on: {0}".format(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(media_array[selectedindex][2])))))
        print("By: {}".format(media_array[selectedindex][3]))
        followLikers(media_array[selectedindex][0])
        print("Automatic: done\ninstabot> ")
    except Exception as error:
        print("Automatic: {}".format(error))
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
                    if i == 3:  # break out of the funct after the first 3 posts
                        return
                    media_id = feed[i]['pk']
                    if not feed[i]['has_liked']:
                        api.like(media_id)
                        if i == 0:
                            addComment(media_id, feed[i])
                        time.sleep(random.randint(1, 3))
    except:
        pass
    _thread.exit()


def likeExplore(threadName, multithread):
    i = 0
    next_max = ' '
    print("Liking Posts from Explore", end='\n')
    while i < 100:
        api.explore(next_max)
        next_max = api.LastJson['next_max_id']
        for eachJsonObj in api.LastJson['items']:
            try:
                media_id = eachJsonObj['media']['pk']
                if not eachJsonObj['media']['has_liked']:
                    api.like(media_id)
                    i = i + 1
                    time.sleep(random.randint(2, 4))
                    print("...\t\t", end='\r')
                progressbar(i/100, "Like Explore Pics")
            except:
                pass
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
                    time.sleep(random.randint(2, 6))
                progressbar(posts/100, "Liking Feed")
        except:
            pass
    print("\nLiked {0} picture(s) from feed.".format(posts))
    _thread.exit()


def likeHashtag(threadName, hashtag):
    print("Liking Posts #" + str(hashtag), end='\n')
    api.getHashtagFeed(hashtag)
    i = 0
    total = len(api.LastJson['items'])
    try:
        for eachJsonObject in api.LastJson['items']:
            media_id = eachJsonObject['caption']['media_id']

            if checkMedia("like", eachJsonObject, 0, 1000):
                if not eachJsonObject['has_liked']:
                    api.like(media_id)
                    i = i+1
                    time.sleep(random.randint(3, 6))
            progressbar(i / total, "Like #" + str(hashtag))
    except:
        pass
    print("likeHashtag process is over: {0} pictures liked".format(i))
    _thread.exit()


def commentHashtag(threadName, hashtag):
    print("Commenting Posts #" + str(hashtag), end='\n')
    api.getHashtagFeed(hashtag)
    i = 0
    total = len(api.LastJson['items'])
    try:
        for eachJsonObject in api.LastJson['items']:
            media_id = eachJsonObject['caption']['media_id']

            if checkMedia("comment", eachJsonObject, 0, 50):
                if not eachJsonObject['has_liked']:
                    api.like(media_id)
                    addComment(media_id, eachJsonObject)
                    i = i + 1
                time.sleep(random.randint(10, 20))
            progressbar(i / total, "Comment #" + str(hashtag))
    except:
        pass
    print("commentHashtag process is over: {0} pictures commented".format(i))
    _thread.exit()


def addComment(m_id, jsonObject):
    writestuff = comments[random.randint(0, len(comments) - 1)]

    try:
        # albania coordinates
        lat = float(jsonObject['location']['lat'])
        lng = float(jsonObject['location']['lng'])

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
        if flr > 1500 or flr < 70 or flng > 1500 or flng < 70:
            return False
        if flr - flng > 600:
            return False
        if flr/flng > 4:
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


def checkMedia(threadName, jsonObject, minim, maxim):
    try:
        post_like = int(jsonObject['like_count'])
        post_comment = int(jsonObject['comment_count'])
        if threadName == "like":
            if post_like in range(minim, maxim):
                return True
        if threadName == "comment":
            if post_comment in range(minim, maxim):
                return True
    except:
        pass

    return False


def checkTime(timevalue, minim, maxim):
    ct = time.time()
    if ct-timevalue in range(minim, maxim):
            return True
    return False


def checkQuality(jsonObject):
    try:
        media_points = 0
        description = str(jsonObject['caption']['text'])
        for eachHashtag in hashtagQuality:
            if eachHashtag in description:
                media_points = media_points + 1
        for eachHashtag in bannedHashtags:
            if eachHashtag in description:
                media_points = media_points - 2
        return int(media_points)
    except:
        return 0


def checkThis():
    updatelists()

    filez = open("check.txt", "a")
    for eachitem in followinglonglist:
        if checkWhitelist(eachitem[0]):
                filez.write(str(eachitem[1]) + "\n")
        time.sleep(random.randint(0, 3))
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
    peoplenotfollowingme(followingID, followersID)
    whiteListed()
    showstats()


def showstats():
    print("\n  {:10} {:10} {:10}\n  {:11s}{:11s}{}\n".format("Followers", "Following", "Unfollowing",
                                                     str(len(followersID)),
                                                     str(len(followingID)),
                                                     str(len(unfollowersID))
                                                     )
          )


def printusername(idnumber):
    for i in range(0, len(followinglonglist) - 1, 1):
        if idnumber == followinglonglist[i][0]:
            print("{:12}:  {}".format(str(followinglonglist[i][0]), str(followinglonglist[i][1])))


def getusername(idnumber):
    for i in range(0, len(followinglonglist) - 1, 1):
        if idnumber == followinglonglist[i][0]:
            return str(followinglonglist[i][1])
    return "not found"


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


"""
####    MAIN
"""

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

"""
###     SET LISTS
"""

followersID = []
followingID = []
unfollowersID = []

followerslonglist = []
followinglonglist = []

whitelist = []

"""
###     RUN
"""

login()
start()
