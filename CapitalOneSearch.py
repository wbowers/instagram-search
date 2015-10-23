
positivity_list = []

#could add likes to determine how much people agree with the positivity in the message
def is_positive(caption, list_of_tags):
    tags = list_of_tags
    words = caption.split()

    positivity = 0

    positives = ['good','love','fun','happy','excited', 'exciting', 'thanks', 'thank',
            'awesome','excellent','positve','well', 'perfect',
            'great', 'best',':)', 'outstanding', 'helpful', 'love']
    negatives = ['bad','sucks','problem','problematic','difficult','negative',
            'disappoint','disappointment','grr','troublesome',
            'imperfect',':(', 'awful','hate']
    inverses = ["not", "doesn't", "isn't", "no"]

    for tag in tags:
        for identifier in positives:
            if tag == identifier:
                positivity += 1
        for identifier in negatives:
            if tag == identifier:
                positivity -= 1

    for x in range(0, len(words)):
        inverted = False
        if x > 0:
            for inverse in inverses:
                if inverse == words[x-1]:
                    inverted = True
        for identifier in positives:
            if words[x] == identifier and inverted:
                positivity -= 1
            if words[x] == identifier and not inverted:
                positivity += 1
        for identifier in negatives:
            if words[x] == identifier and inverted:
                positivity += 1
            if words[x] == identifier and not inverted:
                positivity -= 1
    positivity_list.append(positivity)
    if positivity == 0:
        return 'neutral'
    if positivity > 0:
        return 'Positive'
    else:
        return 'Negative'


client_id = "4c5a72187f264ba883cc08b32064c54a"
client_secret = "9a26afeba3224a07917ea1bbc25c8b0a"

import requests
import json
from pprint import pprint

tag = "CapitalOne" # could take in user input and find trends for any tag
media_count = json.loads(requests.get("https://api.instagram.com/v1/tags/{}?client_id={}".format(tag,client_id)).text)["data"]["media_count"]


posts = requests.get("https://api.instagram.com/v1/tags/" + tag
        + "/media/recent?client_id={}&count={}".format(client_id,media_count))

post_info = json.loads(posts.text)

posts2 = requests.get(post_info["pagination"]["next_url"])
post2_info = json.loads(posts2.text)


more_data = True
count = 0
while more_data and count < 5: # to make sure the code doesn't take too long
    post_info["data"] += post2_info["data"]
    count += 1

    if post2_info["pagination"] == None:
        more_data = False
    else:
        posts2 = requests.get(post2_info["pagination"]["next_url"])
        post2_info = json.loads(posts.text)


#print len(post_info["data"])

for x in range(0,20):
    ans = "Post #{} has {} likes".format(x + 1 , post_info["data"][x]["likes"]['count'])
    user_id = post_info["data"][x]["user"]["id"]
    user = requests.get("https://api.instagram.com/v1/users/" + user_id
            + "/?client_id=4c5a72187f264ba883cc08b32064c54a")
    user_info = json.loads(user.text)
    ans += " and was posted by {} who has {} posts, {} followers, and {} followeees".format(
            user_info["data"]["username"],
            user_info["data"]["counts"]["media"],
            user_info["data"]["counts"]["followed_by"],
            user_info["data"]["counts"]["follows"])

    p_or_n = is_positive(post_info["data"][x]["caption"]["text"],
            post_info["data"][x]["tags"])
    print ans + ". The post is " + p_or_n + " towards " + tag + "."


for x in range(20,len(post_info["data"])):
    is_positive(post_info["data"][x]["caption"]["text"],
            post_info["data"][x]["tags"])

#print positivity_list

import plotly.plotly as py
#from plotly.graph_objs import Scatter

from plotly.graph_objs import *

positivity_list = list(reversed(positivity_list))

for x in range(1, len(positivity_list)):
    positivity_list[x] = positivity_list[x] + positivity_list[x-1]

trace = Scatter( x = range(0, len(positivity_list)),
y = positivity_list
)

data = [trace]

layout = Layout(
    title='Positivity of Individual Posts',
    showlegend=False,
    autosize=True,
    width=1022,
    height=485,
    xaxis=XAxis(
        title='Posts(0ldest to newest)',
        type='linear',
        autorange=True
    ),
    yaxis=YAxis(
        title='Net Positivity',
        type='linear',
        autorange=True
    )
)

fig = Figure(data = data, layout = layout)

unique_url = py.plot(fig, filename = 'positivity-line')


# Graph Ideas
#
# Add Note theat shows average positivity                       |
# Which percent of posts are positive, negative, neutral        |  add as 'notes' in chart
#
#
# chagne x axis to dates not numbers                           *******************

# Return most positve and most negative picture
#
