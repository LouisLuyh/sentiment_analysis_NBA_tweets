import tweepy
import json,time,datetime,os
import sys
import csv
auth = tweepy.OAuthHandler('PvproNswsUGnHlZyJoGti14TW', 'OGLm6qBWPxEPnG0sYonHHoqMlINQHZen8cDo23yjuuJ79zriLG')
auth.set_access_token('1496267973488693252-PXDrYXsSYIUwJsv9EC9K9wSBVP0qmg', 'mI4XTu5WZGRXGE7XIIJVgNC1Yd5PpbsaVpftFeEImvMyb')

api = tweepy.API(auth)



kws = ['@Lakers','@BrooklynNets','@ATLHawks'];  #Keywords of Players
#['@KingJames','@JHarden13','@TheTraeYoung'] # Keywords of teams

for kw in kws:
    results = []  # used to save the final result
    ids = []  # id list, used to cancel repeatition
    csvpath = '%s.csv'%kw
    min_id = 0
    if os.path.exists(csvpath):
        with open(csvpath,encoding='utf8') as csvfile:  #Read the previous recording 
            reader = csv.reader(csvfile)
            for record in reader:
                if record:
                    id, text = record
                    ids.append(id)
                    results.append(text)


    with open(csvpath,'a',encoding='utf8',newline='') as f: # open the file and use it to store tweets
        out_f = csv.writer(f)
        for i in range(20): # can save at most 20*100 tweets once 
            if min_id:
                print(min_id)
                public_tweets = api.search_tweets(kw,max_id=min_id,result_type='recent',count=100)
            else:
                public_tweets = api.search_tweets(kw,result_type='recent',count=100)
            print(len(public_tweets))
            for tweet in public_tweets:
                text = tweet.text
                id = str(tweet.id)
                if not min_id:
                    min_id=id
                elif id<min_id:
                    min_id=id
                if not id in ids:
                    ids.append(id)
                    out_f.writerow([id, text])
                    results.append(text)
            if len(public_tweets)<100:
                break
            else:
                time.sleep(5) #take a rest
        print('total :%s'%(len(ids)))

    
    #players' tweets: dates from 4.11 - 4.22
    
    #teams' tweets: dates from  4.19 - 5.1
    