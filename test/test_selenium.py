import time
from selenium import webdriver

wd = webdriver.Chrome('C:\\gachon2020\\chromedriver.exe')
wd.get('http://www.google.com')

time.sleep(2)
html = wd.page_source
print(html)

wd.quit()