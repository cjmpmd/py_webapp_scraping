import time, openpyxl, json, os ,string,random
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from ady_func import printer
load_dotenv()

# This module orchestrates the export from the scraped data stored in the arrays to a
# custom xslx template

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
def create_audit(fid,vitals,case_data,details,full_notes,meds,driver,mode):
    
    file_name = os.getenv('excel_template')
    srcfile = openpyxl.load_workbook(file_name, read_only=False, keep_vba=False)
    # AUDIT NAME
    time.sleep(3)
    file_name = driver.find_element(by=By.CSS_SELECTOR , value='div.project-name-edit-btn-content>h1').text.strip(' ').strip()
    print('')
    printer('############ CASE: '+file_name.capitalize()+'    ########################')
    print('')
    printer('Creating audit...')
    printer('Creating Q6...')
    srcfile['Q6']['B1'] = details[1] + ' ' + details[3]
    srcfile['Q6']['B2'] = vitals[8] #DOL
    srcfile['Q6']['B3'] = case_data[0][0]
    srcfile['Q6']['D2'] = vitals[9] #SOL
    srcfile['Q6']['D3'] = vitals[3]

    srcfile['Q6']['A9'] = vitals[2] #TYPE
    srcfile['Q6']['B9'] = vitals[0] #TIER
    srcfile['Q6']['C9'] = vitals[1] #RANK
    srcfile['Q6']['D9'] = vitals[15] #PHASE

    srcfile['Q6']['A12'] = vitals[10]
    srcfile['Q6']['A15'] = vitals[12].replace(',000','').replace('$','')
    srcfile['Q6']['A18'] = vitals[13].replace(',000','').replace('$','')
    srcfile['Q6']['A18'] = vitals[14]
    srcfile['Q6']['C21'] = vitals[11] + ' according to fv (DELETE)'
    # srcfile['Q6']['B1'] = details[1][4]
    printer('Facting...')
    srcfile['Facts']['A2'] = case_data[1]

    printer('CheckListing...')
    srcfile['Checklist']['C1'] = ''
    srcfile['Checklist']['C2'] = ''
    srcfile['Checklist']['C3'] = file_name
    srcfile['Checklist']['C4'] = vitals[8]
    srcfile['Checklist']['C5'] = details[0] #DOL
    srcfile['Checklist']['C8'] = case_data[0][4] #TCR #MISSING OTHER TYPES
    srcfile['Checklist']['C12'] = case_data[0][5] #911
    srcfile['Checklist']['C44'] = case_data[0][7] #EDR

    srcfile['Checklist']['F2'] = vitals[15] #PHASE
    srcfile['Checklist']['F3'] = vitals[0] #TIER
    srcfile['Checklist']['F4'] = vitals[1] #RANK
    srcfile['Checklist']['F5'] =  vitals[8] +' - '+ vitals[9] #DOL/SOL

    printer('Creating MEDS...')

    if len(meds)>0:
        rower = 2
        for med in meds:

            srcfile['Meds']['B'+str(rower)] = med[0]
            srcfile['Meds']['C'+str(rower)] = med[1]
            srcfile['Meds']['D'+str(rower)] = med[2]
            srcfile['Meds']['F'+str(rower)] = med[3]
            srcfile['Meds']['G'+str(rower)] = med[10]+' '+med[11]+' '+med[12]+' '+med[13]
            rower= rower+1
    
    printer('Creating FileVine Notes...')
    FV = 'FV Notes'
    srcfile[FV]
    cell_count=2
    
    srcfile[FV]['A1'] = 'ID'
    srcfile[FV]['B1'] = 'G-ID'
    srcfile[FV]['D1'] = 'POSTED BY'
    srcfile[FV]['E1'] = 'DATE'
    srcfile[FV]['F1'] = 'TIME'
    srcfile[FV]['G1'] = 'Type'
    comm_count = 1
    
    printer('#### SAVING each note')
    if(mode==1):
       # Initialize categories to hold matched note strings
        categories = {
            "SR": '',
            "LIEN": '',
            "APPRAISAL": '',
            "LORDEF": '',
            "LORCL": '',
            "LOADEF": '',
            "LOACL": '',
            "AUDIT": ''
        }

        # Define matching criteria for each category
        conditions = {
            "SR": ["SR"],
            "LIEN": ["LIEN"],
            "APPRAISAL": ["Appraisal"],
            "LORDEF": ["LOR", "DEF"],
            "LORCL": ["LOR", ("CL", "PL")],
            "LOADEF": ["LOA", "DEF"],
            "LOACL": ["LOA", ("CL", "PL")],
            "AUDIT": ["Audit"]
        }

        def matches(note_text: str, keywords: list) -> bool:
            """Check if note text contains required keywords."""
            for keyword in keywords:
                if isinstance(keyword, tuple):
                    if not any(term in note_text for term in keyword):
                        return False
                elif keyword not in note_text:
                    return False
            return True

        def process_notes(full_notes, srcfile, FV: str, cell_count: int, comm_count: int):
            """Process notes and assign to srcfile based on conditions and categories."""
            
            for note in full_notes:
                note_text = note[1]
                
                # Categorize note text based on conditions
                for category, keywords in conditions.items():
                    if matches(note_text, keywords):
                        categories[category] += '~~' + note_text + '\n'

                # Write category results to srcfile based on their mappings
                srcfile['Checklist']['C17'] = categories["APPRAISAL"]
                srcfile['Checklist']['C19'] = categories["SR"]
                srcfile['Checklist']['C28'] = categories["LIEN"]
                srcfile['Checklist']['C48'] = categories["LORDEF"]
                srcfile['Checklist']['C49'] = categories["LOADEF"]
                srcfile['Checklist']['C54'] = categories["LORCL"]
                srcfile['Checklist']['C55'] = categories["LOACL"]
                srcfile['Checklist']['C60'] = categories["AUDIT"]
                srcfile['Q6']['G3'] = categories["AUDIT"]

                # Assign note data to srcfile cells
                srcfile[FV][f'A{cell_count}'] = comm_count
                srcfile[FV][f'B{cell_count}'] = note[0]
                srcfile[FV][f'C{cell_count}'] = note_text
                srcfile[FV][f'D{cell_count}'].number_format = 'mm/dd/yyyy'
                srcfile[FV][f'D{cell_count}'] = note[2][0].replace('Posted By ', '').strip('/n')
                srcfile[FV][f'E{cell_count}'] = note[2][1]
                srcfile[FV][f'F{cell_count}'] = note[2][2].strip().strip('\n')
                srcfile[FV][f'H{cell_count}'] = note[2][3]

                # Increment cell and comment counters
                cell_count += 1
                comm_count += 1

            return cell_count, comm_count

    #OWN REFERENCE
        printer('#### Notas totales + comments: ' + str(len(full_notes)))
    srcfile['Q6']['G2'] = fid # LOR DEF 
    file_name = file_name.upper()
    project_path = os.getenv('PROJECT_PATH')
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    file_name_final = project_path+'/'+file_name+' '+fid+' Audit.xlsx'
    srcfile.save(file_name_final)
    print('')
    printer('############ AUDIT COMPLETED '+file_name+' CASE ID: '+fid+'  ###############')
    print('')
   
    # If you want to write the JSON data to a file, you can do this:
    with open(project_path+'/'+file_name+' '+fid+'.txt', "w") as outfile:
        json.dump(full_notes, outfile)
    return project_path
# project-activity-list