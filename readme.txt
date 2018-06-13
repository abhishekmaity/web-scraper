I have used BeautifulSoup for parsing HTML, Gecko-driver in Selenium for the Firefox browser to make requests instead of scripts to Zomato website.

I have used BeautifulSoup because its an HTML parser. It helps one to navigate through the HTML data returned from however we want to fetch the data, and parse it in the format we specify.

List of files
-------------
1.restaurant_list.py
2.restaurant_scraper.py

3a.restaurant_details.txt	3b. zomato_bangalore.json

Running procedure
-----------------
The 'restaurant_list.py' is run which will collect all the URLs of individual restaurants listed on the web-page(s).
It will generate the 'restaurant_details.txt' containing the URLs

Next, the 'restaurant_scraper.py' is executed to collect all the information like name, rating, address, type of cuisines served, lat-long etc. from the restaurant pages stored in 'restaurant_details.txt'.   

Assumptions
-----------
Currently there are total 592 pages each having around 10 restaurants for bangalore zomato website. For this assignment I have decided to navigate only first 3 pages.
        
Output
------
The output is saved in python dictionary in the program and dumped finally in a json named 'zomato_bangalore.json'

