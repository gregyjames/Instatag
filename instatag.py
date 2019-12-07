import urllib2
from bs4 import BeautifulSoup
import json
import re
import math

tag = "funny"
num = 30

response = urllib2.urlopen("https://www.instagram.com/explore/tags/" + tag + "/")
data = response.read()
soup = BeautifulSoup(data, 'html.parser')

#The third script tag is the one with the post data
script = soup.find_all('script')[3].get_text()
#Strip out non json
script = script[21:len(script) -1]

#Get the post data
posts = json.loads(script)
posts = posts["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_top_posts"]["edges"]

tags = []
like_counter = {}
users = {}

for i in posts:
    try:
        #Get all the hashtags per post
        post_tags=re.findall(r"#(\w+)",i["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"])
        #Add post tags to total tags
        tags.extend(post_tags)
        for tag in post_tags:
            if tag in like_counter:
                like_counter[tag] = like_counter[tag] + int(i["node"]["edge_liked_by"]["count"])
                users[tag].append(i["node"]["owner"]["id"])
            else:
                like_counter[tag] = 1
                users[tag] = []
    except:
        pass

tag_counter = {}

#Get the counts of each tag
for tag in tags:
    if tag in tag_counter:
        tag_counter[tag] += 1
    else:
        tag_counter[tag] = 1

avg_likes = {}

for tag in tags:
    avg_likes[tag] = math.floor(like_counter[tag] / tag_counter[tag])

popular_tags = sorted(tag_counter, key = tag_counter.get, reverse = True)
top_tags = popular_tags[:num]

print("All tags in top posts: ")
tagstring = ""
for i in popular_tags:
    tagstring += "#" + i + " "
print(tagstring)

print("\nTop " + str(num) + " tags:")
for i in top_tags:
    #Get count of tag use, total likes, and avg likes per tag
    print(str(i) + "\n->\tCount:" + str(tag_counter[i]) + "\n->\tTotal Likes:" + str(like_counter[i])+ "\n->\tAvg Likes:" + str(avg_likes[i]))
    #For all users who use the hashtag
    print("\tUsers:")
    for i in users[i]:
        #Get user ID
        print("\t\t" + i)
        #Attempt to get username
        try:
            user_url = "https://i.instagram.com/api/v1/users/" + i + "/info/"
            user_req = urllib2.Request(user_url, headers={ 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 Instagram 12.0.0.16.90 (iPhone9,4; iOS 10_3_3; en_US; en-US; scale=2.61; gamut=wide; 1080x1920)' })
            user_html = urllib2.urlopen(user_req).read()
            user_json = json.loads(user_html)
            print("\t\t" + "->" + user_json["user"]["username"])
        except:
            pass

print("\nYour tag list: ")

tagstring = ""
for i in top_tags:
    tagstring += "#" + i + " "
print(tagstring)
        