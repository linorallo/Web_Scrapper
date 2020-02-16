import bs4
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
import sortResults
import datetime as date
mercadolibreDBPK = 2
def searchInMercadoLibre(searchString, blockedWord, searchPageDepth, sortPreference, currency):
    searchString = searchString.replace(' ','+')
    currentPage = 0
    datetime = date.datetime.now()
    if currency == 'USD' :
        urlSite = 'http://www.dolarhoy.com/'
        webSite = urlReq(urlSite)
        html = webSite.read()
        webSite.close()
        page_soup = soup(html, 'html.parser')
        usdContainer = page_soup.find('div',{'class':'pill pill-coti'})
        usdCompra = str(usdContainer.findAll('span')[1:2])[23:30].strip('</').replace(',','.')
        print('USD Compra= '+str(usdCompra))
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
        for item in itemsWhole:
            def itemAnalysis():
                #print('--------------------------------')
                text = str(item.find('span', {'class':'main-title'}))
                name=text.strip('<span class="main-title"> ').strip('</span>')
                #price = str(item.find('span',{'class':'price__fraction'}))[29:36].strip('</span>').replace('.','').replace(',','')
                try:
                    price = str(item.find('span',{'class':'price__fraction'}).text).replace('.','')
                except AttributeError as err:
                    price = str(item.find('div',{'class':'pdp_options__text pdp_options--no-margin'}).text.strip(' $ ').partition(' ')[0]).replace('.','')
                if currency == 'USD' :
                    price = float(price) / float(usdCompra)
                    price = str(round(price, 2))
                try:
                    discount = str(item.find('div',{'class':'item__discount'}).text).strip('% OFF')
                except AttributeError :
                    discount = '0'
                if discount == 'None' : 
                    discount = '0'
                itemNumber = str(len(results))  
                link = str(item.a['href'])
                if 'JM' in link:
                    link = link.partition('JM')[0]+'JM'
                else :
                    link = link.partition('?')[0]
                results.append((itemNumber, price, name, link.strip('https://'), discount, str(datetime), mercadolibreDBPK))
                #print("item #"+ itemNumber +": "+ name +" $"+ price + ' OFF: '+ discount )
            bWordFound = 0
            for bWord in blockedWord:
                if bWord in str(item):  
                    bWordFound+=1
            if bWordFound == 0 :
                itemAnalysis()
        currentPage=currentPage+1
        print('results in MercadoLibre :' + str(len(results)))
        if sortPreference == 'Increasing' :
            return sortResults.sortIncreasing(results)
        if sortPreference == 'Decreasing' :
            return sortResults.sortDecreasing(results)
