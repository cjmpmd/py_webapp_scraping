import time,string,random,datetime,time

from bs4 import BeautifulSoup
from openpyxl.utils import datetime as xl_utils_datetime
from selenium.webdriver.common.by import By

# Custom imports
from ady_func import printer

def convert_to_excel_date(date_string):
    try:
        date = datetime.datetime.strptime(date_string, "%m/%d/%Y")
        excel_date = xl_utils_datetime.to_excel(date)
        return excel_date
    except ValueError:
        print("Invalid date format")
        return None

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def meta_driller(meta):    
    meta.replace('Originally Posted by','').replace('Posted by','').strip(' ').replace(' ','').strip()
    meta.replace('Posted by ','').strip(' ').replace(' ','').strip()
    meta.replace('Originally ','').strip(' ').strip()
    name = meta.split(' on ')[0].strip(' ').strip()
    date = convert_to_excel_date(meta.split(' on ')[1].split(' at ')[0])
    time = meta.split(' on ')[1].split(' at ')[1]
    time2 = meta.split(' on ')[1].strip(' ').replace('at ','').replace('.','')
    
    meta_drill = [name,date,time,time2,]
    
    return meta_drill

def start_notes_loop(driver,action):
    time.sleep(3)
    activity_list = driver.find_elements(by=By.CSS_SELECTOR, value ='.fv-note-body')
    aLength = 0
    bLength = len(activity_list)
    bMax = len(activity_list) -1
    TEMP = loop_notes(driver, action, aLength,bLength,activity_list,bMax)
    
def loop_notes(driver, action, aLength,bLength,activity_list,bMax):
    aLength = bLength
    action.move_to_element(activity_list[bMax]).perform()
    activity_list = driver.find_elements(by=By.CSS_SELECTOR, value ='.fv-note-body')
    bLength = len(activity_list)
    bMax = len(activity_list) -1
    driver.execute_script("window.scrollTo(0, document.getElementsByClassName('page-content-container')[0].scrollHeight);")
    
    notes_found = '' 
    if (aLength<bLength):
        loop_notes(driver, action, aLength,bLength,activity_list,bMax)    
        time.sleep(5)
    
def note_id_wcomments(notes_w_comments):
    return ''

def no_find_notes():
    
    all_notes = []
    all_notes.append(['','', '',''])
    return all_notes 

def find_notes(driver, action):
    to_display = []
    activity_list_final = driver.find_elements(by=By.CSS_SELECTOR, value ='.fv-note-wrapper')
    printer('### Found ' + str(len(activity_list_final))+' note(s)')

    printer('Displaying note\'s comments...')
    printer('-- START')
    counter = 1
    if (len(driver.find_elements(by=By.CSS_SELECTOR, value='.fv-comment-count'))>0):
        notes_w_comments = len(driver.find_elements(by=By.CSS_SELECTOR, value='.fv-comment-count'))
        printer('---- Found '+str(notes_w_comments)+' note(s) with comments')
        note_id_wcomments(driver.find_elements(by=By.CSS_SELECTOR, value='.fv-comment-count'))
    # input('pauseee')
    count = 1
    for i in activity_list_final:
        if(len(i.find_elements(by=By.CSS_SELECTOR, value='.fv-comment-count'))>0):
            action.move_to_element(i).perform()
            time.sleep(2)
            gg = i.find_element(by=By.CSS_SELECTOR, value='.fv-comment-count')
            gg.click()
            printer('---- Comment '+str(count)+' clicked.')
            count = count + 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        
    printer('-- END')
    printer('Calling export of notes')
    
    time.sleep(10)

    page_source = driver.page_source
    soup_main = BeautifulSoup(page_source, features="lxml")
    notes = soup_main.find_all("note")
    all_notes = []
    ind_note = []
    printer('Found all notes..')
    note_counter = 1
    for i in notes:
        commnet_string = ''
        note_code = id_generator()
        note_counter +=1
        note_block = i.find_all('div',{'class' : 'note-body'})
        note = note_block[0].text.rstrip('\n').lstrip('\n').replace('"','--')
        note_code = note_block[0]['id']
        note_meta = i.find_all('div',{'class' : 'note-meta'})[0].text.strip("\n").strip('Originally Posted by').strip('Posted by').strip(' ').replace('n/a','')
        note_counter
        note_meta = meta_driller(note_meta)
        all_notes.append([note_code,note, note_meta,'N'])
        if (i.find_all('div',{'class' : 'fv-comment-count'})):
            comments_wrapper = i.find('div',{'class' : 'fv-comment-count'}).text.strip('\n').strip(' ')
            commnet_string = ' ----- Found comments: ' + comments_wrapper
            comment_body = i.find_all('div',{'class' : 'fv-comment-body'})
            for cb in comment_body:
                comment = cb.find('div',{'class' : 'note-body'}).text.strip('\n').strip(' ')
                comment_meta = str(cb.find('div',{'class' : 'note-meta'}).text.strip('\n').strip(' '))
                comment_meta = comment_meta.replace('Posted by','')
                comment_meta = meta_driller(comment_meta)
                all_notes.append([note_code,comment,comment_meta,'C'])

        printer('-- Note '+str(note_counter)+' Loop' + commnet_string)
    return all_notes
        