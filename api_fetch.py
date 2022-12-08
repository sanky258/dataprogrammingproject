import requests
import csv
from flask import Flask
from views import views
import pyodbc
import time


app=Flask(__name__)
app.register_blueprint(views, url_prefix="/views")

no_data=True

while(True):
    time.sleep(10)
    #PART 1
    # app.run(debug=True)

    # url='http://api.coincap.io/v2/assets'

    # headers={
    #     'Accept': 'application/json',
    #     'Content-Type': 'application/json'
    #         }


    # response=requests.request("GET", url, headers=headers, data={})
    # myjson= response.json()


    # outdata=[]
    # csvheader=['SYMBOL', 'NAME', 'PRICE_IN_USD']

    # for x in myjson['data']:
    #     listing = [x['symbol'],x['name'],x['priceUsd']]
    #     outdata.append(listing)



    # with open('crypto.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer=csv.writer(f)

    #     writer.writerow(csvheader)
    #     writer.writerows(outdata)

    # print('done')

    #PART 2
    
    server = 'abcd2727.database.windows.net'
    database = 'abcd'
    username = 'adminn'
    password = '{Abc@12345}'   
    driver= '{ODBC Driver 17 for SQL Server}'
    connection=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    

    def Delete_all():
        cursor=connection.cursor()
        cursor.execute('''
                    TRUNCATE TABLE crypto 
                    
                ''')
        connection.commit()

    def Write_To_DB(connection,SYMBOL,COIN,PRICE_IN_USD):
    
        cursor=connection.cursor()
        cursor.execute('INSERT INTO crypto(SYMBOL, COIN, PRICE_IN_USD) VALUES(?,?,?);',(SYMBOL,COIN,PRICE_IN_USD))
    #     Read(connection)
        connection.commit()
    
    def Update_DB(connection,SYMBOL, COIN, PRICE_IN_USD):
        cursor=connection.cursor()
        cursor.execute('UPDATE crypto SET SYMBOL=(?), COIN= (?), PRICE_IN_USD=(?);',(SYMBOL,COIN,PRICE_IN_USD))
        # connection.commit()
    

    url='http://api.coincap.io/v2/assets'

    headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json'
            }


    response=requests.request("GET", url, headers=headers, data={})
    myjson= response.json()


    outdata=[]
    csvheader=['SYMBOL', 'NAME', 'PRICE_IN_USD']

    for x in myjson['data']:
        listing = [x['symbol'],x['name'],x['priceUsd']]
        outdata.append(listing)

    for i in outdata:
        SYMBOL=i[0]
        COIN=i[1]
        PRICE_IN_USD=i[2]

        
        if no_data:
            Write_To_DB(connection,SYMBOL,COIN,PRICE_IN_USD)
            no_data=False
        else:
            Update_DB(connection, SYMBOL, COIN, PRICE_IN_USD )
        


    