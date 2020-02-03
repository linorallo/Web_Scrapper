import csv
def writeOut(results, searchString):
    print ('Entro a csvWriter')
    with open(searchString+".cvs", mode='w') as csv_file:
            fieldnames=['item #','price','title', 'discount', 'link',]
            writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow({'item #':result[0],'price':result[1],'title':result[2], 'discount':result[4], 'link' : result[3]})
                
    