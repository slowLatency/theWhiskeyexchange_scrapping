# our aim in this project is to go to a ecommerce website and then scrape data about the products on that website and then take this data
# and store it in a excel file.
#We'll need the "Requests", "BeautifulSoup", "Pandas" Libraries for this project :)

import webbrowser
import requests
from bs4 import BeautifulSoup as bs 
import pandas as pd

#This main url will lead us to our e-commerce website later we'll just append the product links to this URL to go to the specific product page
main_url = "https://www.thewhiskyexchange.com"

Header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}


#now you might be thinking what is a header, this right here can also be called as a request header, 
# "Request headers contain more information about the resource to be fetched, or about the client(eg: the webbrowser in our case) 
# requesting the resource"
# we are using a diff URL over here to send request because this is the page where all our products are
# res=requests.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky', headers=Header).content


#now that we've sent a request to the URL and were able to get the response our aim will be to inspect the page and see where in the HTML code 
# can we get the links to the products from, as we get the links we'll store them so that we can traverse them and scrape those links to get
# info about our products 

# soup=bs(res,'html.parser')

# products=soup.find_all("li",{"class":"product-grid__item"})

product_links=[]
n=2
for i in range(1,n):

    res=requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={i}&psize=24&sort=pasc', headers=Header).content
    soup=bs(res,'html.parser')
    products=soup.find_all("li",{"class":"product-grid__item"})

    for product in products:
        links=product.find("a").get('href')
        product_links.append(main_url+links)

# product_names=[]
# product_pirces=[]
# product_ratings=[]
# product_status=[]
# product_description=[]

data=[]

for link in product_links:
    res=requests.get(link,headers=Header).content
    soup=bs(res,'html.parser')
    name=soup.find('h1',{"class":"product-main__name"}).text.replace('\n','')
    price=soup.find("p",{"class":"product-action__price"}).text
    try:
        description=soup.find("div",{"class":"product-main__description"}).find('p').text.replace('\n','')
    except:
        description=None
    
    try:
        rating=soup.find("p",{"class":"review-overview__content"}).find('span').text.replace('\n','')
    except:
        rating=None

    status=soup.find('p',{"class":"product-action__stock-flag"}).text

    whisky={'Name':name,'Price':price,'About':description,'Rating':rating,'Status':status,'Link to Product':link}
    data.append(whisky)

df=pd.DataFrame(data)

df.to_csv('D:\Python Projects\product_details.csv',index=True)


    