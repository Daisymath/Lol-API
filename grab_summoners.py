import requests
import pickle

api_key = ""

#open api key file
text_file = open("api_key.txt", "r")
 
#read in api key
api_key = text_file.read()
 
#close file
text_file.close()


# grab a list of summoner names by rank
#set up queue, tier, division 
queue = "RANKED_SOLO_5x5"
tier = "GOLD"
division = ["I","II","III","IV"]

summoners = []
for div in division:
    response = requests.get("https://na1.api.riotgames.com/lol/league/v4/entries/"+queue+"/"+tier+"/"+div+"?page=1&api_key="+api_key)
    res = response.json()

    #this produces a list of summoners, need to just pull out summoner id
    for sum in res:
        summoners.append(sum['summonerId'])


# #save summoners to a file
with open('summoners.txt', 'wb') as fp:
    pickle.dump(summoners, fp)