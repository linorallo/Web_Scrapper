import bs4
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup 
import csv
searchString = "asus"
blockWords = ["None", 'screen', 'Protector', 'case', 'film']
searchPageDepth = 4
results=[]
currentPage = 1
while currentPage < searchPageDepth : 
    if currentPage != 0 :
        if currentPage <= (searchPageDepth + 1) : 
            urlSite = "https://www.newegg.com/p/pl?d=" + searchString + "&Page=" + str(currentPage)
            webSite = urlReq(urlSite)
            html = webSite.read()
            webSite.close()
            page_soup = soup(html, 'html.parser')
    itemsWhole = page_soup.findAll('siv',{'class':'item-container'})
    for item in itemsWhole:
        text = str(item.find('div',{'class':'item-info'}))
        #if searchString in text :
        for blockedWord in blockWords:
            if blockedWord not in text:                
                name=text.a
                price = text.find('li',{'class':'price-current'}).strong
                itemNumber = str(len(results)+1)
                link = text.a['href']
                results.append((itemNumber, int(price), name, link,))
                print("item #"+ itemNumber +": "+ name +" $"+ str(price))
    currentPage=currentPage+1
minResultPrice = 100000000000000000
minResultItemNum = ''
with open(searchString+".cvs", mode='w') as csv_file:
    fieldnames=['item #','price','title', 'link']
    writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        #writer.writerow(result[int(itemNumber)])
        if result[1] < minResultPrice :
            minResultPrice = result[1]
            minResultItemNum = result[0]
        writer.writerow({'item #':result[0],'price':result[1],'title':result[2], 'link' : result[3]})
print('Cheapest choice: item #' + minResultItemNum + ' @ $' + str(minResultPrice))

    