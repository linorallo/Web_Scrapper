import bs4
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
import csv
searchString = "s10"
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
            urlSite = 'amazon.com' + str(page_soup.find('li', {'class':'a-last'}).a['href']) + '/'
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
            price = str(item.find('span',{'class':'a-price-whole'})).strip('<span class="a-price-whole">').strip('<span class="a-price-decimal">.</span></')
            itemNumber = str(len(results))
            #link = 'amazon.com' + str(item.find('a', {'class':'a-size-base a-link-normal s-no-hover a-text-normal'})).strip('<a class="a-size-base a-link-normal s-no-hover a-text-normal" href="').strip(">")
            link = 'amazon.com' + item.find('div',{'class':'a-row a-size-base a-color-base'}).a['href'] + '/'
            results.append((itemNumber, price, name, link,))
            print("item #"+ itemNumber +": "+ name +" $"+ str(price))
    currentPage=currentPage+1
    with open(searchString+".cvs", mode='w') as csv_file:
        fieldnames=['item #','price','title', 'link']
        writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            #writer.writerow(result[int(itemNumber)])
            writer.writerow({'item #':result[0],'price':result[1],'title':result[2], 'link' : result[3]})
                
    