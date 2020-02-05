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
            writer = csv.writer(csv_file, lineterminator='\n')
            #writer.writeheader()
            for result in results:
                writer.writerow(result)    
                #writer.write