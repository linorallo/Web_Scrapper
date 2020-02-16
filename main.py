import threading
from threading import *
import amazon_v2
import newegg_scrapper
import mercadolibre_scrapper
import sortResults
import csvWriter
import db
import queue
class searchAmazon(Thread):
    def __init__(self, threadID, name, counter, *args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.args = args
    def run(self) :
        print('Amazon thread initiated...')
        resultQueue = self.args[0][0]
        searchParameters = self.args[0][1]
        resultQueue.put(amazon_v2.searchInAmazon(searchParameters[0],searchParameters[1],searchParameters[2],searchParameters[3],searchParameters[4], ))

class searchNewegg(Thread):
    def __init__(self, threadID, name, counter, *args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.args = args
    def run(self) :
        print('Newegg thread initiated...')
        resultQueue = self.args[0][0]
        searchParameters = self.args[0][1]
        resultQueue.put(newegg_scrapper.searchInNewegg(searchParameters[0],searchParameters[1],searchParameters[2],searchParameters[3],searchParameters[4], ))
class searchMercadoLibre(Thread):
    def __init__(self, threadID, name, counter, *args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.args = args
    def run(self) :
        print('Mercado_libre thread initiated...')
        resultQueue = self.args[0][0]
        searchParameters = self.args[0][1]
        resultQueue.put(mercadolibre_scrapper.searchInMercadoLibre(searchParameters[0],searchParameters[1],searchParameters[2],searchParameters[3],searchParameters[4], ))
print('------------------------------')
searchList = []
blockWords = []
print('Enter to coninue')
while True :
    searchString = str(input('SEARCH: '))
    if searchString == '' :
        break
    else :
        searchList.append(searchString)
        continue
choiceBlockWords=searchChoice=''
while True :
    choiceBlockWords = input('Want to block some not related results? y/n ')
    if choiceBlockWords.capitalize() == ('Y') :
        
        print('Press enter to continue')
        while True :
            blockWordInput = input('->')
            if blockWordInput == '' :
                break
            else :
                blockWords.append(blockWordInput)
        if blockWordInput == '' :
            break
    elif choiceBlockWords.capitalize() == 'N' :
        break
    else :
        continue   
#MAKE SEARCH START IN DATABASE AND THEN ASK IF SHOULD EXTEND IT ONLINE
print('Choose 1 for DataBase search or 2 for new Online search: ')
while True :
    searchChoice = int(input('Selection: '))
    if searchChoice == 1 :
        break
    elif searchChoice == 2:
        break
    else :
        continue
if searchChoice == 1 :
    print('Search initiated... (implement animation)')    
    results = db.readFromDB(searchList, blockWords)
    for result in results :
        sortResults.sortIncreasing(results)
    while True :
        extendOnlineChoice = input('Would you like to exten the search online? y/n ')
        if extendOnlineChoice.capitalize() == 'Y' :
            searchChoice = 2
            break
        elif extendOnlineChoice.capitalize() == 'N' :
            break
        else :
            continue
if searchChoice == 2 :
    sortPreference = 'Increasing'
    currency = 'USD'
    searchString = ''
    for searchWord in searchList :
        searchString = searchString + searchWord + ' '
    searchPageDepth = int(input('How many pages deep should i go? '))
    choiceAmazon=choiceNewegg=choiceML=''
    print('----- New Product Search -----') 
    results = []
    searchParameters=[searchString,blockWords,searchPageDepth, sortPreference,currency]
    outputQ = queue.Queue()
    while True :
        choiceAmazon = input('Search in Amazon? y/n ').capitalize()
        if  choiceAmazon == 'Y' :
            amazonThread = searchAmazon(1,'amazonThread',1,([outputQ,searchParameters]))
            amazonThread.start()
            break
        elif choiceAmazon == 'N' :
            break
        else :
            continue
    while True :
        choiceNewegg = input('Search in Newegg? y/n ').capitalize()
        if  choiceNewegg == 'Y' :
            neweggThread = searchNewegg(1,'neweggThread',1,([outputQ,searchParameters]))
            neweggThread.start()
            break
        elif choiceNewegg == 'N' :
            break
        else :
            continue    
    while True :
        choiceML = input('Search in Mercado Libre? y/n ').capitalize()
        if  choiceML == 'Y' :
            mercadolibreThread = searchMercadoLibre(1,'mercadolibreThread',1,([outputQ,searchParameters]))
            mercadolibreThread.start()
            break
        elif choiceML == 'N' :
            break
        else :
            continue
    print('Search initiated... (implement animation)')
    while True:
        if amazonThread.is_alive() == False :
            amazonThreadStatus = False
        else:
            amazonThreadStatus = True
        if neweggThread.is_alive() == False :
            neweggThreadStatus = False
        else:
            neweggThreadStatus =  True
        if mercadolibreThread.is_alive() == False :
            mercadolibreThreadStatus = False
        else:
            mercadolibreThreadStatus = True
        if amazonThreadStatus == False :
            if neweggThreadStatus == False :
                if mercadolibreThreadStatus == False:
                    break
    print('All threads closed')
    results = []
    queue_length = outputQ.qsize()
    for x in range(queue_length):
        results = results + outputQ.get()
    print('result"s lengt: ' + str(len(results)))
    results = sortResults.sortIncreasing(results)
    db.saveToDB(results)     
quantityShow = int(input('How many items do you wish to see? '))

print('-------------RESULTS------------------')
orderItem = 0
for result in results :
    orderItem+=1
    print(str(orderItem)+'- $'+ str(result[1]) +' / -'+ result[4]  +'% ' + result[2] + ' ; ' + result[3])
    if quantityShow == orderItem :
        print("***That's it***")
        break




