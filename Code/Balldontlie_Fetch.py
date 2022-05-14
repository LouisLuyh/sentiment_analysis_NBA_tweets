#!/usr/bin/env python3

## player_fetch
# See line 180 for instruction

##	This code is constructed based on the use of a balldontlie api  (https://www.balldontlie.io), which collects NBA data from 1979-current
from re import I
import requests
import json
import pandas as pd
import pprint
import sys
import matplotlib.pyplot as plt

#	A function that implements an ask for input of some specific NBA player, and returns his names and average score per season back to main().
def player_all_season_average_status(player_name):
	
	#	Basic introductions.
	introduction = "\nWelcome, our system can help you search for a NBA player or team and report all his/its status from the year of 2000 to 2021"
	print(introduction)
	#	search for the player's id
	#	player_name = input("Please enter a name of a player you are looking for stats\n--For ex. 'Lebron_James' (Capitalization does not matter)\nName: ")	#ask for a name
	#	a optional input function, allows users to input whatever player he wants to investigae about
	print()
	
	url_player_search = ("https://www.balldontlie.io/api/v1/players?search=" + player_name)
	player_search_request = requests.get(url_player_search)	#a list for all data of the player
	player_search_info_txt = player_search_request.text
	player_search_info_dic = json.loads(player_search_info_txt)
	player_id = player_search_info_dic['data'][0]['id']	#locate the player's id number
	
	#	fetch the player's average peformance from 2000 to 2021 season
	player_all_season_status = {}	#store data into dictionary
	for i in range(2000,2022):  #abstract data from year i to f
		url_player_season_average = ("https://www.balldontlie.io/api/v1/season_averages?season=" + str(i) + "&player_ids[]=" + str(player_id))
		player_season_avarage_request = requests.get(url_player_season_average)
		player_season_avarage_txt = player_season_avarage_request.text
		player_season_avarage_dic = json.loads(player_season_avarage_txt)
		if (player_season_avarage_dic['data'] != []):	#only embed data that are not empty (seasons this player didn't skip)
			player_all_season_status[i] = player_season_avarage_dic['data'][0]
	return player_name, player_all_season_status #return name of the player and the dictionary that contails average status back to main funciton

#	To output a dictionary for a player's stats
def display_player_dic(player_name, player_dic):
	for i in player_dic:	#	display everything in the dictionary
		print("The status of " + player_name + " in year " + str(i) + " is: \n" + str(player_dic[i]) + "\n")
	
	
## team_fetch	
	
# Check to see if given team name is an actual NBA team
def is_team(team_name):
	team_url = "https://www.balldontlie.io/api/v1/teams"
	get_teams = requests.get(team_url).json()["data"]
	team_dict = {}
	
	# Collects all NBA team names
	for i in range(0, 30):
		full_name = get_teams[i]["full_name"]
		name = get_teams[i]["name"]
		id = get_teams[i]["id"]
		team_dict[full_name] = id
		team_dict[name] = id
		
	# Searches for inputted name in the dictionary of real team names
	if team_name in team_dict.keys():
		return team_dict[team_name]
	else:
		return False
	
# Collects season data for specified NBA team
def get_all_games(team_name):
	print()
	#team_name = input("Enter a basketball team to get their stats\n--For ex. Los Angeles Lakers\nBe sure to capitalize letters correctly\nName: ")
	#print()
	# a optional input function, allows users to input whatever player he wants to investigae about
	
	
	valid_team = is_team(team_name)
	if valid_team == False:
		print("No team found. Check your spelling or try another team.")
		print()
		team_fetch()

	team_id = valid_team
	
	all_seasons_data = {}
	# For each season, collects data for each game in the season and calculate averages
	for season in range(2000, 2022):
		url = f"""https://www.balldontlie.io/api/v1/games?
		&per_page=100
		&team_ids[]={team_id}
		&postseason=false 
		&seasons[]={season}"""
		
		try:
			games_data = requests.get(url).json()["data"]
		except:
			continue
		
		print(f"Retrieved {season}-{season+1} season data")
		
		try:
			abbreviation = requests.get(f"https://www.balldontlie.io/api/v1/teams/{team_id}").json()["abbreviation"]
		except: 
			continue
		
		total_games = 0
		total_wins = 0
		total_points = 0
		# Collects data for each game, adds it to dictionary
		for game in range(0, len(games_data)):
			is_home = games_data[game]["home_team"]["abbreviation"] == abbreviation
			points = games_data[game]["home_team_score"] if is_home  else games_data[game]["visitor_team_score"]
			is_win = (is_home and (games_data[game]["home_team_score"] > games_data[game]["visitor_team_score"])) or (not is_home and (games_data[game]["home_team_score"] < games_data[game]["visitor_team_score"]))
			total_games += 1
			if is_win:
				total_wins += 1
			total_points += points
		points_per_game = total_points / total_games
		season_data = {"total_games":total_games,
					   "total_points":total_points,
					   "total_wins":total_wins,
					   "win_percent":total_wins/total_games,
					   "points_per_game":points_per_game}
		###all_seasons_data[f"{season}-{season+1}"] = season_data
		all_seasons_data[season] = season_data
		
	return all_seasons_data, team_name

	
#	main function
def player_fetch(player_name):
	player_name, player_dic = player_all_season_average_status(player_name) #catch the return values, player's name and status were returned from p_a_s_a_s function
	file = open("./Data/Player-- " + player_name.lower() + " data.txt", "w")
	file.truncate(0) #clean up the file before re-printing it
	file.close()
	neat_data = pprint.pformat(player_dic)
	print(neat_data, file = open("./Data/Player-- " + player_name.lower() + " data.txt", "a"))
	display_player_dic(player_name, player_dic)
	#input("Press enter to continue... \n\n")
	return player_dic
		


def team_fetch(team_name):
	data = get_all_games(team_name) 
	team_data = data[0]
	neat_data = pprint.pformat(data[0])
	print(neat_data, file=open(f"./Data/Team-- {data[1]} data.txt", "a")) 
	#sys.exit("Success!")
	print("Success!\n")
	#input("Press enter to continue... \n\n")
	return team_data
	
def run():
	#decision = input("\nWelcome to our system! You are currently at the menu page.\nPlease either type 'Player' or 'Team' to go into our different fetching system for related stats. \n'Player' or 'Team': ")
	#decision = decision.lower()
	#if (decision == "player"):
		#player_dic = player_fetch() ###player dic return
		#P_or_t = player_dic
	#elif (decision == "team"):
		#team_dic = team_fetch() ###team dic return
		#P_or_t = team_dic
	#else:
		#print("Something is wrong with your input, please try again.\n")
		
	#---------------------------------------------------------------------------------------
	#above is a optional function that allows a user to choos which function he wasnt to use, fetching player or team
		
		
		
	
	# uncomment the target sample, comment out non-target sample
	
	#name = 'Trae_Young'
	#name = 'Lebron_James'
	#name = 'James_Harden'
	#name = 'Atlanta Hawks'
	#name = 'Brooklyn Nets'
	name = 'Los Angeles Lakers'
	
	'''
	if want to fetch player data: 
		uncomment #decision = 'player'
		comment out decision = 'team'
	
	if want to fetch team data: 
		uncomment #decision = 'team'
		comment out decision = 'player'
	'''
	
	#decision = 'player'
	decision = 'team'
	if decision == 'player':
		P_or_t = player_fetch(name)
	else:
		P_or_t = team_fetch(name)
		

	return P_or_t, decision, name


def check_years(p):   #Check the begin years of Graphteam
    
	years = 2000
	for year in p:
	
		if year in p:	
			print()
		else:
			years += 1
		return year
		
def team_dataRead(dataDic,year): # account neccesary lists of variables from the team dictionary fetched
	
	team_totalgame_list = []	
	team_totalwin_list = []
	points_per_game_list = []

	for year in range(year,2022):
		
		if year in dataDic:
		
			team_totalgame_list.append(dataDic[year]['total_games'])
			team_totalwin_list.append(dataDic[year]['total_wins'])
			points_per_game_list.append(dataDic[year]['points_per_game'])
	return team_totalgame_list, team_totalwin_list, points_per_game_list


def player_dataRead(dataDic,year): # account neccesary lists of variables from the player dictionary fetched
	
	player_pts_list = []	
	player_reb_list = []
	player_ast_list = []
	player_turnover_list = []

	for i in range(year,2022):
		
		if i in dataDic:
		
			player_pts_list.append(dataDic[i]['pts'])
			player_reb_list.append(dataDic[i]['reb'])
			player_ast_list.append(dataDic[i]['ast'])
			player_turnover_list.append(dataDic[i]['turnover'])
	return player_pts_list,player_reb_list,player_ast_list,player_turnover_list


def teamgraph(l1,l2,l3,year,team_name): #main function for drawing a team's graphic
	yearX = []
	plt.figure(figsize=(13, 5), dpi=200)
	for i in range(year,2022):
		yearX.append(i)
	x = range(year,2022,1)

	plt.plot(yearX, l1, label="totalgame", color="#FF3B1D", marker='*', linestyle="-") 
	plt.plot(yearX, l2, label="totalwin", color="#3399FF", marker='o', linestyle="-")
	plt.plot(yearX, l3, label="points", color="#F9A602", marker='s', linestyle="-")


	plt.xticks(x)#设置x轴刻度
	plt.xlabel("Season")#横坐标名字
	plt.ylabel("Game Data")#纵坐标名字
	plt.legend(loc = "best")#图例
	plt.savefig('./Figures/Team--' + team_name + ' Line chart.jpg')  #store the graphic
	#print 图像
	plt.show()


def palyergraph(l1,l2,l3,l4,year,player_name):  #main function for drawing a player's graphic
	yearX = []

	
	plt.figure(figsize=(13, 5), dpi=200)
	for i in range(year,2022):
		yearX.append(i)
	x = range(year,2022,1)

	plt.plot(yearX, l1, label="points", color="#FF3B1D", marker='*', linestyle="-") 
	plt.plot(yearX, l2,label="reb", color="#3399FF", marker='o', linestyle="-")
	plt.plot(yearX, l3, label="ast_", color="#F9A602", marker='s', linestyle="-")
	plt.plot(yearX, l4, label="turnover", color="#13C4A3", marker='d', linestyle="-")

	plt.xticks(x)#设置x轴刻度
	plt.xlabel("Season")#横坐标名字
	plt.ylabel("Player Data")#纵坐标名字
	plt.legend(loc = "best")#图例
	plt.savefig('./Figures/Player--' + player_name + ' Line chart.jpg')  #tore the grapic
	#print 图像
	plt.show()


		
	
#	Strarting the program
if __name__ == '__main__':
	P_or_t, decision, name = run()
	
	year = check_years(P_or_t)

	if (decision == "player"):
		player_pts_list,player_reb_list,player_ast_list,player_turnover_list = player_dataRead(P_or_t,year) 
		palyergraph(player_pts_list,player_reb_list,player_ast_list,player_turnover_list,year, name)
	elif(decision == "team"):
		team_totalgame_list, team_totalwin_list, points_per_game_list = team_dataRead(P_or_t,year)
		teamgraph(team_totalgame_list,team_totalwin_list,points_per_game_list,year,name)
	
	