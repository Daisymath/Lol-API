import requests
import time
import pickle
import math

api_key = "RGAPI-96387f00-a727-4058-9743-f1006ce239f3"


# Open list of match ids:
with open ('match_ids.txt', 'rb') as fp:
    match_ids = pickle.load(fp)

#only going to try the first 5000
match_ids = match_ids[:1000]
n = len(match_ids)
print(n)
m = n//100 + 1
print(m)

#break up into chunks of 100 matches and grab
matches = []
for i in range(m):
    temp_start = time.time()
    for match_id in match_ids[i*100:(i+1)*100]:
        #each req and append takes about 0.36 s each
        temp_res = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+match_id+"?api_key="+ api_key).json()
        matches.append(temp_res)
    temp_end = time.time()
    temp_time = (temp_end - temp_start)
    print("round ",i," successful in ", temp_time," seconds")
    time_sleep = math.ceil(120 - temp_time) + 1
    print(time_sleep)
    time.sleep(time_sleep)
print(len(matches))


with open('matches.txt', 'wb') as fp:
    pickle.dump(matches, fp)

#start by pulling info from no timeline
#pull the entire thing and add to a list -> pickled and saved to a file.  We can process the data later to pull shit out and put into a sql db

#keeps running into erros like:

# requests.exceptions.SSLError: HTTPSConnectionPool(host='americas.api.riotgames.com', port=443): Max retries exceeded with url: /lol/match/v5/matches/NA1_4251900816?api_key=RGAPI-96387f00-a727-4058-9743-f1006ce239f3 (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:997)')))







#write my dict to a json file
#json_string = json.dumps(response.json()['info'])

#print(json.dumps(response.json(), sort_keys=True, indent=4))

# save it to a file
# with open('game_data_test.json', 'w') as outfile:
#    outfile.write(json_string)