import pystache
import json
from bs4 import BeautifulSoup

print BeautifulSoup(pystache.render(open("main.stache").read(), json.loads(open("main.json").read()))).prettify()
