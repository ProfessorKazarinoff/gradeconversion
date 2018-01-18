from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


def main():
    driver = webdriver.Chrome()   #makesure chromedriver.exe is in the cwd
    driver.get("https://online.pcc.edu")
    assert 'Login | PCC' in driver.title

    username_xpath = '//*[@id="username"]'
    username_field = driver.find_element_by_xpath(username_xpath)
    username_field.clear()
    username_field.send_keys("bik.kimmel")

    password_xpath = '//*[@id="password"]'
    password_field = driver.find_element_by_xpath(password_xpath)
    password_field.clear()
    password_field.send_keys("tymypass")

    login_xpath = '//*[@id="fm1"]/div/div[3]/input[4]'
    login_button = driver.find_element_by_xpath(login_xpath)
    login_button.click()

    driver.close()

if __name__ == '__main__':
    main()