
import time
from selenium.webdriver.common.by import By
from ady_func import printer


def details_drill(driver):
    if driver.find_element(By.CLASS_NAME, "btn-project-header-avatar"):
        vitals_button = driver.find_element(by=By.CLASS_NAME, value ='btn-project-header-avatar')
        vitals_button.click()
        time.sleep(9)

        printer('Details opened...')
        contactPanelDateMonth = driver.find_element(by=By.ID, value ='contactPanelDateMonth-birthdate').get_attribute('value')
        contactPanelDateDay = driver.find_element(by=By.ID, value ='contactPanelDateDay-birthdate').get_attribute('value')
        contactPanelDateYear = driver.find_element(by=By.ID, value ='contactPanelDateYear-birthdate').get_attribute('value')

        contactPanelFirstName = driver.find_element(by=By.ID, value ='contactPanelFirstName').get_attribute('value')
        contactPanelMiddleName = driver.find_element(by=By.ID, value ='contactPanelMiddleName').get_attribute('value')
        contactPanelLastName = driver.find_element(by=By.ID, value ='contactPanelLastName').get_attribute('value')

        DOB = contactPanelDateMonth+'/'+contactPanelDateDay+'/'+contactPanelDateYear

        try:
            driver.find_elements(by=By.CSS_SELECTOR, value ='.nav-tabs>li')[1].click()
            driver.find_element(by=By.ID, value ='btn-contactPanel-cancel').click()
        except:            
            time.sleep(9)
            driver.find_elements(by=By.CSS_SELECTOR, value ='.nav-tabs>li')[1].click()
            driver.find_element(by=By.ID, value ='btn-contactPanel-cancel').click()
        
        details=[
            DOB,
            contactPanelFirstName,
            contactPanelMiddleName,
            contactPanelLastName,
            contactPanelFirstName +' '+  contactPanelMiddleName +' '+ contactPanelLastName,
            ]
        return details
    else:
        printer('Error: Details Blande NOT opened...')