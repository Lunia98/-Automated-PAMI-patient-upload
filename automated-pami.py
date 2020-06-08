import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH) #For website
path = "C:\\Users\\Pablo\\Desktop\\Python Udemy\\datamayo.csv"
lines = [line for line in open(path)] #For archive
dataset = [line.strip().split(';') for line in open(path)]

calendarCode= [[0,0,0,0,1,2,3],[n for n in range(4,11)],[n for n in range(11,18)]
,[n for n in range(18,25)],[n for n in range(25,32)]]
#Created may calendar in list of lists

data= []
for line in dataset:
    day = int(line[0])
    name = str(line[1])
    dni = line[2]
    diagnostic = line[3]
    test = int(line[4])
    hour = int(line[5])
    afiliadoPropio = line[6]
    data.append([day,name,dni,diagnostic,test,hour,afiliadoPropio])
#Convert all the list with the first position in integer
#The new list now is 'data'
def calendar():
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
            
def clic_day(w,d): #I have to put +1 because html counts from 1 the positions
    day = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//tr[@id='{w}']/td[{d+1}]"))
    )
    time.sleep(1)
    day.click()    
    
    
def completeNameDoctor ():
    emptyDoctor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_368-real"))
        )
    emptyDoctor.click()
    nameDoctor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_370"))
        )
    time.sleep(0.5)
    nameDoctor.click()
    
    
def patienteClic(): #Abre el recuerdo donde se busca el paciente
    emptyPatiente = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_130-real"))
        )
    emptyPatiente.click()
    
def insertDni(Dni): 
    searchDni = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_140"))
    )
    searchDni.click()
    
    time.sleep(1)

    searchDni.send_keys(Dni)

def clicSearch(): #Una vez ingresado el DNI pongo buscar
    findPatiente = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "zk_comp_159"))
        )
    findPatiente.click()
    
def selectPatient(): #Selecciono el unico paciente que aparezca 
    patienteSelected = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zk_comp_164-cave"))
        )
    patienteSelected.click()
def diagnostic(diag):
    clicDiagnostic = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "zk_comp_208-real"))
    )
    clicDiagnostic.click()
    time.sleep(1)
    searchDiagnostic = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_221"))
    )
    searchDiagnostic.click()

    time.sleep(1)
    searchDiagnostic.send_keys(diag)
    time.sleep(0.5)
    searchDiagnostic.send_keys(Keys.RETURN)
    time.sleep(1)
    selectDiag = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//tbody[@id='zk_comp_229-rows']/tr[1]"))
    )
    time.sleep(0.5)
    selectDiag.click()
    addDiag = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_247"))
    )
    addDiag.click()
    time.sleep(0.5)
    
def test(codTest):
    clicTest = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_265-real"))
    )
    clicTest.click()
    time.sleep(0.5)
    searchTest = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_270"))
    )
    searchTest.click()
    time.sleep(1)
    searchTest.send_keys(codTest)
    searchTest.send_keys(Keys.RETURN)
    time.sleep(1)
    selectTest = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//tbody[@id='zk_comp_272-rows']/tr[1]"))
    )
    time.sleep(1)
    selectTest.click()
def hour(h):
    time.sleep(1)
    selectHour = driver.find_element_by_id("zk_comp_288-real")
    for i in range (0,4):
        selectHour.send_keys(Keys.BACKSPACE)
    selectHour.send_keys(0+h)
def cant():

    cant1 = driver.find_element_by_id("zk_comp_291")
    cant1.send_keys(1)
def patienteType():
    pType = driver.find_element_by_id("zk_comp_293-real")
    pType.send_keys('A')
def addTest():
    
    add1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"zk_comp_298"))
    )
    add1.click()
#-------------------------
#Entry to PAMI's website
driver.get("https://efectoresweb.pami.org.ar/EfectoresWeb/login.isp")
#Open session
search1 = driver.find_element_by_id("zk_comp_16")
search1.send_keys("UP0000000000")
try:
    search2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "zk_comp_20"))
    )
finally:

    search2.send_keys("xxxxxxxxxxxxx")
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
    alta = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "zk_comp_96"))
    ) 
    alta.click()
    time.sleep(1)
    # Here it goes for loops
    completeNameDoctor()
except:
    print('Hubo un error en columna 1!')
     

try:
    time.sleep(1)
    calendar()
except:
    print('Hubo un error en la columna 2!') 
try: 
    p=0
    w = check_week(p,data,calendarCode)
    d = check_day(p,data,calendarCode)
    clic_day(w,d)
    patienteClic()
    time.sleep(1)
    insertDni(data[p][2])
    clicSearch()
    time.sleep(1)
    selectPatient()
    time.sleep(1)
    diagnostic(data[p][3])
    time.sleep(1)
    test(data[p][4])
    time.sleep(1)
    hour(data[p][5])
    time.sleep(0.5)
    cant()
    patienteType()
    time.sleep(0.3)
    addTest()
    #Click in accepted 
    #Alta again 
    
except Exception: 
    traceback.print_exc()

# Falta:
#-Errores para chequear: 
    # Si no aparece nadie con el dni 
    # Dos personas mismo dni
    # Si hay numero de beneficiario en vez de dni 
    # Problema de la hora (hay que agregar el 0 porque el csv se guarda como 800)
#Si esta el error 1, apartar ese paciente en otra lista y seguir con el siguiente
#Corregir los try/except/finally

#Retocar time sleeps entre cosas     

