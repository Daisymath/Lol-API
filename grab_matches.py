from platform import machine
import requests
import time
import pickle

api_key = ""

#open api key file
text_file = open("api_key.txt", "r")
 
#read in api key
api_key = text_file.read()
 
#close file
text_file.close()

#unix time
start_time = "1646183717"

# Open summoner list:
with open ('puuids.txt', 'rb') as fp:
    puuids = pickle.load(fp)



#loop over this list and pull ranked matches from each into a new list
n = len(puuids)
print(n)
m = n//100 + 1
print(m)

matches = set()
for i in range(m):
    temp_start = time.time()
    for puuid in puuids[i*100:(i+1)*100]:
        #each req and append takes about 0.36 s each
        temp_res = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?startTime="+start_time+"&queue=420&start=0&count=100&api_key="+api_key).json()
        for match in temp_res:
            matches.add(match)
    temp_end = time.time()
    temp_time = (temp_end - temp_start)
    print("round ",i," successful in ", temp_time," seconds")
    time.sleep(90)
print(len(matches))



#back to list
matches_list = list(matches)


#write to file
with open('match_ids.txt', 'wb') as fp:
        pickle.dump(matches_list, fp)





