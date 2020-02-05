import bs4
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
import sortResults
def searchInMercadoLibre(searchString, blockedWord, searchPageDepth, sortPreference, currency):
    searchString = searchString.replace(' ','+')
    currentPage = 0
    if currency == 'USD' :
        urlSite = 'http://www.dolarhoy.com/'
        webSite = urlReq(urlSite)
        html = webSite.read()
        webSite.close()
        page_soup = soup(html, 'html.parser')
        usdContainer = page_soup.find('div',{'class':'pill pill-coti'})
        usdCompra = str(usdContainer.findAll('span')[1:2])[23:30].strip('</').replace(',','.')
    urlSite = "https://listado.mercadolibre.com.ar/" + searchString +'/'
    webSite = urlReq(urlSite)
    html = webSite.read()
    webSite.close()
    page_soup = soup(html, 'html.parser')
    results=[]
    while currentPage < searchPageDepth : 
        if currentPage != 0 :
            if currentPage <= searchPageDepth : 
                urlSite = str(page_soup.find('li', {'class':'andes-pagination__button andes-pagination__button--next'}).a['href'])
                webSite = urlReq(urlSite)
                html = webSite.read()
                webSite.close()
                page_soup = soup(html, 'html.parser')
        itemsWhole = page_soup.findAll('li',{'class':'results-item highlighted article stack product'})
        print(len(itemsWhole))
        for item in itemsWhole:
            def itemAnalysis():
                #print('--------------------------------')
                text = str(item.find('span', {'class':'main-title'}))
                name=text.strip('<span class="main-title"> ').strip('</span>')
                price = str(item.find('span',{'class':'price__fraction'}))[29:36].strip('</span>').replace('.','')
                if len(price)<1 :
                    price = str(item.find('div',{'class':'pdp_options__text pdp_options--no-margin'}))[63:70].strip('.').strip('<')
                if currency == 'USD' :
                    #print('PRECIO: '+ str(float(price))+' '+str(float(usdCompra)))
                    price = str(float(price) / float(usdCompra))
                discount = str(item.find('div',{'class':'item-discount'}))[0:4].strip('</div>')
                if discount == 'None' : 
                    discount = 'N/A'
                itemNumber = str(len(results))  
                link = item.a['href']
                results.append((itemNumber, price, name, link, discount,))
                #print("item #"+ itemNumber +": "+ name +" $"+ price + ' OFF: '+ discount )
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
