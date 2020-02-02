import bs4
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
import csv
searchString = "samsung"
blockWords = ["None", 'screen', 'Protector', 'case', 'film']
searchPageDepth = 2
currentPage = 0
urlSite = "https://listado.mercadolibre.com.ar/" + searchString +'/'
webSite = urlReq(urlSite)
html = webSite.read()
webSite.close()
page_soup = soup(html, 'html.parser')
results=[]
while currentPage < searchPageDepth : 
    if currentPage != 0 :
        if currentPage <= searchPageDepth : 
            print('iterando por pagina: '+ str(currentPage))
            urlSite = str(page_soup.find('li', {'class':'andes-pagination__button andes-pagination__button--next'}).a['href'])
            webSite = urlReq(urlSite)
            html = webSite.read()
            webSite.close()
            page_soup = soup(html, 'html.parser')
    itemsWhole = page_soup.findAll('li',{'class':'results-item highlighted article stack product'})
    print(len(itemsWhole))
    for item in itemsWhole:
        text = str(item.find('span', {'class':'main-title'}))
        blockedItem = False
        for blockedWord in blockWords:
            if blockedWord not in text:
                blockedItem = False
            else:
                blockedItem = True
        if blockedItem == False:
            name=text.strip('<span class="main-title"> ').strip('</span>')
            price = str(item.find('span',{'class':'price__fraction'})).strip('<span class="price__fraction">').strip('</span')
            discount = str(item.find('div',{'class':'item-discount'})).strip('<div class="item-discount">').strip('</div>')
            itemNumber = str(len(results))
            link = item.a['href']
            results.append((itemNumber, price, name, link, discount,))
            print("item #"+ itemNumber +": "+ name +" $"+ str(price))
    currentPage=currentPage+1
    with open(searchString+".cvs", mode='w') as csv_file:
        fieldnames=['item #','price','title', 'link']
        writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            #writer.writerow(result[int(itemNumber)])
            writer.writerow({'item #':result[0],'price':result[1],'title':result[2], 'link' : result[3]})
                
    