import lxml.html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = Options()
options.headless = False
options.add_argument("--window-size=800,600")
datais = {}

driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver')
#driver = webdriver.Remote('http://127.0.0.1:4444/', options.to_capabilities())
driver.get("https://charts.bogged.finance/?token=0xc1999565b29e5fa35a24ecc16a4dcf632fb22d1e")
current_price = ""
delay = 20 # seconds
def getPrice():
    
    try:
        driver.refresh()
        myElem = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH, './/body/div[1]/div[3]/main/div/div/div/div/div[5]/div/div/div/div/div[1]/p[2]/span')))
         #myElem = WebDriverWait(driver,delay).until(ExpectedConditions.elementToBeClickable(By.xpath(".//body/div[2]/div[1]/div[2]/div[1]/div[2]/table/tr[1]/td[2]/div/div[1]/div[1]/div/div[1]/div[2]/div/div[2]")))
        myElem = driver.find_element_by_xpath(".//body/div[1]/div[3]/main/div/div/div/div/div[2]/div[1]/div[1]/span[2]/h4") #print ("Page is ready!")
         #myElem2 = WebDriverWait(driver,delay).until(EC.visibility_of_all_elements_located((By.XPATH, './/body/div[1]/div[2]/main/div/div/div/div/div[4]/div/div/div/div/div[1]/p[2]/span')))
         #myElem = WebDriverWait(driver,delay).until(ExpectedConditions.elementToBeClickable(By.xpath(".//body/div[2]/div[1]/div[2]/div[1]/div[2]/table/tr[1]/td[2]/div/div[1]/div[1]/div/div[1]/div[2]/div/div[2]")))
        myElem2 = driver.find_element_by_xpath(".//body/div[1]/div[3]/main/div/div/div/div/div[2]/div[1]/div[2]/span[3]/h4") #print ("Page is ready!")
        myElem3 = driver.find_element_by_xpath("//body/div[1]/div[3]/main/div/div/div/div/div[2]/div[1]/div[1]/span[3]/h4") #print ("Page is ready!")
        datais = {'price': myElem.text, 'cap' : myElem2.text, 'hc24' : str(myElem3.text) }
        return datais

    except:
        #print ("Loading took too much time!")
        pass


def getCap():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=800,600")

    driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')
    driver.get("https://charts.bogged.finance/?token=0xc1999565b29e5fa35a24ecc16a4dcf632fb22d1e")
    current_price = ""
    delay = 20 # seconds
    try:
        myElem = WebDriverWait(driver,delay).until(EC.visibility_of_all_elements_located((By.XPATH, './/body/div[1]/div[2]/main/div/div/div/div/div[4]/div/div/div/div/div[1]/p[2]/span')))
         #myElem = WebDriverWait(driver,delay).until(ExpectedConditions.elementToBeClickable(By.xpath(".//body/div[2]/div[1]/div[2]/div[1]/div[2]/table/tr[1]/td[2]/div/div[1]/div[1]/div/div[1]/div[2]/div/div[2]")))
        myElem = driver.find_element_by_xpath(".//body/div[1]/div[2]/main/div/div/div/div/div[1]/div[1]/div[2]/span[3]/h4") #print ("Page is ready!")
        return myElem.text

    except:
        #print ("Loading took too much time!")
        pass





#print (getPrice())
#print (getCap())