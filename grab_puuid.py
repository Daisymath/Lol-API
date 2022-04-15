import requests
import pickle
import time

api_key = "RGAPI-96387f00-a727-4058-9743-f1006ce239f3"

# Open summoner list:
with open ('summoners.txt', 'rb') as fp:
    summoners = pickle.load(fp)

n = len(summoners)
print(n)
m = n//100 + 1
print(m)

puuids = []
for i in range(m):
    temp_start = time.time()
    for sum in summoners[i*100:(i+1)*100]:
        #each req and append takes about 0.36 s each
        temp_res = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/"+ sum +"?api_key="+api_key)
        puuids.append(temp_res.json()["puuid"])
    temp_end = time.time()
    temp_time = (temp_end - temp_start)
    print("round ",i," successful in ", temp_time," seconds")
    time.sleep(90)
        

# puuids = []
# for sum in summoners:
#     temp_res = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/"+ sum +"?api_key="+api_key)
#     puuids.append(temp_res.json()["puuid"])


# print(len(puuids))
# print(puuids)

with open('puuids.txt', 'wb') as fp:
        pickle.dump(puuids, fp)