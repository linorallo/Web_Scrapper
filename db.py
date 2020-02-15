import mysql.connector 
import dbScripts
def connectDB() :
    try:
        db = mysql.connector.connect(user = 'root', password = '1308',  host = '127.0.0.1', database = 'mydb')
        print('DataBase accessed')
    except db.Error as err:
        print(err)
    return db 
    
def saveToDB(results):
    db = connectDB()
    cursor = db.cursor()
    cursor.execute(dbScripts.retrieveAll())
    retrieved = cursor.fetchall()
    addProduct = ('INSERT INTO product (itemNumber, productPrice, productName , productLink, productDiscount, productDiscoverDate, store_idstore) VALUES (%s, %s, %s , %s , %s, %s , %s)')
    #cursor.executemany(addProduct, results)
    print('-----------------------------------------')
    addedItemCount = 0 
    for result in results :
        if result[3]  in str(retrieved) :
            for item in retrieved:
                if result[3] in item :
                    if result[1] in item :
                        pass
                    else :
                        cursor.execute(dbScripts.updatePriceProduct(result[3],result[1]))
        else:
            cursor.execute(addProduct, result)
            addedItemCount += 1
    skippedItemCount = len(results) - addedItemCount     
    #cursor.execute(dbScripts.deleteDuplicates())
    db.commit()
    cursor.close()
    print(str(addedItemCount) + ' items were inserted to database; ' + str(skippedItemCount) + ' items were skipped')
    print('-----------------------------------------')

def readFromDB(searchList, blockedWords) :
    db = connectDB()
    cursor = db.cursor()
    cursor.execute(dbScripts.searchProducts(searchList,blockedWords))
    results = cursor.fetchall()
    return results

