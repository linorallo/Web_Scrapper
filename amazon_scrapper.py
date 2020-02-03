import bs4
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
import csvWriter
searchString = "moto"
blockWords = ["None", 'screen', 'Protector', 'case', 'film']
searchPageDepth = 4
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
            urlSite = 'https://www.amazon.com' + str(page_soup.find('li', {'class':'a-last'}).a['href']) + '/'
            webSite = urlReq(urlSite)
            html = webSite.read()
            webSite.close()
            page_soup = soup(html, 'html.parser')
    itemsWhole = page_soup.findAll('span',{'cel_widget_id':'SEARCH_RESULTS-SEARCH_RESULTS'})
    for item in itemsWhole:
        text = str(item.find('span',{'class':'a-size-medium a-color-base a-text-normal'}))
        blockedItem = False
        for blockedWord in blockWords:
            if blockedWord in text:
                blockedItem = True
        if blockedItem == False:
            name=text.strip('<span class="a-size-medium a-color-base a-text-normal" dir="auto">').strip('</')
            if (item.find('free') or item.find('FREE')):
                price = fullPrice = '0'
            else:
                price = str(item.find('span',{'class':'a-price-whole'})).strip('<span class="a-price-whole">').strip('<span class="a-price-decimal">.</span></ $').replace(' ','')
                fullPrice = str(item.find('span',{'class':'a-offscreen'})).strip('<span class="a-offscreen"></span> $ N').replace(' ','')
            if float(fullPrice) - float(price) > 1:
                discount = str(100-(float(price)*100/float(fullPrice))) + '%'
            else:
                discount = 'N/A'
            itemNumber = str(len(results))
            link = 'amazon.com' + item.find('div',{'class':'a-row a-size-base a-color-base'}).a['href'] + '/'
            results.append((itemNumber, price, name, link, discount))
            print("item #"+ itemNumber +": "+ name +" $"+ str(price) + 'off' + discount)
    currentPage=currentPage+1
csvWriter.writeOut(results, searchString)
                
    