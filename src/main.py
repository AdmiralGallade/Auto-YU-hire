

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



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


def OpenJobs():
    evenJobNumberXpath="//*[@class='tblStripingEven']/td/a[@class='relink']"

    evenJobNameXpath="//*[@class='tblStripingEven']//a[@class='relink']/ancestor::td/following-sibling::td/div/a"


    oddJobNumberXpath="//*[@class='tblStripingOdd']/td/a[@class='relink']" 
    oddJobNameXpath="//*[@class='tblStripingOdd']/td/a[@class='relink']/ancestor::td/following-sibling::td/div/a"

    
def main():
    Login()
    AffliationChoices(["YUSA 2 PT","Work Study - LEAP","Work Study"])

    



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






