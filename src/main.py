

from asyncore import write
from genericpath import getsize
import json
from logging import exception
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
import time 
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Chrome(executable_path=r"src\\chromedriver.exe")

def Login():
    driver.get('https://jobs-ca.technomedia.com/yorkuniversity/?')

    f=open("src\\account.txt","r")
    lines=f.readlines()
    username=lines[0]
    password=lines[1]
    f.close()

    # print("Username: "+username +"\n Password: "+password+"\n")
    try:
        Cookies_button=driver.find_element_by_xpath("//button[contains(text(),'Accept all cookies')]")
        Cookies_button.is_displayed()
        Cookies_button.click()
    except:
        print("Cookies popup not found")


    Username_Input=driver.find_element_by_id("TM_LOGINFRAME_USERNAME_FLD")
    Username_Input.send_keys(username)

    Password_Input=driver.find_element_by_id("TM_LOGINFRAME_PASSWORD_FLD")
    Password_Input.send_keys(password)

    Continue_Button=driver.find_element_by_id("TM_LOGINFRAME_CONTINUE_BTN")
    Continue_Button.click()

    ViewJobPosting_button=driver.find_element_by_xpath("//*[@id='liNEWS_INTERNAL_JOBS']/a")
    ViewJobPosting_button.click()

#waits for it to come online
def waitForAnElement(elem):
    from selenium.webdriver.support.wait import WebDriverWait
    element = WebDriverWait(driver, 10).until(lambda x: elem)

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    except exception:
        return False
    return True


# Prereq: Needs to be on Job Postings page after logging in. 
def AffliationChoices(option):
    Affliation_Dropdown=driver.find_element_by_xpath("//*[@data-id='selContractTypes_1']/span[contains(text(),'Affiliation')]")
    Affliation_Dropdown.click()


    for affChoice in list(option):
        # print(affChoice)
        choice="//*[@id='frmimproveSearch2_1']/div//a/span[normalize-space(text())='"+str(affChoice)+"']"
        # print(choice)
        affliationOption= driver.find_element_by_xpath(choice)
        affliationOption.click()
    
    Affliation_Dropdown.click()
    
    flag=False
    #Getting unusual error in which dropdown is still open, fix attempt for that.
    try:
        flag=check_exists_by_xpath("//*[@class='btn-group bootstrap-select show-tick re-select doNotAutoSelectFirstOption open']")
    except NoSuchElementException:
        flag=False
    
    if flag==True:
        dropdown_class=driver.find_element_by_xpath("//*[@class='btn-group bootstrap-select show-tick re-select doNotAutoSelectFirstOption open']")
        dropdown_class.click()
    SearchButton=driver.find_element_by_id("btnSearchbutton2_1")


    SearchButton.click()

def writeToFile(id):
    
    with open('src\history.txt', 'a') as f:
        f.write(id+"\n")

def writeToManualApplicationFile(id):
    
    with open('src\manualApplyList.txt', 'a') as f:
        f.write(id+"\n")


def checkJobApplied(id):
    check = str(id)
    with open('src\history.txt') as f:
        match = check in f.read().splitlines()
    print("match is: ",match)
    return match




def ApplyToJob(element: WebElement):
   
    
    element.click()
    applyButton=driver.find_element_by_id("btnApply_top")
    applyButton.click()
    
    
   

    flag= True
    try:
        test=driver.find_element_by_xpath("//h1[@class='TM_titlePage ']/span/span[contains(text(),'Application already')]")
        
    except NoSuchElementException:
        flag= False
    except exception:
        flag= False
    

    if flag==True:
        print("Job already applied for ")
        backButton=driver.find_element_by_xpath("//*[@id='Button-Box']/input[2]")
        backButton.click()
        AffliationChoices(["Work Study - LEAP","Work Study","YUSA 2 PT"])
        #Should exit it here

    elif flag==False:
        print("New job found, applying.")
        privacyCheckbox=driver.find_element_by_id("chkReadAndAccept")
        # privacyCheckbox.location_once_scrolled_into_view()
        privacyCheckbox.click()

        saveButton=driver.find_element_by_id("btnsave")
        saveButton.click()

        time.sleep(15)
        applyForJobHeader=driver.find_element_by_xpath("//*[@title='Apply for a Job']")
        waitForAnElement(applyForJobHeader)

        submitButton=driver.find_element_by_id("btnSubmit")
        # submitButton.location_once_scrolled_into_view()
        submitButton.click()

        backButton=driver.find_element_by_xpath("//*[@id='Button-Box']/input[2]")
        backButton.click()

    
    
    # waitForAnElement("//*[@id='job-search-toggle']")

    AffliationChoices(["Work Study - LEAP","Work Study","YUSA 2 PT"])
    print("passed apply jobs")


        











def OpenJobs():

    

    jobsNumberXpath="//*[contains(@class,'tblStripingEven') or contains(@class,'tblStripingOdd')]/td/a[@class='relink']"

    jobsNumberListSize= len(driver.find_elements_by_xpath(jobsNumberXpath))
    
    
    # for i in range(1,jobsNumberListSize):
    for i in range(45,200):
        
        
        
        AffliationChoices(["Work Study - LEAP","Work Study","YUSA 2 PT"])
        if i>=45:
            for j in range(1,i%20):
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(1)
        elemXpath="(//*[contains(@class,'tblStripingEven') or contains(@class,'tblStripingOdd')]/td/a[@class='relink'])["+str(i)+"]"
        currentElem=driver.find_element_by_xpath(elemXpath)
        currentText=currentElem.text
        print("Current text is:"+currentText)
        if checkJobApplied(currentText)==True:
            print("Current jop has already been applied to, skipping.")
            ViewJobPosting_button=driver.find_element_by_xpath("//*[@id='liNEWS_INTERNAL_JOBS']/a")
            ViewJobPosting_button.click()
        else:
            try:
                print(currentText+" is the current job number")
                ApplyToJob(currentElem)
                writeToFile(currentText)
            except NoSuchElementException:
                print("Job number which requires manual filling of forms: "+currentText)
                writeToManualApplicationFile(currentText)
                ViewJobPosting_button=driver.find_element_by_xpath("//*[@id='liNEWS_INTERNAL_JOBS']/a")
                ViewJobPosting_button.click()
    
   
        


    

        



    
def main():

    Login()
    
    OpenJobs()


    

    



if __name__ == "__main__":
    main()

# User_Input=driver.find_element_by_id("mli")
# User_Input.send_keys(username)

# # driver.find_element_by_id("password").click()



# # driver.find_element_by_id("password").send_keys("Test")

# driver.switch_to.alert.dismiss()

# # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "password"))).click()
# Pwd_Input=driver.find_element_by_id(password)
# Pwd_Input.send_keys("passwor1d")

# Login_Button=driver.find_element_by_xpath("//*[@type='submit']")
# Login_Button.click()






