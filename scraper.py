# Alias python3
# Always type PYTHON3 INSTEAD OF PYTHON!
# importing libraries
from bs4 import BeautifulSoup
import urllib.request
import re

url = "http://www.pinocchiospizza.net/menu.html"
try:
    menu = urllib.request.urlopen(url)
except:
    print("An error occured.")

soup = BeautifulSoup(menu, "html.parser")

# print([type(item) for item in list(soup.children)])

element = re.compile('foodmenu')
content_list = soup.find_all('td', attrs={'class': element})
print(content_list)