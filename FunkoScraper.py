
from bs4 import BeautifulSoup
import requests 
import pandas as pd
import schedule
import time
import smtplib
from email.message import EmailMessage

def send_text(subject, body,to):

    msg = EmailMessage()
    msg.set_content(body)
    msg['to']= to
    msg['subject'] = subject

    #Replace with gmail
    user = "user@gmail.com"
    msg['from'] = user

    #Replace with password
    password = "password"

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)

    server.quit()




def main():

    name_array = []
    price_array = []

    URL = 'https://firstformcollectibles.com/search?q=avatar+funko&type=product%2Cpage%2Carticle'

    html_text = requests.get(URL).text


    soup = BeautifulSoup(html_text, 'lxml')

    Product_cards = soup.find_all('div', class_ ='product-body' )

    for Products in Product_cards:

        Pop_name = Products.a.text
        
        Pop_price = Products.ins.text

        temp_String = Pop_price[1::]
        

        Num_price = float(temp_String)

        if Num_price < 20.00:
            print(Pop_name)
            print(Pop_price)

            name_array.append(Pop_name)
            price_array.append(Pop_price)

    data = {
        'Name' : name_array,
        'Price' : price_array
    }

    df = pd.DataFrame(data)

    custom_header = ['Name', 'Price']

    df.to_excel('output.xlsx', index=False)

    #Replace with number
    send_text("Update", "Your collectible spreadsheet is now ready to view", "number@tmomail.net")


#Runs program once a day
while 1:
    main()
    time.sleep(86400)
