from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import xlsxwriter
#Global Section
from selenium.webdriver.support.ui import WebDriverWait


# Lista - Captação de Dados do Instagram
dataframe_instagram = []

# Carregando a página do Instagram
url = 'http://www.instagram.com'
sleep(3.5)

# Carregar credenciais de login
with open('login.txt') as file:
    login = json.load(file)
    username = login.get("username", None)
    password = login.get("password", None)

def scrappe_comments(driver, name):
   
   
    driver.get(f'http://www.instagram.com/{name}/')
    time.sleep(10)
    
    driver.execute_script("window.scrollTo(0,4000);")

    time.sleep(7)

    driver.execute_script("window.scrollTo(0,4000);")

    time.sleep(7)
   
    # Encontro do link para entrar na publicação
    post_link = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/p/"]'))
    )

    #entrada em cada postagem
    for link in post_link:
        post_url =link.get_attribute('href')
        
        driver.get(post_url)

        time.sleep(5)
                                                     


def login(username, password):

    options = Options()
    options.page_load_strategy = 'none'
    driver = webdriver.Chrome(options=options)

    # Login
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="loginForm"]')))

        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]//input[@name="username"]')))
        email_input.send_keys(username)

        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]//input[@name="password"]')))
        password_input.send_keys(password)

        submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
        submit.click()

        sleep(6)

        scrappe_comments(driver, name)

        print(dataframe_instagram)
    except TimeoutException:
        print("Não foi possível logar com sua conta")







name = input('Qual usuário gostaria de pesquisar? :  ')
login(username, password)

sleep(20)








