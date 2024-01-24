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
   
                                  
    dados = []
    post_link = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]')

    #entrada em cada postagem
    for link in post_link:
        #Encontrar os links de postagens
        link.click()
        time.sleep(15)

        #Usuários
        users = driver.find_elements(By.CSS_SELECTOR,'span._ap3a._aaco._aacw._aacx._aad7._aade[dir="auto"]')
        
        users_instagram = []
        for i in users:
            users_instagram.append(i.text)
    
        # Comentários
        comments = driver.find_elements(By.CSS_SELECTOR, 'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.\
                                                        x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj[dir="auto"][style="line-height:\
                                                        var(--base-line-clamp-line-height); --base-line-clamp-line-height: 18px;"]')
        
            #Separação de comentários do instagram 
        comments_instagram = []
        for i in range(1, len(comments)):
            if i % 2 == 0:
                comments_instagram.append(comments[i].text)


        #curtida do comentário
        likes = driver.find_elements(By.CSS_SELECTOR,'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.\
                                                        x1fhwpqd.x1s688f.x1roi4f4.x1s3etm8.x676frb.x10wh9bi.x1wdrske.x8viiok.x18hxmgj[dir="auto"][style="line-height: var(--base-line-clamp-line-height);\
                                                        --base-line-clamp-line-height: 16px;"]')
        
            # Abordar apenas linhas com curtidas
        likes_instagram = []
        for i in range(len(likes)):
            if "curtidas" in likes[i].text: 
                likes_instagram.append(likes[i].text)

        
        
        # Arquivar tudo em uma lista
        dados.append([users_instagram,comments_instagram, likes_instagram])

        time.sleep(10)

        driver.quit()
                                                     


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








