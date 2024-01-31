from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import six 
import csv
import re        
import numpy as np
import json
from time import sleep



# Carregando a página do Instagram
url = 'http://www.instagram.com'

# Solicita ao usuário que insira os links separados por vírgula
post_links_input = input('Adicione os links que gostaria de fazer scraping (separe os links por vírgula): ')
post_link = post_links_input.split(',')
# Carregar credenciais de login
with open('login.txt') as file:
    login = json.load(file)
    username = login.get("username", None)
    password = login.get("password", None)




# def login(username, password):
options = Options()
options.page_load_strategy = 'none'
driver = webdriver.Chrome(options=options)

# Login
driver.get(url)


WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="loginForm"]')))

email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]//input[@name="username"]')))
email_input.send_keys(username)

password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]//input[@name="password"]')))
password_input.send_keys(password)

submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
submit.click()

sleep(6)

# ========================================================================
# Scrapping nas paginas desejadas
nomes = []

# Itera sobre a lista de links
for i, link in enumerate(post_link):
    nome = f'scrapping_{i + 1}' 
    nomes.append(nome)



# entrada em cada postagem
for nome_postagem, link in zip(nomes, post_link):
    # Encontrar os links de postagens
    driver.get(link)
    sleep(15)
    
    # Scrollar os comentários da página, com a intenção de captar o máximo de informações
    element = driver.find_element(By.CSS_SELECTOR, '.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6')

    # Quantidade de scroll down
    num_scrolls = 150 

    # Loop para realizar o scroll diversas vezes
    for _ in range(1, num_scrolls):
        driver.execute_script("arguments[0].scrollBy(0, 2000);", element)
        sleep(3)

    print("Passou pela Scrollada")
    sleep(15)
# ===============================================================================

    users_instagram = []
    # Captura - Usuario
    users = driver.find_elements(By.CSS_SELECTOR, 'span._ap3a._aaco._aacw._aacx._aad7._aade[dir="auto"]')

    for i in range(2, len(users)):
        users_instagram.append(users[i].text)
        

    print('Passou pelos usuarios')
    sleep(15)
# ===============================================================================
    # Captura - Comentários

    # Comentários
    comments = driver.find_elements(By.CSS_SELECTOR, 'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj[dir="auto"][style="line-height: var(--base-line-clamp-line-height); --base-line-clamp-line-height: 18px;"]')
    
        #Separação de comentários do instagram  (Encontro de padrão)
    comments_instagram = []
    for i in range(1, len(comments)):
        if i % 2 == 0:
            comments_instagram.append(comments[i].text)
# ===============================================================================
    # Captura - Likes dos comentários

    print('Passou pelos comentarios')
    #curtida do comentário
    likes = driver.find_elements(By.CSS_SELECTOR,'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1xmf6yo.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1[style="height: 16px;"]')

    # Abordar apenas linhas com curtidas
    likes_instagram = []
    for i in range(1,len(likes)):
        if "curtidas" in likes[i].text: 
            likes_instagram.append(likes[i].text)
        else: 
            likes_instagram.append(None)
# ===============================================================================
    # Extração - Data do Comentário
    datetime =driver.find_elements(By.CSS_SELECTOR, 'time.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x1roi4f4.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6')

    datetime_instagram = []

    # Iterar sobre os elementos de tempo e extrair as datas
    for i in datetime:
        datetime_value = i.get_attribute('datetime')
        datetime_instagram.append(datetime_value)

# ===============================================================================

    # Arquivar tudo em um arquivo
    with open(f'{nome_postagem}.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(f"Usuários: {users_instagram}\n")
        arquivo.write(f"Comentários: {comments_instagram}\n")
        arquivo.write(f"Curtidas: {likes_instagram}\n")
        arquivo.write(f"Data: {datetime_instagram}\n")

    time.sleep(10)

# Encerrar o WebDriver
driver.quit()
