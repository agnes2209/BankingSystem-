import datetime
def createEntry(username,amount,type):
    statefile=open("acstatement.txt","a")
    currdate=datetime.datetime.now()
    
    currdate_con=str(currdate)
    statefile.write(username+" "+str(amount)+" "+type+" "+currdate_con+"\n")