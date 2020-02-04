import bs4
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
def searchInNewegg(searchString, blockedWord, strictFilter, searchPageDepth):
    if len(blockedWord) > 0:
        blockedWordFilter = True
    else :
        blockedWordFilter = False
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
        itemsWhole = page_soup.findAll('div',{'class':'item-container'})
        for item in itemsWhole:
            def itemAnalysis():
                text = item.find('div',{'class':'item-info'})
                name=str(text.find('a',{'class':'item-title'}).text)
                price = str(text.find('li',{'class':'price-current'}).text)
                print('price: '+ price)
                discount = str(text.find('span',{'class':'price-save-percentage'}))
                print('discount: '+discount)
                itemNumber = str(len(results)+1)
                link = text.a['href']
                if len(discount) <2 :
                    discount = '0%'
                results.append((itemNumber, price, name, link, discount))
                print("item #"+ itemNumber +": "+ name +" $"+ str(price) + " OFF " + discount)  
            if blockedWordFilter == True :
                for bWord in blockedWord:
                    if bWord not in str(item):  
                        if strictFilter == True :
                            if searchString in str(item) :
                                itemAnalysis()    
                        else:
                            itemAnalysis()        
            else :
                if strictFilter == True :
                    if searchString  in str(item) :
                        itemAnalysis()    
                else:
                    itemAnalysis() 
        currentPage=currentPage+1
    return results
    #csvWriter.writeOut(results, searchString)

        