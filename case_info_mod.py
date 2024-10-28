import time
from selenium.webdriver.common.by import By

def get_value_by_name(case_table, name):
    """Helper function to retrieve the value of an element by its name, returning 'N/A' if not found."""
    try:
        return str(case_table.find_element(By.NAME, name).get_attribute('value'))
    except Exception:
        return 'N/A'

def case_details(driver):
    time.sleep(15)  
    
    case_table = driver.find_element(By.CLASS_NAME, 'project-item-body')
    bb = driver.find_elements(By.CLASS_NAME, 'form-group')[1]
    DOL = bb.find_elements(By.TAG_NAME, 'input')[1].get_attribute('value')

    # Retrieve values using the helper function
    SUD = get_value_by_name(case_table, 'pendingdatesignupdate100232')
    LOC = get_value_by_name(case_table, 'locationofaccident100232')
    SOF = get_value_by_name(case_table, 'statementoffacts100232')
    POSITION = get_value_by_name(case_table, 'clientpositioninincident100232')
    TCR = get_value_by_name(case_table, 'trafficcollisionreporttcr100232')
    C911 = get_value_by_name(case_table, 'f_911call100232')
    PURPOSE = get_value_by_name(case_table, 'purposeoftrip100232')
    EDR = get_value_by_name(case_table, 'edr100232')

    # Handle default values
    C911 = C911 if C911 else 'Unknown'
    EDR = EDR if EDR else 'Unknown'

    # Construct the facts string
    facts = (
        f"a. Location / Time: {LOC}\n"
        f"b. Purpose of Trip: {PURPOSE}\n"
        f"c. Facts: {POSITION} {SOF}\n"
        "d. Witnesses / Passengers: \n"
        f"e. Evidence (TCR, Reports, RS, etc): (TCR: {TCR}) (911: {C911}) (EDR: {EDR})\n"
        "f. Course & Scope Investigation: "
    )

    case_data_drill = [SUD, LOC, SOF, POSITION, TCR, C911, PURPOSE, EDR, DOL]
    case_data = [case_data_drill, facts]

    return case_data