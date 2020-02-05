import bs4
import sortResults
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
def searchInNewegg(searchString, blockedWord, searchPageDepth, sortPreference):
    searchString = searchString.replace(' ','+')
    results=[]
    currentPage = 1
    while currentPage <= searchPageDepth : 
        if currentPage != 0 :
            if currentPage <= (searchPageDepth + 1) : 
                urlSite = "https://www.newegg.com/p/pl?d=" + searchString + "&Page=" + str(currentPage)
                webSite = urlReq(urlSite)
                html = webSite.read()
                webSite.close()
                page_soup = soup(html, 'html.parser')
        itemsWholeGrid = page_soup.find('div',{'class':'items-view is-grid'})
        itemsWhole = itemsWholeGrid.findAll('div',{'class':'item-container'})
        for item in itemsWhole:
            def itemAnalysis():
                print('--------------------------------')
                text = item.find('div',{'class':'item-info'})
                name=str(text.find('a',{'class':'item-title'}).text)
                price = str(text.find('li',{'class':'price-current'}))[78:85].strip('</strong>').replace(',','')
                discount = str(text.find('span',{'class':'price-save-percentage'}))
                itemNumber = str(len(results)+1)
                link = text.a['href']
                if len(discount) <2 :
                    discount = '0%'
                results.append((itemNumber, price, name, link, discount))
                print("item #"+ itemNumber +": "+ name +" $"+ str(price) + " OFF " + discount)  
            bWordFound=0
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

        