import bs4
import sortResults
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
def searchInAmazon(searchString, blockedWord, searchPageDepth, sortPreference, currency):
    searchString = searchString.replace(' ','+')
    currentPage = 0
    urlSite = "https://www.amazon.com/s?k=" + searchString + "&ref=nb_sb_noss_2"
    webSite = urlReq(urlSite)
    html = webSite.read()
    webSite.close()
    page_soup = soup(html, 'html.parser')
    results=[]
    while currentPage < searchPageDepth : 
        if currentPage != 0 :
            if currentPage <= searchPageDepth : 
                urlSite = 'https://amazon.com' + str(page_soup.find('li', {'class':'a-last'}).a['href']) + '/'
                webSite = urlReq(urlSite)
                html = webSite.read()
                webSite.close()
                page_soup = soup(html, 'html.parser')
        itemsWhole = page_soup.findAll('span',{'cel_widget_id':'SEARCH_RESULTS-SEARCH_RESULTS'})
        for item in itemsWhole:
            def itemAnalysis():
                if 'App' and 'Prime Video' not in str(item):
                    text = str(item.find('span',{'class':'a-size-medium a-color-base a-text-normal'}))
                    #print('--------------------------------')
                    name=text.strip('<span class="a-size-medium a-color-base a-text-normal" dir="auto">').strip('</')
                    if (item.find('free') or item.find('FREE')):
                        price = fullPrice = '0'
                    else:
                        #print(name)
                        price = str(item.find('span',{'class':'a-price-whole'}))[28:37].strip('<span class')
                        fullPrice = str(item.find('span',{'class':'a-offscreen'}))[27:36].strip('</span ')
                        try:
                            if float(fullPrice) - float(price) > 1:
                                discount = str(100-(float(price)*100/float(fullPrice))) + '%'
                            else:
                                discount = 'N/A'  
                        except ValueError:
                            discount = 'N/A'     
                    itemNumber = str(len(results))
                    link = 'https://amazon.com' + item.find('div',{'class':'a-row a-size-base a-color-base'}).a['href'] + '/'
                    results.append((itemNumber, price, name, link, discount))
                    #print("item #"+ itemNumber +": "+ name +" $"+ str(price) + ' OFF ' + discount +' !')
            bWordFound = 0
            for bWord in blockedWord:
                if bWord in str(item):  
                    bWordFound+=1
            if bWordFound == 0 :
                itemAnalysis()
        currentPage=currentPage+1
    if sortPreference == 'Increasing' :
        return sortResults.sortIncreasing(results)
    if sortPreference == 'Decreasing' :
        return sortResults.sortDecreasing(results)