## pip install pandas
## pip install xlrd
## pip install unidecode
## pip install pyad
## pip install pywin32
## pip install openpyxl
import pyad  # For some reason it has to be imported like this                       
from pyad import adquery, adcomputer
import pandas as pd
import unidecode as ud
import datetime
import numpy as np

## Excel path
excel_file_path = (r'\\plwawfpa01\Groups\IS\SSM\assets\assets.xlsx')

## Excel columns name mapping
type_of_asset = 'Equipment type'
name = 'First name'
surname = 'Last name'
purchase_date = 'Purchase date'
comment = 'Comments'
part_number = 'PN'
manufacturer = 'Manufacturer'
model = 'Model'
serial_number = 'Serial Number'
status = 'Status'

## AD filter settings
attributes_ad = ["Name", "description"]
where_clause_ad = "objectClass = '*'"
base_dn_ad = "OU=PLWA,OU=wkswin10,OU=objects,DC=EAME,DC=SYNGENTA,DC=ORG"

## Logging
log_file = open("sync_log", "a")
def write_to_log(text, log_name, start_time = None):
    now = str(datetime.datetime.now())
    if start_time == None:
        log_string = now + ' ' + text + '\n'
    else:
        duration = datetime.datetime.now() - start_time
        log_string = now + ' ' + text + ' ' + str(duration) + '\n'
    log_name.write(log_string)

## Import filtered PC name and description from AD as dictionary
def import_from_ad(attr,where,dn):
    adquery_start_time = datetime.datetime.now()
    q = pyad.adquery.ADQuery()
    q.execute_query(attributes = attr,where_clause = where,base_dn = dn)
    write_to_log("AD query completed in",log_file,adquery_start_time)
    dict_of_pc_to_check = {}
    for r in q.get_results():
        name_upper = r['Name'].upper()
        if name_upper.startswith('PLWAL'):
            tuple_from_description = r['description']
            if tuple_from_description != None:
                dict_of_pc_to_check[name_upper] = tuple_from_description[0]
            else:
                dict_of_pc_to_check[name_upper] = None
    return dict_of_pc_to_check

## Import filtered data from assets file
def import_excel(excel_path):
    excel_import_start = datetime.datetime.now()
    df = pd.read_excel(excel_path)
    df_filtered = df[df[type_of_asset]=='laptop'].replace(np.nan, '', regex=True) ## replace nan with '', filter
    write_to_log("Excel import completed in",log_file,excel_import_start)
    return df_filtered

## Create description string according to excel file. string format like 
def description_string(el):
    pc_serial = el[serial_number].strip()
    manufacturer_model = el[manufacturer].strip() + ' ' + el[model].strip()
    p_n = str(el[part_number]).strip()
    name_to_normal = ud.unidecode(str(el[surname])).strip() + ' ' + ud.unidecode(str(el[name])).strip()
    comment_from_excel = el[comment]
    ##Formating purchase date
    if el[purchase_date] == '':
        formated_purchase_date = ''
    else:
        purchase_date_temp = el[purchase_date]
        if purchase_date_temp.month >= 10:
            purchase_month = str(purchase_date_temp.month)
        else:
            purchase_month = str("0")+str(purchase_date_temp.month)
        formated_purchase_date = str(purchase_date_temp.year)+purchase_month
    description_string_from_excel = ('{};{};{};{};{};;{}'.format(name_to_normal,manufacturer_model,pc_serial,p_n,formated_purchase_date,comment_from_excel))
    return description_string_from_excel

## Go through elements in data imported from excel, checks if it is in PC to check dict and update accordingly
def sync_ad(excel_list,ad_dict):
    synced_count = 0
    edited_count = 0
    for i in range(len(excel_list)):
        row = excel_list.iloc[i]
        pc_name_to_check = ('PLWAL'+ row[serial_number]).strip().upper()
        if pc_name_to_check in ad_dict:
            description_string_from_excel = description_string(row)
            if ad_dict[pc_name_to_check] != description_string_from_excel:
                time_update_begins = datetime.datetime.now()
                # AD description update
                ad_pc_to_update = adcomputer.ADComputer.from_cn(pc_name_to_check)
                ad_pc_to_update.update_attribute('description', description_string_from_excel)
                log_str = "changing "+ str(ad_dict[pc_name_to_check])+ " to " + str(description_string_from_excel)
                write_to_log(log_str,log_file,time_update_begins)
                edited_count += 1
            else:
                #log_str = str(datetime.datetime.now()) + " " + str(ad_dict[pc_name_to_check])+" Already synced!\n"
                #log_file.write(log_str)
                synced_count += 1
            del ad_dict[pc_name_to_check]
        else:
            continue
    ## Writing synced elements count
    sync_str = "Synced elements count " + str(synced_count)
    edit_str = "Edited elements count " + str(edited_count)
    write_to_log(sync_str,log_file)
    write_to_log(edit_str,log_file)

    ## Writing remaining items to log file
    for item in ad_dict:
        log_str = "not found in excel file " + str(item)
        write_to_log(log_str,log_file)

## Import and sync
write_to_log("-------------------Excel sync start--------------------------",log_file)
imported_excel_list = import_excel(excel_file_path)
imported_ad_dict = import_from_ad(attributes_ad,where_clause_ad,base_dn_ad)
sync_ad(imported_excel_list,imported_ad_dict)
log_file.close()