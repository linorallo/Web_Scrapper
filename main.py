import threading
import amazon_v2
import newegg_scrapper
import mercadolibre_scrapper
import sortResults
import csvWriter
import db
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
    while True :
        choiceAmazon = input('Search in Amazon? y/n ').capitalize()
        if  choiceAmazon == 'Y' :
            #implemnt threading
            amazonResults = amazon_v2.searchInAmazon(searchString,blockWords,searchPageDepth, sortPreference,currency)
            results = amazonResults
            break
        elif choiceAmazon == 'N' :
            break
        else :
            continue
    while True :
        choiceNewegg = input('Search in Newegg? y/n ').capitalize()
        if  choiceNewegg == 'Y' :
            #implemnt threading
            neweggResults = newegg_scrapper.searchInNewegg(searchString,blockWords,searchPageDepth, sortPreference,currency)
            results = results + neweggResults
            break
        elif choiceNewegg == 'N' :
            break
        else :
            continue    
    while True :
        choiceML = input('Search in Mercado Libre? y/n ').capitalize()
        if  choiceML == 'Y' :
            #implemnt threading
            mercadoLibreResults = mercadolibre_scrapper.searchInMercadoLibre(searchString,blockWords,searchPageDepth, sortPreference,currency)
            results = results + mercadoLibreResults
            break
        elif choiceML == 'N' :
            break
        else :
            continue
    
    print('Search initiated... (implement animation)')
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





#neweggThread = threading.Thread( newegg_scrapper.searchInNewegg, args=(searchString,blockWords,searchPageDepth, sortPreference))

#amazonThread = threading.Thread( amazonResults = amazon_v2.searchInAmazon, args=(searchString,blockWords,searchPageDepth, sortPreference))
#neweggThread.start()
#amazonThread.start()
