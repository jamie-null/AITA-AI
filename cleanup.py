import praw
import pickle as pkl
from math import log
import csv
from datetime import datetime, timezone
from collections import Counter
import re

def pickleLoader(pklFile):
    try:
        while True:
            yield pkl.load(pklFile)
    except EOFError:
        pass

with open('posts.pkl','rb') as f, open('posts.csv', 'w', encoding='utf-8', newline='') as csvfile:
    postwriter = csv.writer(csvfile)
    postwriter.writerow(['id','title','created_utc' 'body','nta','yta','nah','esh','info','flair'])

    flairs = Counter()
    i = 0
    for post in pickleLoader(f):
        if i > 1000:
            break
        i += 1
        if "meta" in post.title.lower() or "update" in post.title.lower():
            continue
        if post.link_flair_text is not None:
            flairs[post.link_flair_text] += 1
            if "meta" in post.link_flair_text.lower() or "shitpost" in post.link_flair_text.lower() or "troll" in post.link_flair_text.lower():
                continue
        if post.selftext == "[removed]" or post.selftext == "[deleted]":
            continue

        nta = 0
        yta = 0
        nah = 0
        esh = 0
        info = 0

        post.comments.replace_more(limit=0)
        for comment in post.comments:
            if comment.author == "AutoModerator" or comment.is_submitter or comment.score < 1:
                continue
            #only count parent comments
            if comment.parent_id[:2] != "t3":
                continue

            #if a comment contains multiple acronyms, count it for all of them
            if re.search(r"\bnta\b",comment.body,re.IGNORECASE):
                nta += comment.score
            if re.search(r"\byta\b",comment.body,re.IGNORECASE):
                yta += comment.score
            if re.search(r"\bnah\b",comment.body,re.IGNORECASE):
                nah += comment.score
            if re.search(r"\besh\b",comment.body,re.IGNORECASE):
                esh += comment.score
            if re.search(r"\binfo\b",comment.body,re.IGNORECASE):
                info += comment.score

        print(post.link_flair_text,datetime.fromtimestamp(post.created_utc))
        postwriter.writerow([post.id,post.title,post.created_utc,post.selftext,nta,yta,nah,esh,info,post.link_flair_text])

print(flairs.most_common())

"""
        #enforce conformity of scores with judgement
        if link_flair_text is None:
            continue
        elif "no " in post.link_flair_text.lower() && max(nah,esh,info,nta,yta) != nah:
            nah = max(nah,esh,info,nta,yta) * 2
        elif "every" in post.link_flair_text.lower() && max(nah,esh,info,nta,yta) != nah:
            nah = max(nah,esh,info,nta,yta) * 2
        elif "info" in post.link_flair_text.lower() or "too close" in post.link_flair_text.lower() && max(nah,esh,info,nta,yta) != nah:
            nah = max(nah,esh,info,nta,yta) * 2
        elif "not the" in post.link_flair_text.lower() && max(nah,esh,info,nta,yta) != nta:
            nta = max(nah,esh,info,nta,yta) * 2
        elif "asshole" == post.link_flair_text.lower() && max(nah,esh,info,nta,yta) != yta:
            yta = max(nah,esh,info,nta,yta) * 2

        #if still it adds up to zero, discard, otherwise balance it out
        total = sum([log(max(i,1) for i in [nta,yta,nah,esh,info]])
        if total == 0:
            continue
        else:
            normed = [log(max(i,1)/total for i in [nta,yta,nah,esh,info]]
"""