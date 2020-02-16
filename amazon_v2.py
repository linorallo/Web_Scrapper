import bs4
import sortResults
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
import datetime as date
amazonDBPK = 3
def searchInAmazon(searchString, blockedWord, searchPageDepth, sortPreference, currency):
    datetime = date.datetime.now()
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
                    name=text.strip('<span class="a-size-medium a-color-base a-text-normal" dir="auto">').strip('</')
                    if (item.find('free') or item.find('FREE')):
                        price = fullPrice = '0'
                    else:
                        try:
                            price = str(item.find('span',{'class':'a-price-whole'}).text).replace(',','').strip('.')
                            fullPriceSpan = item.find('span',{'data-a-strike':'true'})
                            try:
                                fullPrice = str(fullPriceSpan.find('span',{'class':'a-offscreen'}).text).strip('$').partition('.')[0]
                            except:
                                fullPrice = price
                            try:
                                if fullPrice != price:
                                    discount = str(100 - round(float(price),2)*100/round(float(fullPrice),2)).partition('.')[0] 
                                    #print(discount)
                                else:
                                    discount = '0'  
                            except ValueError as err:
                                discount = '0'     
                            itemNumber = str(len(results))
                            link = ('amazon.com' + item.find('a',{'class':'a-link-normal a-text-normal'})['href']).partition('ref')[0]
                            results.append((itemNumber, price, name, link, discount, str(datetime), amazonDBPK))
                        except AttributeError as err:
                            pass
                            #print('Item Skipped in Amazon due to: ' +str(err))
                    
            bWordFound = 0
            for bWord in blockedWord:
                if bWord in str(item):  
                    bWordFound+=1
            if bWordFound == 0 :
                itemAnalysis()
        currentPage=currentPage+1
    print('results in Amazon :' + str(len(results)))
    if sortPreference == 'Increasing' :
        return sortResults.sortIncreasing(results)
    if sortPreference == 'Decreasing' :
        return sortResults.sortDecreasing(results)