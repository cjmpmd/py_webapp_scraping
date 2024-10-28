
import time
from asyncio.windows_events import NULL
from selenium.webdriver.common.by import By
from ady_func import printer

def vitals_drill(driver):
    tSleep = 3.5
    time.sleep(tSleep)
    printer('Finding vitals')
    vitals_btn = 'fvs-button fvs-button--primary fvs-button--trailing-icon svelte-x4x5bc'
    str_error=''
    try:    
        time.sleep(tSleep)
        time.sleep(tSleep)
        vitals_button = driver.find_element(by=By.CLASS_NAME, value ='vitals-toggle')
        vitals_button.click()

    except:
        
        time.sleep(tSleep)
        time.sleep(tSleep)
        vitals_button = driver.find_element(by=By.CLASS_NAME, value ='vitals-toggle')
        vitals_button.click()     
    
    status =''
    if (len(driver.find_elements(by=By.CSS_SELECTOR , value='.select-button-text')) == 0):
        printer('---ERROR HANDLING: Waiting status to be readable.')
        time.sleep(5)
    status = driver.find_element(by=By.CSS_SELECTOR , value='.select-button-text').text
    vitals_button_close = driver.find_element(by=By.CLASS_NAME, 
        value ='close-button')

    vitalspanel = driver.find_element(by=By.CSS_SELECTOR, 
        value ='.vitals-panel')
    vitals_drillin_1 = vitalspanel.find_elements(by=By.TAG_NAME, 
        value ='span')
    
    time.sleep(4)

    vitals_list=[
    vitals_drillin_1[0].text,	# Specific data label, removed for privacy
    vitals_drillin_1[1].text,	# Specific data label, removed for privacy
    vitals_drillin_1[2].text,	# Specific data label, removed for privacy
    vitals_drillin_1[3].text,	# Specific data label, removed for privacy
    vitals_drillin_1[4].text,	# Specific data label, removed for privacy
    vitals_drillin_1[5].text,	# Specific data label, removed for privacy
    vitals_drillin_1[6].text,	# Specific data label, removed for privacy
    vitals_drillin_1[7].text,   # Specific data label, removed for privacy
    vitals_drillin_1[8].text,   # Specific data label, removed for privacy
    vitals_drillin_1[9].text,	# Specific data label, removed for privacy
    vitals_drillin_1[10].text,	# Specific data label, removed for privacy
    vitals_drillin_1[11].text,	# Specific data label, removed for privacy
    vitals_drillin_1[12].text,	# Specific data label, removed for privacy
    vitals_drillin_1[13].text,	# Specific data label, removed for privacy
    vitals_drillin_1[14].text,	# Specific data label, removed for privacy
    status,	

    ]
    time.sleep(tSleep)
    if(vitals_button_close != NULL):
        vitals_button_close.click()
        printer('Vitals closed...')
    printer('Exporting vitals...')
    return vitals_list