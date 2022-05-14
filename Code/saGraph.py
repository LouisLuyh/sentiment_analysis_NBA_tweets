
import sentimentAnalysis as sa 
import matplotlib.pyplot as plt

# saGraph.py draw the piechart the displays the percentage of samples' comments in three categories

fn = sa.filename # can substitute filename to filename2, filename3, filename4, filename5, or filename6

result, compound = sa.sentimentAnalysis(fn) 
CompoundAverageNum, PositiveNum, NegativeNum, NeutralNum, CommentNum = sa.graphData(result, compound)


Positive_percent = PositiveNum/CommentNum   
Negative_percent = NegativeNum/CommentNum
NeutralNum_percent =NeutralNum/CommentNum
plt.figure()
# the precentage label
labelsPie =['Positive','Negative','NeutralNum']
# calculate percentage
x = [Positive_percent,Negative_percent,NeutralNum_percent]
# draw the pie chart
plt.pie(x,labels=labelsPie,autopct='%.2f%%' )
plt.axis('equal')
# store the pie chart into Figures directory
plt.savefig('./Figures/'+fn+'.jpg')
# title of the picture
plt.title(fn)


plt.show()


