import tweepy
import time
import random

#This section requires the keys to be inserted instead of the "x" in order for the code to work!
API_KEY = "xxx"
API_SECRET = "xxx"
ACCESS_KEY = "xxx"
ACCESS_SECRET = "xxx"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_id.txt'
FILE_NAME1 = 'self_love.txt'
FILE_NAME2 = 'reminders.txt'

#Function that retrieves the last ID that was seen from the file and returns it.
def retrieve_last_id(file_name):
    f_read = open(file_name, 'r')
    last_id = int(f_read.read().strip())
    f_read.close()
    return last_id

#Function that stores the last id that was seen on Twitter to the file.
def store_last_id(last_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_id))
    f_write.close()
    return

#Loads the self-love quotes and makes a list out of it.
def load_love(file_name):
    my_file = open(file_name, 'r')
    content = my_file.read()
    love_list = content.split("\n")
    my_file.close()

    return love_list

#Loads the reminders and makes a list out of it.
def load_reminder(file_name):
    my_file1 = open(file_name, 'r')
    content1 = my_file1.read()
    reminder_list = content1.split("\n")
    my_file1.close()

    return reminder_list

#Function that automates tweets every 1 hour. It waits 1 hour before tweeting.
def tweet(content):
    print("Tweeting out soon", flush = True)
    tweets = random.choice(content)
    api.update_status(status=tweets)
    time.sleep(3600)

#Function that goes through the ids from earliest to latest and replies to each one with a random reminder.
def reply(content1):
    print('tweets are being grabbed and replied', flush = True)
    last_id = retrieve_last_id(FILE_NAME)
    mentions = api.mentions_timeline(tweet_mode='extended')

    for mention in reversed(mentions):
        last_id = mention.id
        store_last_id(last_id, FILE_NAME)
        print("Found the mention", flush = True)
        print("Now responding back", flush = True)

        username = mention.user.screen_name

        reply = "@%s " % username + random.choice(content1)
        api.update_status(status=reply, in_reply_to_status_id=mention.id)

while True:
    try:
        content1 = load_reminder(FILE_NAME2)
        reply(content1)
        content = load_love(FILE_NAME1)
        tweet(content)
    except tweepy.errors.TweepyException:
        time.sleep(15)
    except StopIteration:
        break
