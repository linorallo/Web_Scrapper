import amazon_v2
import newegg_scrapper
import sortResults
import csvWriter
searchString = "hp Ryzen"
blockWords = ['Celeron', 'i7']
sortPreference = 'Increasing'
searchPageDepth = 1
neweggResults = newegg_scrapper.searchInNewegg(searchString,blockWords,searchPageDepth, sortPreference)
amazonResults = amazon_v2.searchInAmazon(searchString,blockWords,searchPageDepth, sortPreference)
results = sortResults.sortIncreasing(neweggResults+amazonResults)
csvWriter.writeOut(results, searchString)
print('Search Completed')