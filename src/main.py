

import json
from logging import exception
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
import time 


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
    
    SearchButton=driver.find_element_by_id("btnSearchbutton2_1")
    SearchButton.click()

def writeToFile(id):
    d={id}
    with open('src\history.json', 'a') as f:
        json.dump(d, f)


def checkJobApplied(id):
    d={}
    with open('src\history.json') as f:
        d=json.load(f)
    if id in d:
        print("existing")
        return True
    else:
        print("New key")
        return False

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    except exception:
        return False
    return True



def ApplyToJob(element):
    #TODO: add check for number, if it exists in history.json then return None
    element.click()
    applyButton=driver.find_element_by_id("btnApply_top")
    applyButton.click()
    
    
    
    #this checks if job is already applied or not

    flag=flag= True
    try:
        test=driver.find_element_by_xpath("//h1[@class='TM_titlePage ']/span/span[contains(text(),'Application already')]")
        print(test.text)
    except NoSuchElementException:
        flag= False
    except exception:
        flag= False
    

    if flag==True:
        backButton=driver.find_element_by_xpath("//*[@id='Button-Box']/input[2]")
        backButton.click()
        #Should exit it here

    elif flag==False:
    
        privacyCheckbox=driver.find_element_by_id("chkReadAndAccept")
        privacyCheckbox.location_once_scrolled_into_view()
        privacyCheckbox.click()

        saveButton=driver.find_element_by_id("btnsave")
        saveButton.click()

        applyForJobHeader=driver.find_element_by_xpath("//*[@title='Apply for a Job'']")
        waitForAnElement(applyForJobHeader)

        submitButton=driver.find_element_by_id("btnSubmit")
        submitButton.location_once_scrolled_into_view()
        submitButton.click()

        backButton=driver.find_element_by_xpath("//*[@id='Button-Box']/input[2]")
        backButton.click()

    print("clicked back ")
    
    waitForAnElement("//*[@id='job-search-toggle']")

    print("passed apply jobs")

        











def OpenJobs():

    AffliationChoices(["Work Study - LEAP","Work Study"])

    evenJobNumberXpath="//*[@class='tblStripingEven']/td/a[@class='relink']"
    # evenJobNameXpath="//*[@class='tblStripingEven']//a[@class='relink']/ancestor::td/following-sibling::td/div/a"

    # evenJobsNameList= driver.find_elements_by_xpath(evenJobNameXpath)
    evenJobsNumList=driver.find_elements_by_xpath(evenJobNumberXpath)

   


    oddJobNumberXpath="//*[@class='tblStripingOdd']/td/a[@class='relink']" 
    # oddJobNameXpath="//*[@class='tblStripingOdd']/td/a[@class='relink']/ancestor::td/following-sibling::td/div/a"

    oddJobsNumList=driver.find_elements_by_xpath(oddJobNumberXpath)
    
    #Individual webelements:
    for odd, even in zip(oddJobsNumList, evenJobsNumList):
        
        print(odd,"<--")
        ApplyToJob(odd)

        # ApplyToJob(even)



    
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






