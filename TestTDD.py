# http://175.24.111.140:8080
from selenium import webdriver
browser=webdriver.Firefox()
browser.get('http://localhost:8000')
assert 'Django' in browser.title
