from platform import machine
import requests
import time
import pickle

api_key = "RGAPI-96387f00-a727-4058-9743-f1006ce239f3"

#unix time
start_time = "1646183717"

# Open summoner list:
with open ('puuids.txt', 'rb') as fp:
    puuids = pickle.load(fp)

# puuid = puuids[0]

# Need to get api key for only ranked matches starting in 12.5, then put in code to space things out.
# request matches for a single player
# response = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?startTime="+start_time+"&queue=420&start=0&count=100&api_key="+api_key)
# print(response.json())


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


#solo que is queueId = 420, lol
#timestamps are given in unix, just use a converter -> start with patch 12.5 -> 1646183717

#back to list
matches_list = list(matches)

print(len(matches_list))

#write to file
with open('match_ids.txt', 'wb') as fp:
        pickle.dump(matches_list, fp)





