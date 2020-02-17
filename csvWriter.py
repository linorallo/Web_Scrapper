import csv
minResultPrice = 100000000000000000
minResultItemNum = ''
def minResult(results):
    for result in results:
            if result[1] < minResultPrice :
                minResultPrice = result[1]
                minResultItemNum = result[0]
                print('Cheapest choice: item #' + minResultItemNum + ' @ $' + str(minResultPrice))
def writeOut(results, searchString):
    print ('Entro a csvWriter')
    with open(searchString+".cvs", mode='w') as csv_file:
            fieldnames=['item #','price','title', 'discount', 'link',]
            writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                try:
                    writer.writerow({'item #':result[0],'price':result[1],'title':result[2], 'discount':result[4], 'link' : result[3]})    
                except UnicodeEncodeError :
                    print('UnicodeEncodeError')
                #writer.write