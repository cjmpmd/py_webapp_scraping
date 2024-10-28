import os
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
load_dotenv()

def login(url,driver,fid):
    # Open the driver and pass the url
    driver.get(url)

    # Find the DOM elements from login form
    mail = driver.find_element(by=By.NAME, value ='Email')
    pss = driver.find_element(by=By.NAME, value ='Password')
    
    # Retreive redentials from env variables
    mEmail = os.getenv('mEmail') 
    mPassword = os.getenv('mPassword') 

    # Populate the login form
    mail.send_keys(mEmail)
    pss.send_keys(mPassword)
    
    # Submit login
    btn = driver.find_element(by=By.TAG_NAME, value ='button')
    btn.click()

    # Return response driver
    return driver