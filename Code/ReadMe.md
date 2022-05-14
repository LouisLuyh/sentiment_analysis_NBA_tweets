# CIS 400 Term Project
## Sentiment Analysis Regarding the Comparison between Performance of Basketball Players/Teams and Twitter Comments

- Install Tweepy ```pip install tweepy```
- Install NLTK ```pip install NLTK```
- Run ```Balldontlie_Fetch.py```, the program will output a text file to the Data directory that contains the data for each season and a graph into the Figures directory.
  - Starting line 176, comment out non-target name, uncomment target name
  - if hit rate limit, error message ```ValueError: x and y must have same first dimension, but have shapes (22,) and (9,)``` appears. Wait for 1 minute or 2 and re-run the program.
- Run ```tweets_fetch.py```, will generate CSV files that store the tweets.
  - On lines 12 and 13, substitute team names or player names.
- the ```sentimentAnalysis.py``` file has three functions, the ```findMostPN(result)``` can return the most positive and most negative results. Other functions will be called by the  ```saGraph.py``` file.
- Run ```saGraph.py```, will output a pie chart into the Figures directory
  - At line 8, substitute filename parameter with filename2, filename3, filename4, filename5, filename6
     