
import time
from bs4 import BeautifulSoup
from ady_func import printer

def name_drill(name):
    h3 = name.find('h3',{'class': 'person-name'})
    site_name = h3.find('span',{'class': 'ng-binding'}).text
    md_name = ''
    if (h3.find('small',{'class': 'person-abbr-name'})):
        md_name = h3.find('small',{'class': 'person-abbr-name'}).text.replace(u'\xa0', u' ').strip().strip('(').strip(')')
    block_two = name.find('div',{'class': 'person-details'})
    try:
        a = block_two.find_all('a')
        for i in a:
            namu.append(i.text)
    except:
        print('No a-tag found for '+site_name)
    namu = [
        site_name,
        md_name,
    ]
    site_name = "\n".join(namu)
    final_nam = [
        site_name,
        md_name,
    ]
    return final_nam

def meds_drill(driver,fid):
    printer('Meds Search...')
    time.sleep(15)
    
    page_source = driver.page_source
    
    med = BeautifulSoup(page_source, features="lxml")
    
    if med.find('table',{'id' : 'collection-table'}):
        med = med.find('table',{'id' : 'collection-table'})
        trs = med.find_all('tr',{'class': 'custom-item'})
        meds_rows =[]
        for tr in trs:
            try:
            
                provider = name_drill(tr.find('div',{'class':'person-block-body'}))[0]
                provider_name = name_drill(tr.find('div',{'class':'person-block-body'}))[1]
                billedamount = tr.find('td',{'class':'billedamount100236'}).text.replace('n/a','').strip('').strip("\n")
                providertype = tr.find('td',{'class':'providertype100236'}).text.replace('n/a','').strip('').strip("\n")
                firstscheduledvisit = tr.find('td',{'class':'firstscheduledvisit100236'}).text.replace('n/a','').strip('').strip("\n")
                istheclientstilltreating = tr.find('td',{'class':'istheclientstilltreating100236'}).text.replace('n/a','').strip('').strip("\n")
                otherspecialty = tr.find('td',{'class':'otherspecialty100236'}).text.replace('n/a','').strip('').strip("\n")
                discharged = tr.find('td',{'class':'discharged100236'}).text.replace('n/a','').strip('').strip("\n")
                didclientattendfirstvisit = tr.find('td',{'class':'didclientattendfirstvisit100236'}).text.replace('n/a','').strip('').strip("\n")
                dateoffinaltreatment = tr.find('td',{'class':'dateoffinaltreatment100236'}).text.replace('n/a','').strip('').strip("\n")
                notes = tr.find('td',{'class':'notes100236'}).text.replace('n/a','').strip('').strip("\n")
                billingnotes = tr.find('td',{'class':'billingnotes100236'}).text.replace('n/a','').strip('').strip("\n")
                additionalnotes = tr.find('td',{'class':'additionalnotes100236'}).text.replace('n/a','').strip('').strip("\n")
                additionalnotes1 = tr.find('td',{'class':'additionalnotes1100236'}).text.replace('n/a','').strip('').strip("\n")
                creat = tr.find('td',{'class':'createdDate'}).text.replace('n/a','').strip('').strip("\n")
                billedamount.strip("n/a")
                
                temp_data = [
                    provider,
                    provider_name,
                    providertype,
                    billedamount,
                    firstscheduledvisit,
                    istheclientstilltreating,
                    otherspecialty,
                    discharged,
                    didclientattendfirstvisit,
                    dateoffinaltreatment,
                    notes,
                    billingnotes,
                    additionalnotes,
                    additionalnotes1,
                    creat,
                ]
                meds_rows.append(temp_data)
                temp_data =[]
                
            except:
                pass
        printer('#### ' + str(len(trs))+ ' Meds Found!')
    else:
        printer('#### No Meds table')
        meds_rows = []

    return meds_rows