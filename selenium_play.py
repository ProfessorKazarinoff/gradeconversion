from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


def main():
    driver = webdriver.Chrome()
    driver.get("http://www.pcc.edu")
    #driver.wait(2) #does not work
    assert "Portland Community College" in driver.title
    link = driver.find_element_by_link_text('mypcc')
    link.click()
    username_field = driver.find_element_by_name("username")
    username_field.clear()
    username_field.send_keys("peter.kazarinsff")
    password_field = driver.find_element_by_name("password")
    password_field.clear()
    password_field.send_keys("peter.kazarinoff")
    #SignIn_button = driver.find_element_by_class_name('input.btn.btn-default')
    xpath = '// *[ @ id = "loginTable1"] / div[1] / div[3] / input'
    SignIn_button = driver.find_element_by_xpath(xpath)
    SignIn_button.click()
    #WebDriverWait(driver,2)
    #assert "No results found." not in driver.page_source
    #wait()
    driver.close()

if __name__ == '__main__':
    main()