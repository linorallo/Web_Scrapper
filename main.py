import amazon_v2
import newegg_scrapper
searchString = "moto"
blockWords = ["None", 'screen', 'Protector', 'case', 'film']
strictFilter = False
searchPageDepth = 2
neweggResults = newegg_scrapper.searchInNewegg(searchString,blockWords,strictFilter,searchPageDepth)
#amazonResults = amazon_v2.searchInAmazon(searchString,blockWords,strictFilter,searchPageDepth)
#print(amazonResults)
