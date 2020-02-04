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
            urlSite = 'https://amazon.com' + str(page_soup.find('li', {'class':'a-last'}).a['href']) + '/'
            webSite = urlReq(urlSite)
            html = webSite.read()
            webSite.close()
            page_soup = soup(html, 'html.parser')
    itemsWhole = page_soup.findAll('span',{'cel_widget_id':'SEARCH_RESULTS-SEARCH_RESULTS'})
    for item in itemsWhole:
        text = str(item.find('span',{'class':'a-size-medium a-color-base a-text-normal'}))
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

    