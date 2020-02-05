
import threading
import amazon_v2
import newegg_scrapper
import mercadolibre_scrapper
import sortResults
import csvWriter
searchString = "hp Ryzen"
blockWords = ['Celeron', 'i7']
sortPreference = 'Increasing'
searchPageDepth = 1
currency = 'USD'
#neweggThread = threading.Thread( newegg_scrapper.searchInNewegg, args=(searchString,blockWords,searchPageDepth, sortPreference))
#neweggResults = neweggThread.result()
mercadoLibreResults = mercadolibre_scrapper.searchInMercadoLibre(searchString,blockWords,searchPageDepth, sortPreference,currency)
#neweggResults = newegg_scrapper.searchInNewegg(searchString,blockWords,searchPageDepth, sortPreference,currency)
#amazonResults = amazon_v2.searchInAmazon(searchString,blockWords,searchPageDepth, sortPreference,currency)

#amazonThread = threading.Thread( amazonResults = amazon_v2.searchInAmazon, args=(searchString,blockWords,searchPageDepth, sortPreference))
#neweggThread.start()
#amazonThread.start()
#results = sortResults.sortIncreasing(neweggResults+amazonResults + mercadoLibreResults)
results=mercadoLibreResults
csvWriter.writeOut(results, searchString)
print('Search Completed')