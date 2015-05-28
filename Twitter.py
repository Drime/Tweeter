from  TwitterAPI import TwitterAPI, TwitterRestPager

#Twitter config
consumer_key="x2eEtVabxBHgO2ZCbPILgQ"
consumer_secret ="NCAfNJ2TumW1c8CzIRetMuvnv7lMP6zcoRCoCzUcfg"

access_token_key = "901352550-XA7os5RsxyONuHYDVGsh53pHJM1WraJ4X4WQ6TKs"
access_token_secret = "scGqUMcvWruw8wzb6LLvBKhjbRJc6blyNHtFRRw2ckQ"



if __name__ == "__main__":

#def Get_Twitter():

    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret, auth_type='oAuth1',)

    #pulled_tweets = api.request('statuses/update', 'to:abnamro -from:abnamro')

    pager = api.request('search/tweets', {'q': 'to:abnamro -from:abnamro', 'count': '100', 'since': '2015-05-28'})

    print('jj')

    for item in pager:
        print(item['text'] if 'text' in item else item)
