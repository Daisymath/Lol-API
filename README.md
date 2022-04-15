# League of Legends API
Python code for grabbing information from RIOT API

## Description
This code will use a base RIOT API key to pull match info from RIOT's API.  I wanted data from ranked matches to try and apply ML algorithms as I learn about them.  The goal would be to predict the winner of a match by the information at the 14 minute mark of the game.  

## What Next
I am going to work on cleaning up the structure of the code and files.  Firstly, creating one main script and making each file into a module with a function to import.  As I work on the ML algorithms, finding better features to pull would be next. 

## Libraries
For the API I used pandas, requests, pickle, time, and math libraries.

## Challenges
Since my API key is currently a temporary one, RIOT has a servere limit on requests per minute.  Specifically, I am allowed 100 requests per 2 minutes.  This means that to grab 10,000 matches, I needed to break this into chunks and then make sure I didn't go past this limit.  If you do this on a temporary key, it will take some time to grab a large number of matches.

## Running This Code
To run this code you need to first install the required libraries if you do not have them installed.

Then you need to run the following files in order.

grab_summoners.py -> grab_puuids.py -> grab_matches.py -> grab_info.py

<strong>grab_summoners.py</strong>

This file grabs summoner id's for the given que, tier, and division(s).  These need to be defined in the file.  I have it set up to grab summoners in Gold IV - I.

<strong>grab_puuid.py</strong>

This file takes in the summoner id's and grabs puuid's.  

<strong>grab_matches.py</strong>

This file takes in the puuid's and pulls ranked match id's played by each player.  You need to choose the start time you are interested in.  It is in UNIX time and I have it currently set for about when patch 12.5 dropped.  I first set up the variable matches as a set since I expect to get many duplicates.  This is the converted to a list to save.

<strong>grab_info.py</strong>

This file takes in the match id's and pulls data from the match and match-timeline API's.  This means two calls for each match.  This is why they are broken into chunks of 50 at a time.  I set up a team_df that contains dictionaries for each time.  The keys represent information I was interested in pulling.  For each request, if the API status code is not 200 it is printed.  This way if something goes wrong you can see it!

## Link to Kaggle dataset example
https://www.kaggle.com/datasets/gbolduc/league-of-legends-lol-gold-ranked-games

## Resources from RIOT API
https://developer.riotgames.com/

https://developer.riotgames.com/apis
