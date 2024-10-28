import os, time, logging, time, chromedriver_autoinstaller

from dotenv import load_dotenv
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chromedriver_autoinstaller.install()

# CUSTOM MODULES
import login_mod, loop_notes, vitals_mod, details_mod, med_tab_mod, webapi_mod
from ady_func import printer
from ady_func import idd

import notes_exporter
import case_info_mod

load_dotenv() 

# Main controller: orchestrates the webscraping and calls the web API to store in the database
def start(mode, fid):

    fid = str(fid)
    print('')
    printer('Case ID to summarize: '+fid)
    print('')

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    fid = str(fid)
    logging.info('Case ID to summarize: %s', fid)

    action_count = 1
    printer('INITIATING...')
    printer('Creating case info temporary holder')
    case_meta = []
    case_info =[]

    # 11283027
    # ################################################################################
    # # APP META
    perf_time = []
    date_start = time.strftime('%Y-%m-%d %H:%M:%S')

    perf_time.append(date_start)
        
    # ################################################################################
    # # APP START & LOGIN
    printer('Logging in')
    url= url(os.getenv('login_url'))
    #  Driver load and settings
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    login_mod.login(url,driver,url)
    process_file(fid,driver,mode)
    date_end = time.strftime('%Y-%m-%d %H:%M:%S')

    perf_time.append(date_end)
    print('')
    print('Performance details')
    print(perf_time)

def process_file(fid,driver,mode): 
    main_url = os.getenv('main_url')
    case_url = urljoin(main_url, f"{fid}/activity")
    case_detils = urljoin(main_url, f"/#/project/{fid}/custom/collisioninfo10193")
    med_tab_url= urljoin(main_url, f"/#/project/{fid}/custom/meds10193?page=1")

    # ################################################################################
    # REDIRECT TO A SPECIFIC PROJECT
    printer('Redirecting to proyect') 
    driver.get(case_url)
    
    # ################################################################################
    # VITAL SIGNS PROCESSING 
    printer('Exploring Vitals') 
    vitals = (vitals_mod.vitals_drill(driver))

    # ################################################################################
    # DETAILS PROCESSING 
    printer('Exploring PL details') 
    details = details_mod.details_drill(driver)

    # ################################################################################
    # CASE DETAILS
    printer('Exploring Case details') 
    driver.get(case_detils)
    case_data = case_info_mod.case_details(driver)

    # ################################################################################
    # REDIRECT TO A SPECIFIC PROJECT
    printer('Redirecting to proyect') 
    driver.get(case_url)
    
    ################################################################################
    # DEFINE ACTION AND START LOOPING THROUGH NOTES 
    #Sleep to await page request load
    time.sleep(3) 
    printer('Exploring notes') 
    action = ActionChains(driver)
    def moder(mode):
        if(mode == 1):
            return loop_notes.find_notes(driver,action)
        if(mode == 2):
            return loop_notes.no_find_notes()
         
    full_notes = moder(mode)
    
    # ################################################################################
    # MED TAB PROCESSING 
    printer('Exploring MedTab')    
    driver.get(med_tab_url)
    meds = med_tab_mod.meds_drill(driver,fid)

    # ################################################################################
    # EXPORT AUDIT
    printer('Creating Audit...')
    main_location = notes_exporter.create_audit(fid,vitals,case_data,details,full_notes,meds,driver,mode)
    
    # ################################################################################
    # DB WEBAPP
    printer('Conectando con localhost webapp...')
    webapi_mod.dashboard(fid,vitals,case_data,details,full_notes,meds,main_location,mode)
    
    
    fid = []
    vitals = []
    case_data = []
    details = []
    full_notes = []
    meds = []
    main_location = ''
    

