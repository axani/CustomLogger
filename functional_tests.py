#!/env/bin/python
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
browser = webdriver.Firefox(capabilities=firefox_capabilities, executable_path='libs/geckodriver')
browser.get('http://www.google.de')

assert 'Django' in browser.title

browser.quit()