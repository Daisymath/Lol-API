# Goal is to grab a single match and pick out the information 
# Once this is figured out, we can figure out how to save it to a SQL DB

import requests
import pandas as pd
import pickle
import time
import math

api_key = ""

#open api key file
text_file = open("api_key.txt", "r")
 
#read in api key
api_key = text_file.read()
 
#close file
text_file.close()
 


#test match_id
# match_id = "NA1_4242407137"

#load match ids
with open ('match_ids.txt', 'rb') as fp:
    match_ids = pickle.load(fp)



# Use this to restrict to a smaller batch of match id's if needed.
# temp_match_ids = match_ids[0:20]

#because my api key has rate limits, I need to break up the match ids into 50 id chunks.  I can run 100 api calls in 2 minutes.  Each match takes 2 api calls.
n = len(match_ids)
print(n)
m = n//50 + 1
print(m)

#list for matches
matches_meta = []
matches_info = []
#open the previous list of full timeline matches
with open("full_games.txt","rb") as f:
    obj = pickle.load(f)
    #I had some issues with doing too many at once, this is here to take a breather so we don't get our API key rejected.
    for i in range(m):
        if i == math.floor(m/2):
            time.sleep(120)
        #We will keep track of how long this takes and then add a sleep time to get to 2 minutes.
        temp_start = time.time()
        for match_id in match_ids[i*50:(i+1)*50]:
            #Setting up data frames for teams
            #initial list of dicts for the teams
            teams_df = [
                {"win":False,
                "dragons":0,
                "rift":0,
                "towersTaken":[0,0,0],
                "players":[
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    },
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    },
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    },
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    },
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    }
                ]
                },
                {"win":False,
                "dragons":0,
                "rift":0,
                "towersTaken":[0,0,0],
                "players":[
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    },
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    },
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    },
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    },
                    {"pId":0,
                    "champion":"",
                    "role":"",
                    "gold":0,
                    "minions":0,
                    "jungleMinions":0,
                    "kills":0,
                    "deaths":0,
                    "assists":0
                    }
                ]
                }

            ]


            #############Setting up data for match meta

            #get the timeline match data
            res_timeline = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+match_id+"/timeline?api_key="+ api_key)

            # 200 we are good to go, otherwise skip this match and go to the next one.
            if res_timeline.status_code == 200:
                pass
            else:
                print(match_id)
                continue

            #save the raw timeline data and store it in case we want to change the information we are collecting later.
            save = res_timeline.json()
            obj.append(save)

            #frames happen every 60 seconds.  These contain all of the events that have happened in the last minute and summary info for that minute.
            frames = res_timeline.json()['info']['frames']

            #get the non timeline match information
            res_no_timeline = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/"+match_id+"?api_key="+ api_key)
            if res_no_timeline.status_code == 200:
                pass
            else:
                print(match_id)
                continue
            #the info dict is where most of the relevant information is.
            res_no_t_json = res_no_timeline.json()['info']

            #game length
            game_length = res_no_t_json["gameDuration"]

            #set up a list for the players
            teams= []

            participants = res_no_t_json['participants']
            # fill out the id, champion, and role for each player. 
            # the first 5 are on the blue team, next five on the read team 
            for i in range(len(participants)):
                if i < 5:
                    teams_df[0]["players"][i]["pId"] = participants[i]["participantId"]
                    teams_df[0]["players"][i]["champion"] = participants[i]["championName"]
                    teams_df[0]["players"][i]["role"] = participants[i]["teamPosition"]
                else:
                    teams_df[1]["players"][i%5]["pId"] = participants[i]["participantId"]
                    teams_df[1]["players"][i%5]["champion"] = participants[i]["championName"]
                    teams_df[1]["players"][i%5]["role"] = participants[i]["teamPosition"]


            #winning team
            winning_team = frames[-1]['events'][-1]['winningTeam']

            #update df
            if winning_team == 100:
                teams_df[0]["win"] = True
            else:
                teams_df[1]["win"] = True






            ################
            # #Setting up data for match info
            ###############
            #find timestamp close to 14 min
            #this will pull the participant frames 1 - 10 at about 14 min.  
            for frame in frames:
                ###Grab the frame at 14 minutes to find summary info on each player
                if abs(frame['timestamp'] - 840000) < 1000:
                    for i in range(len(frame['participantFrames'])):
                    #total gold,minions,jungle minions
                        if i < 5:
                            teams_df[0]["players"][i]["gold"] = frame['participantFrames'][str(i+1)]["totalGold"]
                            teams_df[0]["players"][i]["minions"] = frame['participantFrames'][str(i+1)]["minionsKilled"]
                            teams_df[0]["players"][i]["jungleMinions"] = frame['participantFrames'][str(i+1)]["jungleMinionsKilled"]
                        else:
                            teams_df[1]["players"][i%5]["gold"] = frame['participantFrames'][str(i+1)]["totalGold"]
                            teams_df[1]["players"][i%5]["minions"] = frame['participantFrames'][str(i+1)]["minionsKilled"]
                            teams_df[1]["players"][i%5]["jungleMinions"] = frame['participantFrames'][str(i+1)]["jungleMinionsKilled"]

                #now look at all of the frames up to and including 14 minutes.
                if frame['timestamp'] < 841000:
                    for event in frame['events']:
                        #counting up champion kills
                        if event['type'] == "CHAMPION_KILL":
                            ##victimId
                            if event["victimId"] <= 5:
                                teams_df[0]["players"][event["victimId"] - 1]["deaths"] += 1
                            else:
                                teams_df[1]["players"][event["victimId"]%6]["deaths"] += 1

                            #killerId
                            if event["killerId"] <= 5:
                                teams_df[0]["players"][event["killerId"] - 1]["kills"] += 1
                            else:
                                teams_df[1]["players"][event["killerId"]%6]["kills"] += 1

                            # assisting participants this is a list
                            if "assistingParticipantIds" in event.keys():
                                for part in event["assistingParticipantIds"]:
                                    if part <=5:
                                        teams_df[0]["players"][part - 1]["assists"] += 1
                                    else:
                                        teams_df[1]["players"][part%6]["assists"] += 1

                        #counting up dragon and rift herald kills
                        if event['type'] == "ELITE_MONSTER_KILL":
                            if event["monsterType"] == "DRAGON":
                                if event["killerTeamId"] == 100:
                                    teams_df[0]["dragons"] += 1
                                else:
                                    teams_df[1]["dragons"] += 1
                            elif event["monsterType"] == "RIFTHERALD":
                                if event["killerTeamId"] == 100:
                                    teams_df[0]["rift"] += 1
                                else:
                                    teams_df[1]["rift"] += 1

                        #counting up tower kills           
                        if event['type'] == "BUILDING_KILL":
                            if event['teamId'] == 100:
                                if event["laneType"] == "TOP_LANE":
                                    teams_df[0]["towersTaken"][0] += 1
                                elif event["laneType"] == "MID_LANE":
                                    teams_df[0]["towersTaken"][1] +=1
                                else:
                                    teams_df[0]["towersTaken"][2] += 1
                            elif event['teamId'] == 200:
                                if event["laneType"] == "TOP_LANE":
                                    teams_df[1]["towersTaken"][0] += 1
                                elif event["laneType"] == "MID_LANE":
                                    teams_df[1]["towersTaken"][1] += 1
                                else:
                                    teams_df[1]["towersTaken"][2] += 1

            
            ###################
            #Set up Roles 
            ##################
            temp_team1 = []
            for player in teams_df[0]['players']:
                if player['role'] == "TOP":
                    temp_team1.append(player["champion"])
                elif player['role'] == "JUNGLE":
                    temp_team1.append(player["champion"])
                elif player['role'] == "MIDDLE":
                    temp_team1.append(player["champion"])
                elif player['role'] == "BOTTOM":
                    temp_team1.append(player["champion"])
                elif player['role'] == "UTILITY":
                    temp_team1.append(player["champion"])

            temp_team2 = []
            for player in teams_df[1]['players']:
                if player['role'] == "TOP":
                    temp_team2.append(player["champion"])
                elif player['role'] == "JUNGLE":
                    temp_team2.append(player["champion"])
                elif player['role'] == "MIDDLE":
                    temp_team2.append(player["champion"])
                elif player['role'] == "BOTTOM":
                    temp_team2.append(player["champion"])
                elif player['role'] == "UTILITY":
                    temp_team2.append(player["champion"])

            ##combine meta info into one list and add it to list of matches
            matches_meta.append([match_id,game_length,winning_team]+temp_team1 + temp_team2)



            #calculate gold differences between roles 
            temp_gold_diff = [0,0,0,0,0]
            for player in teams_df[0]['players']:
                if player['role'] == "TOP":
                    temp_gold_diff[0] += player["gold"]
                elif player['role'] == "JUNGLE":
                    temp_gold_diff[1] += player["gold"]
                elif player['role'] == "MIDDLE":
                    temp_gold_diff[2] += player["gold"]
                elif player['role'] == "BOTTOM":
                    temp_gold_diff[3] += player["gold"]
                elif player['role'] == "UTILITY":
                    temp_gold_diff[4] += player["gold"]

            for player in teams_df[1]['players']:
                if player['role'] == "TOP":
                    temp_gold_diff[0] -= player["gold"]
                elif player['role'] == "JUNGLE":
                    temp_gold_diff[1] -= player["gold"]
                elif player['role'] == "MIDDLE":
                    temp_gold_diff[2] -= player["gold"]
                elif player['role'] == "BOTTOM":
                    temp_gold_diff[3] -= player["gold"]
                elif player['role'] == "UTILITY":
                    temp_gold_diff[4] -= player["gold"]

            # add the match info data to the matches info list.  
            matches_info.append([match_id,teams_df[0]['dragons'],teams_df[1]['dragons'],teams_df[0]['rift'],teams_df[1]['rift']] + temp_gold_diff + teams_df[0]['towersTaken'] + teams_df[1]['towersTaken'])
        
        # finding out how long this batch of 50 took
        temp_end = time.time()
        temp_time = (temp_end - temp_start)

        #if it took less than 2 minutes, add in the required sleep time to get to 2 minutes.
        if(temp_time < 120):
            time_sleep = math.ceil(120 - temp_time) + 1
            time.sleep(time_sleep)
        print("This round took: ",temp_time," seconds")    
    


########################
# Setting up df's and saving to csv's

#Put list of matches into df
match_meta = pd.DataFrame(data=matches_meta,index=None,columns=["matchId","gameLength","winningTeam","team1Top","team1Jg","team1Mid","team1Adc","team1Supp","team2Top","team2Jg","team2Mid","team2Adc","team2Supp"])
print(match_meta.head())

# #Put list of match infos into df
match_info = pd.DataFrame(data=matches_info,index=None,columns=["matchId","t1Dragons","t2Dragons","t1Rift","t2Rift","topGoldDiff","jgGoldDiff","midGoldDiff","adcGoldDiff","suppGoldDiff","t1TopTowerTaken","t1MidTowerTaken","t1BotTowerTaken","t2TopTowerTaken","t2MidTowerTaken","t2BotTowerTaken"])
print(match_info.head())


# add the raw match timeline data to the full_games file.
with open('full_games.txt', 'wb') as fc:
        pickle.dump(obj, fc)


# add the match meta and info to the csv file.
#append mode has not worked for me.  If doing this in chunks, you have to make a new csv each time and then combine them later via Python or manually in Excel/Sheets/etc.

match_meta.to_csv('matches_meta.csv',index=False,header=False)

match_info.to_csv('matches_info.csv',index=False,header=False)

