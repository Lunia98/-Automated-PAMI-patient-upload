import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
import calendar
from datetime import date 

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
driver = webdriver.Chrome(PATH) 
path = "C:\\Users\\milag\\Desktop\\dataagosto.csv"
lines = [line for line in open(path)]   
dataset = [line.strip().split(';') for line in open(path)]

xpath_diag_empty= "//tbody[@id='zk_comp_244-rows']/tr[1]/td[2]"
xpath_test_empty= "//tbody[@id='zk_comp_287-rows']/tr[1]/td[2]"
# Created may calendar in list of lists
today= date.today()
last_month= today.month -1
current_year = today.year
calendarCode= calendar.monthcalendar(current_year,last_month)

errorList = []
# Convert all the list with the correct types 
# The new list of patients now is 'data'
data= []
for line in dataset:
    day = int(line[0])
    name = str(line[1])
    dni = line[2]
    diag = line[3]
    test0 = int(line[4])
    hour0 = str(line[5])
    afiliadoPropio = line[6]
    data.append([day,name,dni,diag,test0,hour0,afiliadoPropio])
# For upload a patient
def alta():
    alta = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "zk_comp_96"))
    ) 
    alta.click()  
# This function opens the calendar and goes to the last month (we always want to that)
def click_calendar():
    calendario = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_128-real"))
        )
    calendario.click()
        
    left = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "_z_6-left"))
    )
    left.click()

def check_week(p,data,calendarCode):
    if data[p][0] in calendarCode[0]:
        week = '_z_6-w0'
        return week     
    elif data[p][0] in calendarCode[1]:
        week = '_z_6-w1'
        return week   
    elif data[p][0] in calendarCode[2]:
        week = '_z_6-w2'
        return week   
    elif data[p][0] in calendarCode[3]:
        week = '_z_6-w3'
        return week   
    elif data[p][0] in calendarCode[4]:
        week = '_z_6-w4'
        return week   

def check_day(p,data,calendarCode):
    if data[p][0] in calendarCode[0]:
        d = calendarCode[0].index(data[p][0])
        return d
    elif data[p][0] in calendarCode[1]:
        d = calendarCode[1].index(data[p][0])
        return d
    elif data[p][0] in calendarCode[2]:
        d = calendarCode[2].index(data[p][0])
        return d
    elif data[p][0] in calendarCode[3]:
        d = calendarCode[3].index(data[p][0])
        return d
    elif data[p][0] in calendarCode[4]:
        d = calendarCode[4].index(data[p][0])
        return d
    
# +1 because html counts from 1 the positions            
def clic_day(w,d): 
    day = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//tr[@id='{w}']/td[{d+1}]"))
    )
    time.sleep(1)
    day.click()    
    
# Select the doctor who did the studies    
def complete_name_doctor ():
    emptyDoctor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_383-real"))
        )
    emptyDoctor.click()
    nameDoctor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_385"))
        )
    time.sleep(0.5)
    nameDoctor.click()
    
# Open the box where the patient is searched    
def patient_clic(): 
    emptyPatiente = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_130-real"))
        )
    emptyPatiente.click()

def n_beneficiario(num):
    searchBene = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_153"))
    )
    searchBene.click()
    time.sleep(1)
    for i in range (0,18):
        searchBene.send_keys(Keys.BACKSPACE)
    time.sleep(1)

    searchBene.send_keys(num)
    
def insert_dni(Dni): 
    searchBene = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "zk_comp_153"))
    )
    searchBene.click()
    searchBene.clear()
    time.sleep(0.3)
    for i in range (0,18):
        searchBene.send_keys(Keys.BACKSPACE)
    time.sleep(0.5)

    searchDni = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_140"))
    )
    searchDni.click()
    time.sleep(0.5)
    for i in range (0,10):
        searchDni.send_keys(Keys.BACKSPACE)
    time.sleep(1)
    searchDni.send_keys(Dni)
# The patient is sought after having entered ID or benefit number
def clic_search(): 
    findPatiente = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "zk_comp_159"))
        )
    findPatiente.click()

# Select the only patient that appears    
def select_patient(): 
    patienteSelected = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_164-rows"))
        )
    patienteSelected.click()

def check_if_exist_second_patient(datapatient):
    try: 
        second_result = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='zk_comp_164-rows']/tr[2]")))
    except: 
        second_result = False	
    if second_result:
        lastname= datapatient.split()
        first_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='zk_comp_164-rows']/tr[1]")))
        first_text_content = first_result.get_attribute("textContent").split()
        second_text_content = second_result.get_attribute("textContent").split()
        if lastname[0].lower() == first_text_content[0].lower():
            first_result.click()
        elif lastname[0].lower() == second_text_content[0].lower():
            second_result.click()
        else: 
            cancel()
    else:
        time.sleep(0.3)
        select_patient()

def click_diagnostic():
    clicDiagnostic = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "zk_comp_223-real"))
    )
    clicDiagnostic.click()
    time.sleep(1)

def search_diag(diag):
    searchDiagnostic = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_236"))
    )
    searchDiagnostic.click()

    time.sleep(1)
    searchDiagnostic.send_keys(diag)
    time.sleep(0.5)
    searchDiagnostic.send_keys(Keys.RETURN)
    time.sleep(1)

def select_and_add_diag():
    selectDiag = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//tbody[@id='zk_comp_244-rows']/tr[1]"))
    )
    time.sleep(0.5)
    selectDiag.click()
    addDiag = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_262"))
    )
    addDiag.click()
    time.sleep(0.5)

def same_as_above(datacurrent, dataprev):
    return datacurrent == dataprev

def is_not_empty(xpath):
    try: 
        selectDiag = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    except:
        selectDiag = False
    if selectDiag != False:
        return True
    else:
        return False
def click_test():
    clicTest = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_280-real"))
    )
    clicTest.click()
    time.sleep(0.5)
def search_test(codTest):
    searchTest = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_285"))
    )
    searchTest.click()
    time.sleep(1)
    searchTest.send_keys(codTest)
    searchTest.send_keys(Keys.RETURN)
    time.sleep(1)
def select_test():
    selectTest = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//tbody[@id='zk_comp_287-rows']/tr[1]"))
    )
    time.sleep(1)
    selectTest.click()
def hour(h):
    time.sleep(1)
    selectHour = driver.find_element_by_id("zk_comp_303-real")
    for i in range (0,4):
        selectHour.send_keys(Keys.BACKSPACE)
    selectHour.send_keys(h)
def cant():

    cant1 = driver.find_element_by_id("zk_comp_306")
    cant1.send_keys(1)
def patient_type():
    pType = driver.find_element_by_id("zk_comp_308-real")
    pType.send_keys('A')
def add_test():
    
    add1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_313"))
    )
    add1.click()
def accepted():
    aceptar = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, "zk_comp_317"))
    )
    aceptar.click()
def cancel():
    cancel = driver.find_element_by_id("zk_comp_318")
    cancel.click()
    time.sleep(2)
    alta()
    errorList.append(data[p])
#-------------------------
#Entry to PAMI's website
driver.get("https://efectoresweb.pami.org.ar/EfectoresWeb/login.isp")
#Open session
search1 = driver.find_element_by_id("zk_comp_16")
search1.send_keys("UP000000000000")
search2 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "zk_comp_20"))
)

search2.send_keys("xxxxxxxxxxxxxx")
search2.send_keys(Keys.RETURN)
    #Enter the section where I actually upload the data
try:
    prestaciones = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "zk_comp_12-a"))
    )
    prestaciones.click()
    prestacionAmbulatoria = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "zk_comp_14-a"))
    )
    prestacionAmbulatoria.click()
    alta()
    time.sleep(1)

except Exception:
    traceback.print_exc()
     

for p in range(0,len(data)):
    try:   
        time.sleep(1)
        complete_name_doctor()
        time.sleep(1)
        click_calendar()
        w = check_week(p,data,calendarCode)
        d = check_day(p,data,calendarCode)
        time.sleep(1)
        clic_day(w,d)
        patient_clic()
        time.sleep(0.5)
    
        if (len(data[p][2]) > 9):
            searchDni = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_140")))
            searchDni.click()
            time.sleep(0.5)
            for i in range (0,10):
                searchDni.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
            n_beneficiario(data[p][2])
            
        else: 
            insert_dni(data[p][2])
        time.sleep(0.5)
        clic_search()
        
        check_if_exist_second_patient(data[p][1])
        
        time.sleep(0.3)
        
        click_diagnostic()

        if same_as_above(data[p][3], data[p-1][3]) and is_not_empty(xpath_diag_empty):
            select_and_add_diag()
        else:
            search_diag(data[p][3])
            select_and_add_diag()
        
        time.sleep(0.5)
        click_test()

        if same_as_above(data[p][4], data[p-1][4]) and is_not_empty(xpath_test_empty):
            select_test()
        else:
            search_test(data[p][4])
            select_test()
        
        time.sleep(0.5)
        
        hour(data[p][5])
        
        time.sleep(0.5)
        
        cant()
        patient_type()
        
        time.sleep(0.3)
        
        add_test()
        time.sleep(1)
        accepted()
        
        time.sleep(2)
        
        alta()
    except:
        cancel()
    #Click in accepted 
    #Alta again 
if len(errorList) > 0:    
    print("Hey these patients couldn't be processed")
    print(errorList)

# Falta:

#Retocar time sleeps entre cosas     
#Agregar comentarios 
