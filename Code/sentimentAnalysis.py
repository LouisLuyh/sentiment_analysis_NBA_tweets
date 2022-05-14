#!/usr/bin/env python3

from csv import reader
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# this method reads the comments stored in the CSV file, and perform sentiment analysis on the comments
# will return the result of sentiment analysis and the sum of compound
def sentimentAnalysis(filename):

	sentences, users, result, negative, positive = [], [], [], [], []
	compoundSum, index = 0, 0
	
	with open(filename, 'r') as csvFile:
		csvReader = reader(csvFile)
		rows = list(csvReader)
		
	for i in rows:
		users.append(i[0])
		sentences.append(i[1])
	
	for sentence in sentences:
		sid = SentimentIntensityAnalyzer()
		ss = sid.polarity_scores(sentence)
		result.append((users[index], ss.get("compound"), ss.get("neg"), ss.get("pos"), sentence))
		compoundSum += ss.get("compound")
		index += 1
		
	return result, compoundSum
	
	
# this method returns the most positive and most negative tweet, as well as their sentiment scores
def findMostPN(result):
	
	positive = result.sort(key=lambda y: y[3])
	mostPositive = result[-1]
		
	negative = result.sort(key=lambda y: y[2])
	mostNegative = result[-1]
	
	return mostPositive, mostNegative


# this method categorizes the result of sentiment analysis into positive, negative, and neutral
# this method returns the data for drawing the pie chart
def graphData(result, compoundSum):
	
	compoundAverage = compoundSum/len(result)
	
	positives, negitives, neutrals = [], [], []
	for i in result:
		if i[1] > 0:
			positives.append(i)
		elif i[1] < 0:
			negitives.append(i)
		elif i[1] == 0:
			neutrals.append(i)
	
	return compoundAverage, len(positives), len(negitives), len(neutrals), len(result)
	

# the files to preform sentiment analysis on 
filename = '@TheTraeYoung.csv'
filename2 = '@KingJames.csv'
filename3 = '@JHarden13.csv'
filename4 = '@ATLHawks.csv'
filename5 = '@BrooklynNets.csv'
filename6 = '@Lakers.csv'

