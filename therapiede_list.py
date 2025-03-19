from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import sys
import os
from datetime import datetime
from selenium.common import exceptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.print_page_options import PrintOptions
import base64
import math

currentScriptDirectoryPath = os.path.dirname(os.path.abspath(__file__))
currentScriptDirectoryPathFiles = os.listdir(currentScriptDirectoryPath)

sys.path.append(currentScriptDirectoryPath)

from therapiede_list_lib import save_data
from therapiede_list_lib import is_data
from therapiede_list_lib import load_data
from therapiede_list_lib import get_all_lat_lon
from therapiede_list_lib import get_all_lat_lon_mod
from therapiede_list_lib import write_the_file
from therapiede_list_lib import write_quermed_online_email_files
from therapiede_list_lib import write_all_trans_online_theras
from therapiede_list_lib import write_trans_db_files

def calcDistanceBetweenPoints(driver, lat1, lon1, lat2, lon2):
    distance = driver.execute_script("return window.coordinateDistance(arguments[0], arguments[1], arguments[2], arguments[3])", lat1, lon1, lat2, lon2)
    return round(distance, 3)

def write_the_file(name="0", content=[]):
    target = os.path.join("thera_lists", name+"_theras_online.txt")
    with open(target, 'w') as f:
         for line in content:
             f.write(f"{line}\n")
             
def search_word_in_page(word, driver):
    return word in driver.page_source

def search_array_in_page(words, driver, must_found=1):
    founded = 0
    for word in words:
        if search_word_in_page(word, driver):
           founded = founded + 1
    return founded >= must_found

search_words_queer = ["Transition", "Transitionsbegleitung", "transident", "lesbisch", "schwul", "bisexuell", "pansexuell", "intersexuell", "polyamor", "queer", "nonbinär", "trans*", "Trans*", "VLSP", "LGBTQ", "LGBTQ+", "LGBTQIA", "Geschlechtsdysphorie", "inter*", "Transidentität", "vlsp.de", "Verband für lesbische", "nonbinary", "gay", "lesbian", "bisexual", "pansexual", "transidenter"]  
search_words_queer_must_found = 1
no_trans_thera_email = []
trans_thera_email = []
no_trans_thera_email_all = []
trans_thera_email_all = []
def search_queer_words_on_thera_profil(url, driver):
    main_window = driver.current_window_handle
    main_window_one = driver.window_handles[0]
    driver.execute_script("window.open()")
    time.sleep(1)
    new_tab = driver.window_handles[1]
    driver.switch_to.window(new_tab)
    time.sleep(1)
    driver.get(url)
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#microsite .shadowbox.therapist-details')))
    except Exception as e:
        print(e)
        print("exception")
        driver.close()
        driver.switch_to.window(main_window_one)
        return False
    is_founded_queer = search_array_in_page(search_words_queer, driver, search_words_queer_must_found)
    if search_word_in_page("Psychologische/r Psychotherapeut/in", driver) or search_word_in_page("Diplom-Psychologie", driver) or search_word_in_page("Master in Psychologie", driver):
       if is_founded_queer:
          trans_profil_psychologe[url] = True
       else:
          no_trans_profil_psychologe[url] = True
    try:
        contact_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#contact-button')))
    except Exception as e: 
        print(e)
        print("exception")
        driver.close()
        driver.switch_to.window(main_window_one)
        return is_founded_queer

    with open('./jquery.js', 'r') as jquery_js: 
        # 3) Read the jquery from a file
        jquery = jquery_js.read() 
        # 4) Load jquery lib
        driver.execute_script(jquery)
        
    with open('./contact_button.js', 'r') as cb_js: 
        # 3) Read the jquery from a file
        cb = cb_js.read() 
        # 4) Load jquery lib
        driver.execute_script(cb)

    email_address_value = driver.execute_script("return window.getDecryptedEmail();");
    len_email_address_value = len(email_address_value)
    time.sleep(1)
    driver.close()
    driver.switch_to.window(main_window_one)
    if is_founded_queer:
       print("founded")
       if len_email_address_value > 0:
          trans_thera_email.append(email_address_value)
          trans_thera_email_all.append(email_address_value)
          print("trans_email: " + email_address_value)
    else:
       if len_email_address_value > 0:
          no_trans_thera_email.append(email_address_value)
          no_trans_thera_email_all.append(email_address_value)
          print("no_trans_email: " + email_address_value)
    return is_founded_queer

no_trans_profil = {}
trans_profil = {}
trans_profil_psychologe = {}
trans_profil_gruppe = {}
trans_profil_both = {}
no_trans_profil_psychologe = {}
no_trans_profil_gruppe = {}
no_trans_profil_both = {}
trans_and_sexual_thera = {}
trans_and_sexual_thera_gruppe = {}
trans_and_sexual_thera_psychologe = {}
trans_and_sexual_thera_both = {}
no_trans_and_sexual_thera = {}
no_trans_and_sexual_thera_gruppe = {}
no_trans_and_sexual_thera_psychologe = {}
no_trans_and_sexual_thera_both = {}
psychologe_check = {}
email_check = {}
ret_write_trans_db_files = write_trans_db_files()
trans_profil = ret_write_trans_db_files["trans_profil"]
no_trans_profil = ret_write_trans_db_files["no_trans_profil"]
trans_profil_gruppe = ret_write_trans_db_files["trans_profil_gruppe"]
trans_profil_psychologe = ret_write_trans_db_files["trans_profil_psychologe"]
trans_profil_both = ret_write_trans_db_files["trans_profil_both"]
no_trans_profil_gruppe = ret_write_trans_db_files["no_trans_profil_gruppe"]
no_trans_profil_psychologe = ret_write_trans_db_files["no_trans_profil_psychologe"]
no_trans_profil_both = ret_write_trans_db_files["no_trans_profil_both"]
trans_and_sexual_thera = ret_write_trans_db_files["trans_and_sexual_thera"]
trans_and_sexual_thera_gruppe = ret_write_trans_db_files["trans_and_sexual_thera_gruppe"]
trans_and_sexual_thera_psychologe = ret_write_trans_db_files["trans_and_sexual_thera_psychologe"]
trans_and_sexual_thera_both = ret_write_trans_db_files["trans_and_sexual_thera_both"]
no_trans_and_sexual_thera = ret_write_trans_db_files["no_trans_and_sexual_thera"]
no_trans_and_sexual_thera_gruppe = ret_write_trans_db_files["no_trans_and_sexual_thera_gruppe"]
no_trans_and_sexual_thera_psychologe = ret_write_trans_db_files["no_trans_and_sexual_thera_psychologe"]
no_trans_and_sexual_thera_both = ret_write_trans_db_files["no_trans_and_sexual_thera_both"]
thera_data = {}
if is_data("psychologe_check"):
   psychologe_check = load_data("psychologe_check")
if is_data("thera_data"):
   thera_data = load_data("thera_data")
def create_thera_data_attr(url, name, value):
    if not url in thera_data:
       thera_data[url] = {}
    if not name in thera_data[url]:
       thera_data[url][name] = value
    save_data(thera_data, "thera_data")

def create_thera_data_attrs(url, value, names):
    for i in range(0, len(names)):
        create_thera_data_attr(url, names[i], value)
def set_thera_data_value(url, name, value):
    create_thera_data_attr(url, name, "")
    thera_data[url][name] = value
    save_data(thera_data, "thera_data")
def get_thera_data_value(url, name, default_value=""):
    if url in thera_data and name in thera_data[url]:
       return thera_data[url][name]
    else:
       create_thera_data_attr(url, name, default_value)
       return default_value
    
def init_thera(url):
    create_thera_data_attrs(url, "", ["jobtitle", "name", "email", "wartezeit", "description"])
    create_thera_data_attrs(url, False, [
                                            "trans", "psychologe", "sexualitaet", "gruppe", "gruppe_and_psychologe", 
                                            "trans_and_psychologe", "trans_and_gruppe_and_psychologe", 
                                            "psychologe_check", "queer_check", "email_check", 
                                            "has_email",
                                            "offline"
                                        ])
    save_data(thera_data, "thera_data")

def change_thera(url):
    if True:
        if url == "https://www.therapie.de/profil/blaszcyk/":
           thera_data[url]["psychologe"] = True
        
        if url == "https://www.therapie.de/profil/brauer/":
           thera_data[url]["gruppe"] = True
        
        if not thera_data[url]["psychologe"]:
           jobtitle = thera_data[url]["jobtitle"].strip()
           name = thera_data[url]["name"].strip()
           desc = thera_data[url]["description"].strip()
           is_psych_string = "Psych."
           is_psych_string_2 = "Dipl.-Psycholog"
           if is_psych_string in name or is_psych_string in jobtitle or "Psycholog" in jobtitle or is_psych_string_2 in desc:
              thera_data[url]["psychologe"] = True
              #thera_data[url]["heilpraktiker"] = False
        
        if thera_data[url]["gruppe"] and thera_data[url]["psychologe"]:
           thera_data[url]["gruppe_and_psychologe"] = True
    
        if thera_data[url]["trans"] and thera_data[url]["gruppe"] and thera_data[url]["psychologe"]:
           thera_data[url]["trans_and_gruppe_and_psychologe"] = True
           
    save_data(thera_data, "thera_data")

def search_queer_words_on_thera_profil_ex(url, driver):
    init_thera(url)
    if url in psychologe_check:
       psycho_type = type(psychologe_check[url])
       if psycho_type == type(True):
          psychologe_check[url] = ""
          save_data(psychologe_check, "psychologe_check")

       if len(psychologe_check[url]) > 0:
          set_thera_data_value(url, "psychologe_check", True)
          istrans = is_trans(url)
          istranstype = type(istrans) == type(True)
          set_thera_data_value(url, "trans", istranstype and istrans)
          if istranstype:
             return istrans          
          
    driver.get(url)
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#generellinfos')))
    except Exception as e:
        pass
    time.sleep(1)
    try:
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#microsite .shadowbox.therapist-details')))
    except Exception as e:
        print(e)
        print("exception")
        is_that_psychologe = search_word_in_page("Psychologische/r Psychotherapeut/in", driver) or search_word_in_page("Diplom-Psychologie", driver) or search_word_in_page("<li>Berufsverband Deutscher Psychologinnen und Psychologen</li>", driver)
        is_that_sexual = search_word_in_page("<li>Sexualität</li>", driver)
        is_that_gruppe = search_word_in_page("<li>Gruppentherapie</li>", driver)
        is_that_hpg = search_word_in_page("<li>Erlaubnis zur Psychotherapie nach Heilpraktikergesetz</li>", driver)
        is_that_both = is_that_gruppe and is_that_psychologe
        set_thera_data_value(url, "psychologe", is_that_psychologe)
        set_thera_data_value(url, "heilpraktiker", is_that_hpg)
        set_thera_data_value(url, "sexualitaet", is_that_sexual)
        set_thera_data_value(url, "gruppe", is_that_gruppe)
        set_thera_data_value(url, "gruppe_and_psychologe", is_that_both)
        set_thera_data_value(url, "psychologe_check", True)
        set_thera_data_value(url, "trans", False)
        set_thera_data_value(url, "queer_check", False)
        set_thera_data_value(url, "email_check", False)
        set_thera_data_value(url, "has_email", False)
        prefix = ""
        if is_that_gruppe:
           print("Gruppen Therapeut")
        if is_that_sexual:
           print("Sex Therapeut")
        if is_that_psychologe:
           print("Psycho Therapeut >.< -> Der dein Verstand der Norm angleicht!!!!")
        if is_that_both:
           print("Beides!!!!")
        if is_that_sexual:
            no_trans_profil[url] = ""
            save_data(no_trans_profil, "no_trans_profil")
            if is_that_psychologe:
               no_trans_profil_psychologe[url] = ""
               save_data(no_trans_profil_psychologe, "no_trans_profil_psychologe")
            if is_that_gruppe:
               no_trans_profil_gruppe[url] = ""
               save_data(no_trans_profil_gruppe, "no_trans_profil_gruppe")
            if is_that_both:
               no_trans_profil_both[url] = ""
               save_data(no_trans_profil_both, "no_trans_profil_both")
        else:
            no_trans_and_sexual_thera[url] = ""
            save_data(no_trans_and_sexual_thera, "no_trans_and_sexual_thera")
            if is_that_psychologe:
               no_trans_and_sexual_thera_psychologe[url] = ""
               save_data(no_trans_and_sexual_thera_psychologe, "no_trans_and_sexual_thera_psychologe")
            if is_that_gruppe:
               no_trans_and_sexual_thera_gruppe[url] = ""
               save_data(no_trans_and_sexual_thera_gruppe, "no_trans_and_sexual_thera_gruppe")
            if is_that_both:
               no_trans_and_sexual_thera_both[url] = ""
               save_data(no_trans_and_sexual_thera_both, "no_trans_and_sexual_thera_both")
               
        psychologe_check[url] = ""
        save_data(psychologe_check, "psychologe_check")
        return False
    is_founded_queer = search_array_in_page(search_words_queer, driver, search_words_queer_must_found)
    has_trans_profil_email = url in email_check and url in trans_profil
    has_no_trans_profil_email = url in email_check and url in no_trans_thera_email
    is_that_psychologe = search_word_in_page("Psychologische/r Psychotherapeut/in", driver) or search_word_in_page("Diplom-Psychologie", driver) or search_word_in_page("<li>Berufsverband Deutscher Psychologinnen und Psychologen</li>", driver)
    is_that_sexual = search_word_in_page("<li>Sexualität</li>", driver)
    is_that_gruppe = search_word_in_page("<li>Gruppentherapie</li>", driver)
    is_that_hpg = search_word_in_page("<li>Erlaubnis zur Psychotherapie nach Heilpraktikergesetz</li>", driver)
    is_that_both = is_that_gruppe and is_that_psychologe
    trans_and_psychologe = is_founded_queer and is_that_psychologe
    trans_and_gruppe_and_psychologe = trans_and_psychologe and is_that_gruppe
    set_thera_data_value(url, "psychologe", is_that_psychologe)
    set_thera_data_value(url, "heilpraktiker", is_that_hpg)
    set_thera_data_value(url, "sexualitaet", is_that_sexual)
    set_thera_data_value(url, "gruppe", is_that_gruppe)
    set_thera_data_value(url, "gruppe_and_psychologe", is_that_both)
    set_thera_data_value(url, "psychologe_check", True)
    set_thera_data_value(url, "trans", is_founded_queer)
    set_thera_data_value(url, "queer_check", True)
    set_thera_data_value(url, "email_check", False)
    set_thera_data_value(url, "has_email", False)
    set_thera_data_value(url, "trans_and_psychologe", trans_and_psychologe)
    set_thera_data_value(url, "trans_and_gruppe_and_psychologe", trans_and_gruppe_and_psychologe)
    if is_that_sexual:
       print("Sex Therapeut")
    if is_that_psychologe:
       print("Psycho Therapeut >.< -> Der dein Verstand der Norm angleicht!!!!")
    if is_that_gruppe:
       print("Gruppentherapie!!!!")
    if is_that_both:
       print("Beides!!!!")
    if is_founded_queer:
       if not url in email_check:
          trans_profil[url] = ""
          save_data(trans_profil, "trans_profil")
          if is_that_psychologe:
             trans_profil_psychologe[url] = ""
             save_data(trans_profil_psychologe, "trans_profil_psychologe")
          if is_that_gruppe:
             trans_profil_gruppe[url] = ""
             save_data(trans_profil_gruppe, "trans_profil_gruppe")
          if is_that_both:
             trans_profil_both[url] = ""
             save_data(trans_profil_both, "trans_profil_both")
    elif not url in email_check:
        if is_that_sexual:
           no_trans_profil[url] = ""
           save_data(no_trans_profil, "no_trans_profil")
           if is_that_psychologe:
              no_trans_profil_psychologe[url] = ""
              save_data(no_trans_profil_psychologe, "no_trans_profil_psychologe")
           if is_that_gruppe:
              no_trans_profil_gruppe[url] = ""
              save_data(no_trans_profil_gruppe, "no_trans_profil_gruppe")
           if is_that_both:
              no_trans_profil_both[url] = ""
              save_data(no_trans_profil_both, "no_trans_profil_both")
        else:
           no_trans_and_sexual_thera[url] = ""
           save_data(no_trans_and_sexual_thera, "no_trans_and_sexual_thera")
           if is_that_psychologe:
              no_trans_and_sexual_thera_psychologe[url] = ""
              save_data(no_trans_and_sexual_thera_psychologe, "no_trans_and_sexual_thera_psychologe")
           if is_that_gruppe:
              no_trans_and_sexual_thera_gruppe[url] = ""
              save_data(no_trans_and_sexual_thera_gruppe, "no_trans_and_sexual_thera_gruppe")
           if is_that_both:
              no_trans_and_sexual_thera_both[url] = ""
              save_data(no_trans_and_sexual_thera_both, "no_trans_and_sexual_thera_both")
    psychologe_check[url] = ""
    save_data(psychologe_check, "psychologe_check")
    
    with open('./jquery.js', 'r') as jquery_js: 
        # 3) Read the jquery from a file
        jquery = jquery_js.read() 
        # 4) Load jquery lib
        driver.execute_script(jquery)
        
    with open('./find_wait_time.js', 'r') as fwt_js: 
        # 3) Read the jquery from a file
        fwt = fwt_js.read() 
        # 4) Load jquery lib
        driver.execute_script(fwt)
    wait_time = driver.execute_script("return document.querySelector('#generellinfos > .headline + .shadowbox-row + .shadowbox-row.row > div + div > ul:last-child > li:first-child').innerHTML;");
    print("wait_time: " + str(wait_time))
    set_thera_data_value(url, "wartezeit", wait_time)
    print("wait_time: " + wait_time)
    if has_trans_profil_email:
       return trans_profil[url]
 
    if has_no_trans_profil_email:
       return no_trans_profil[url]
 
    jobtitle_selector = "#microsite .therapist-details[itemtype='http://schema.org/Person'] .therapist-name h1 > span[itemprop='jobtitle']"
    name_selector =  "#microsite .therapist-details[itemtype='http://schema.org/Person'] .therapist-name h1 > span[itemprop='name']"
    desc_selector =  "#microsite .therapist-details .therapist-name h2[itemprop='description']"
    jobtitle = driver.execute_script("return document.querySelector(arguments[0]).innerHTML;", jobtitle_selector)
    name = driver.execute_script("return document.querySelector(arguments[0]).innerHTML;", name_selector)
    description = driver.execute_script("return document.querySelector(arguments[0]).innerHTML;", desc_selector)
    set_thera_data_value(url, "jobtitle", jobtitle)
    set_thera_data_value(url, "name", name)
    set_thera_data_value(url, "description", description)
    print("jobtitle: " + jobtitle)
    print("name: " + name)
    print("description: " + description)
    try:
        contact_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#contact-button')))
    except Exception as e: 
        print(e)
        print("exception")
        set_thera_data_value(url, "email_check", True)
        set_thera_data_value(url, "has_email", False)
        return is_founded_queer

    with open('./contact_button.js', 'r') as cb_js: 
        # 3) Read the jquery from a file
        cb = cb_js.read() 
        # 4) Load jquery lib
        driver.execute_script(cb)

    email_address_value = driver.execute_script("return window.getDecryptedEmail();");
    len_email_address_value = len(email_address_value)
    time.sleep(1)
    if len(email_address_value) > 0:
       set_thera_data_value(url, "email", email_address_value)
       set_thera_data_value(url, "email_check", True)
       set_thera_data_value(url, "has_email", True)
    else:
       set_thera_data_value(url, "has_email", False)
    if is_founded_queer:
        trans_profil[url] = email_address_value
        save_data(trans_profil, "trans_profil")
        if is_that_psychologe:
           trans_profil_psychologe[url] = email_address_value
           save_data(trans_profil_psychologe, "trans_profil_psychologe")
        if is_that_gruppe:
           trans_profil_gruppe[url] = ""
           save_data(trans_profil_gruppe, "trans_profil_gruppe")
        if is_that_both:
           trans_profil_both[url] = ""
           save_data(trans_profil_both, "trans_profil_both")
    else:
        if is_that_sexual:
           no_trans_profil[url] = email_address_value
           save_data(no_trans_profil, "no_trans_profil")
           if is_that_psychologe:
              no_trans_profil_psychologe[url] = email_address_value
              save_data(no_trans_profil_psychologe, "no_trans_profil_psychologe")
           if is_that_gruppe:
              no_trans_profil_gruppe[url] = email_address_value
              save_data(no_trans_profil_gruppe, "no_trans_profil_gruppe")
           if is_that_both:
              no_trans_profil_both[url] = email_address_value
              save_data(no_trans_profil_both, "no_trans_profil_both")
        else:
           no_trans_and_sexual_thera[url] = email_address_value
           save_data(no_trans_and_sexual_thera, "no_trans_and_sexual_thera")
           if is_that_psychologe:
              no_trans_and_sexual_thera_psychologe[url] = email_address_value
              save_data(no_trans_and_sexual_thera_psychologe, "no_trans_and_sexual_thera_psychologe")
           if is_that_gruppe:
              no_trans_and_sexual_thera_gruppe[url] = email_address_value
              save_data(no_trans_and_sexual_thera_gruppe, "no_trans_and_sexual_thera_gruppe")
           if is_that_both:
              no_trans_and_sexual_thera_both[url] = email_address_value
              save_data(no_trans_and_sexual_thera_both, "no_trans_and_sexual_thera_both")
    psychologe_check[url] = email_address_value
    save_data(psychologe_check, "psychologe_check")

def is_trans(url):
    if url in trans_profil or url in trans_profil_gruppe or url in trans_profil_psychologe:
       return True
    elif url in no_trans_profil or url in no_trans_profil_gruppe or url in no_trans_and_sexual_thera_psychologe or url in no_trans_and_sexual_thera:
       return False
    else:
       return None

def is_psychologe(url):
    if url in trans_profil_psychologe:
       return True
       
    if url in no_trans_profil_psychologe:
       return True
       
    if url in no_trans_and_sexual_thera_psychologe:
       return True
       
def is_gruppe(url):
    if url in trans_profil_gruppe:
       return True
       
    if url in no_trans_profil_gruppe:
       return True
       
    if url in no_trans_and_sexual_thera_gruppe:
       return True
       
def is_both(url):
    if url in trans_profil_both:
       return True
       
    if url in no_trans_profil_both:
       return True
       
    if url in no_trans_and_sexual_thera_both:
       return True

downloadDefaultDirectory = '.'
headlessmode = False
options = webdriver.ChromeOptions()
options_test = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.add_argument("--disable-renderer-backgrounding");
options.add_argument("--disable-background-timer-throttling");
options.add_argument("--disable-backgrounding-occluded-windows");
options.add_argument("--disable-client-side-phishing-detection");
options.add_argument("--disable-crash-reporter");
options.add_argument("--disable-oopr-debug-crash-dump");
options.add_argument("--no-crash-upload");
options.add_argument("--disable-gpu");
options.add_argument("--disable-extensions");
options.add_argument("--disable-low-res-tiling");
options.add_argument("--log-level=3");
options.add_argument("--silent");
options.add_argument("--disable-search-engine-choice-screen")
options.add_argument("--headless=new")
options.add_argument("--window-position=-2400,-2400")
options_test.add_argument("--disable-search-engine-choice-screen")
prefs = {
    'download.default_directory': downloadDefaultDirectory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
}
options.add_experimental_option('prefs', prefs)
options_test.add_experimental_option('prefs', prefs)
if not headlessmode:
   selected_options = options_test
else:
   selected_options = options
driver = webdriver.Chrome(options=selected_options)
haveLogin = False
closeDriver = False
driver.get("https://www.therapie.de/psychotherapie/-verfahren-/online-therapie/-ort-/alle-orte/")

try:
    zwickau = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.list-columns a[href="/psychotherapie/-verfahren-/online-therapie/-ort-/zwickau/"]')))
except TimeoutException as e:
    print("Couldn't find: " + str("zwickau"))
    pass

with open('./jquery.js', 'r') as jquery_js: 
    # 3) Read the jquery from a file
    jquery = jquery_js.read() 
    # 4) Load jquery lib
    driver.execute_script(jquery)

with open('./therapiede_list.js', 'r') as therapiede_list_js: 
    # 3) Read the jquery from a file
    therapiede_list = therapiede_list_js.read() 
    # 4) Load therapiede_list lib
    driver.execute_script(therapiede_list)
    # 5) Execute your command 
#lat=51.1638175&lon=10.447831111111112&search_radius=0
#https://www.latlong.net/category/cities-83-15.html
       
try:
    thera_cool = WebDriverWait(driver, 70).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-columns.thera_cool")))
    thera_links = driver.execute_script('return document.querySelectorAll(".list-columns.thera_cool a.thera_link");')
    thera_links_new = []
    thera_links_neww = []
    thera_links_loc = []
    thera_links_neww = {}
    thera_links_new_y = {}
    if is_data("thera_links_neww"):
       thera_links_neww = load_data("thera_links_neww")
    if is_data("thera_links_new_y"):
       thera_links_new_y = load_data("thera_links_new_y")
    if not "thera_links_new" in thera_links_new_y:
       thera_links_new_y["thera_links_new"] = []
    if not "thera_links_loc" in thera_links_new_y:
       thera_links_new_y["thera_links_loc"] = []
    if not "all_lat_lon_keys" in thera_links_new_y:
       thera_links_new_y["all_lat_lon_keys"] = []
    save_data(thera_links_new_y, "thera_links_new_y")
    for i in range(len(thera_links_new_y["thera_links_new"]), len(thera_links)):
        print("hallo " + str(i))
        print(thera_links[i].get_attribute("href"))
        noname = driver.execute_script('return $(arguments[0]).hasClass("noname");',  thera_links[i])
        if noname:
           thera_link_get = driver.execute_script('return $(arguments[0]).data("href")',  thera_links[i])
        else:
           thera_link_get = driver.execute_script('return $(arguments[0]).attr("href")',  thera_links[i])
        thera_link_get_loc = driver.execute_script('return $(arguments[0]).data("locx")',  thera_links[i])
        thera_links_new.append(thera_link_get)
        thera_links_loc.append(thera_link_get_loc)
        if not thera_link_get in thera_links_neww:
           thera_links_neww[thera_link_get] = {}
           thera_links_neww[thera_link_get]["search_results"] = []
           thera_links_neww[thera_link_get]["completed"] = False
    thera_links_new_y["thera_links_new"] = thera_links_new
    thera_links_new_y["thera_links_loc"] = thera_links_loc
    save_data(thera_links_new_y, "thera_links_new_y")
    noo_search_results = []
    noo_search_results_loc = {}
    noo_search_results_li = []
    noo_search_results_li_loc = {}
    hel_search_results = []
    hel_search_results_loc = {}
    trans_thera_email_loc = {}
    no_trans_thera_email_loc = {}
    st = "https://www.therapie.de"
    creamy_thera = {}
    if is_data("creamy_thera"):
       creamy_thera = load_data("creamy_thera")
    
    creamy_thera_keys = list(creamy_thera.keys())

    creamy_thera_li = {}
    loc_all_lat_lon = get_all_lat_lon_mod()
    all_lat_lon_keys = list(loc_all_lat_lon.keys())
    len_all_lat_lon_keys = len(loc_all_lat_lon)
    len_all_lat_lon_keys_y = len(thera_links_new_y["all_lat_lon_keys"])
    print("len_lat " + str(len_all_lat_lon_keys))
    allDistance = 0
    flat = 0
    flng = 0
    distanceSet = False
    for i in range(len_all_lat_lon_keys_y, len_all_lat_lon_keys):    
        all_lat_lon_key = all_lat_lon_keys[i]
        all_lat_lon_value = loc_all_lat_lon[all_lat_lon_key]
        lat = round(all_lat_lon_value["lat"], 3)
        lng = round(all_lat_lon_value["lng"], 3)
        if not distanceSet:
           flat = lat 
           flng = lng
           distanceSet = True
           continue
        
        distance = calcDistanceBetweenPoints(driver, flat, flng, lat, lng)
        allDistance += distance
        allDistance = round(allDistance, 3)
        print("distance: " + str(distance))
        print("allDistance: " + str(allDistance))
        if allDistance > 70 or distance > 70:
           new_link = "{0}/therapeutensuche/ergebnisse/?arbeitsschwerpunkt=0&verfahren=37&search_radius=0&lat={1}&lon={2}".format(st,flat,flng)
           thera_links_new.append(new_link)
           thera_links_loc.append(all_lat_lon_key)
           thera_links_new_y["all_lat_lon_keys"].append(all_lat_lon_key)
           if not new_link in thera_links_neww:
              thera_links_neww[new_link] = {}
              thera_links_neww[new_link]["search_results"] = []
              thera_links_neww[new_link]["completed"] = False
           allDistance = 0
           distance = 0
           flat = 0
           flng = 0
           distanceSet = False
                 
        #new_link = "{0}/therapeutensuche/ergebnisse/?arbeitsschwerpunkt=0&verfahren=37&search_radius=0&lat={1}&lon={2}".format(st,lat,lng)
        #print(lng)
        #thera_links_new.append(new_link)
        #thera_links_loc.append(all_lat_lon_key)
    thera_links_new_y["thera_links_new"] = thera_links_new
    thera_links_new_y["thera_links_loc"] = thera_links_loc
    save_data(thera_links_new_y, "thera_links_new_y")
    nos = []
    if is_data("trans_profil"):
       trans_profil = load_data("trans_profil")
    if is_data("no_trans_profil"):
       no_trans_profil = load_data("no_trans_profil")
    trans_thera_email_all = []
    trans_thera_email_all_psychologe = []
    trans_thera_email_all_gruppe = []
    trans_thera_email_all_both = []
    no_trans_thera_email_all_psychologe = []
    no_trans_thera_email_all_gruppe = []
    no_trans_thera_email_all_both = []
    no_trans_and_sexual_thera_email_all = []
    no_trans_and_sexual_thera_email_all_psychologe = []
    no_trans_and_sexual_thera_email_all_gruppe = []
    no_trans_and_sexual_thera_email_all_both = []
    for i in range(0, len(thera_links_new)):
        thera_link_get = thera_links_new[i]
        thera_link_get_loc = thera_links_loc[i]
        hel_search_results_loc[thera_link_get_loc] = []
        trans_thera_email_loc[thera_link_get_loc] = []
        no_trans_thera_email_loc[thera_link_get_loc] = []
        no = {}
        no["search_results"] = []
        no["search_results"+thera_link_get_loc] = []
        
       # if thera_links_neww[thera_link_get]["completed"]:
        #   t_search_results = thera_links_neww[thera_link_get]["search_results"]
         #  for j in range(0, len(t_search_results)):
          #     hel_search_results_loc[thera_link_get_loc].append(t_search_results[j])
           #    hel_search_results.append(t_search_results[j])
            #   write_the_file("all", hel_search_results)   
             #  write_the_file(thera_link_get_loc, hel_search_results_loc[thera_link_get_loc])
              # no["search_results"].append(t_search_results[j])
               #if not t_search_results[j] in creamy_thera:
                #  creamy_thera[t_search_results[j]] = True
                 # save_data(creamy_thera, "creamy_thera")
        #   continue
        #no_search_results = []
        print(thera_link_get)
        try:
            driver.get(thera_link_get)
            time.sleep(3)
        except:
            print("thera_Get_linkj; " + thera_link_get)
            continue
        search_results = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results ul.search-results-list")))
        search_results = driver.execute_script('return document.querySelectorAll(".search-results ul.search-results-list li.panel a");')
        for x in range(0, len(search_results)):
            ele_url = driver.execute_script('return arguments[0].getAttribute("href");', search_results[x])
            if ele_url == None:
               x = x - 1
               continue
            sr = st + str(ele_url)
            if sr in creamy_thera:
               continue
            thera_links_neww[thera_link_get]["search_results"].append(st)
            creamy_thera[sr] = True
            save_data(creamy_thera, "creamy_thera")
            #no_search_results.append(sr)
            hel_search_results.append(sr)
            hel_search_results_loc[thera_link_get_loc].append(sr)
            write_the_file("all", hel_search_results)   
            write_the_file(thera_link_get_loc, hel_search_results_loc[thera_link_get_loc])
            no["search_results"].append(sr)
        pagenav_bottom = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#pagenav-bottom")))
        thera_link_first_href = driver.execute_script('return $("#pagenav-bottom li.active a").last().attr("href");')
        print(thera_link_first_href)
        no["thera_link_get"] = thera_link_get
        no["thera_link_first_href"] = thera_link_first_href
        thera_link_first =  int(driver.execute_script('return $("#pagenav-bottom li.active a").last().html();'), 10)
        no["thera_link_first"] = thera_link_first
        thera_link_next = int(driver.execute_script('return $("#pagenav-bottom li.active + li a").last().html();'), 10)
        no["thera_link_next"] = thera_link_next
        print(thera_link_next)
        thera_link_last = int(driver.execute_script('return $("#pagenav-bottom li:not(.active):not(.next) a").last().html();'), 10)
        no["thera_link_last"] = thera_link_last
        print(thera_link_last)
        for j in range(thera_link_next, thera_link_last + 1):
            next_page_link = thera_link_first_href + "&page=" + str(j)
            driver.execute_script('document.location.href=arguments[0]', next_page_link)
            time.sleep(3)
            new_search_results = driver.execute_script('return document.querySelectorAll(".search-results ul.search-results-list li.panel a");')
            for x in range(0, len(new_search_results)):
                ele_url = driver.execute_script('return arguments[0].getAttribute("href");', new_search_results[x])
                if ele_url == None:
                   x = x - 1
                   continue
                sr = st + str(ele_url)
                if sr in creamy_thera:
                   continue
                thera_links_neww[thera_link_get]["search_results"].append(st)
                creamy_thera[sr] = True
                save_data(creamy_thera, "creamy_thera")
                #no_search_results.append(sr)
                hel_search_results.append(sr)
                hel_search_results_loc[thera_link_get_loc].append(sr)
                no["search_results"].append(sr)
                write_the_file("all", hel_search_results)   
                write_the_file(thera_link_get_loc, hel_search_results_loc[thera_link_get_loc])
        
        thera_links_neww[thera_link_get]["completed"] = True
        save_data(thera_links_neww, "thera_links_neww")
        no_search_results = no["search_results"]
        no["trans_thera_email_all"] = []
        no["no_trans_thera_email_all"] = []
        no["trans_thera_email_all_psychologe"] = []
        no["trans_thera_email_all_gruppe"] = []
        no["trans_thera_email_all_both"] = [] 
        no["no_trans_thera_email_all_psychologe"] = []
        no["no_trans_thera_email_all_gruppe"] = []
        no["no_trans_thera_email_all_both"] = []
        no["no_trans_and_sexual_thera_email_all"] = []
        no["no_trans_and_sexual_thera_email_all_psychologe"] = []
        no["no_trans_and_sexual_thera_email_all_gruppe"] = []
        no["no_trans_and_sexual_thera_email_all_both"] = []
        for k in range(0, len(no_search_results)):
            url = no_search_results[k]
            if search_queer_words_on_thera_profil_ex(url, driver):
               email_address_value = trans_profil[url]
               no["trans_thera_email_all"].append(email_address_value)
               if is_psychologe(url):
                  trans_thera_email_all_psychologe.append(email_address_value)
                  no["trans_thera_email_all_psychologe"].append(email_address_value)
               if is_gruppe(url):
                  trans_thera_email_all_gruppe.append(email_address_value)
                  no["trans_thera_email_all_gruppe"].append(email_address_value)
               if is_both(url):
                  trans_thera_email_all_both.append(email_address_value)
                  no["trans_thera_email_all_both"].append(email_address_value)
               trans_thera_email_all.append(email_address_value)
               write_the_file(thera_link_get_loc + "_trans_thera_email", no["trans_thera_email_all"])
               write_the_file(thera_link_get_loc + "_trans_thera_email_psychologe", no["trans_thera_email_all_psychologe"])
               write_the_file(thera_link_get_loc + "_trans_thera_email_both", no["trans_thera_email_all_both"])
            elif url in no_trans_and_sexual_thera:
               email_address_value = no_trans_and_sexual_thera[url] 
               no["no_trans_and_sexual_thera_email_all"].append(email_address_value)
               no_trans_and_sexual_thera_email_all.append(email_address_value)
               if is_psychologe(url):
                  no_trans_and_sexual_thera_email_all_psychologe.append(email_address_value)
                  no["no_trans_and_sexual_thera_email_all_psychologe"].append(email_address_value)
               if is_gruppe(url):
                  no_trans_and_sexual_thera_email_all_gruppe.append(email_address_value)
                  no["no_trans_and_sexual_thera_email_all_gruppe"].append(email_address_value)
               if is_both(url):
                  no_trans_and_sexual_thera_email_all_both.append(email_address_value)
                  no["no_trans_and_sexual_thera_email_all_both"].append(email_address_value)
               write_the_file(thera_link_get_loc + "_no_trans_and_sexual_thera_email", no["no_trans_and_sexual_thera_email_all"])
               write_the_file(thera_link_get_loc + "_no_trans_and_sexual_thera_email_psychologe", no["no_trans_and_sexual_thera_email_all_psychologe"])
               write_the_file(thera_link_get_loc + "_no_trans_and_sexual_thera_email_gruppe", no["no_trans_and_sexual_thera_email_all_gruppe"])
               write_the_file(thera_link_get_loc + "_no_trans_and_sexual_thera_email_both", no["no_trans_and_sexual_thera_email_all_both"])
            elif url in no_trans_profil:
               email_address_value = no_trans_profil[url] 
               no["no_trans_thera_email_all"].append(email_address_value)
               no_trans_thera_email_all.append(email_address_value)
               if is_psychologe(url):
                  no_trans_thera_email_all_psychologe.append(email_address_value)
                  no["no_trans_thera_email_all_psychologe"].append(email_address_value)
               if is_gruppe(url):
                  no_trans_thera_email_all_gruppe.append(email_address_value)
                  no["no_trans_thera_email_all_gruppe"].append(email_address_value)
               if is_both(url):
                  no_trans_thera_email_all_both.append(email_address_value)
                  no["no_trans_thera_email_all_both"].append(email_address_value)
               write_the_file(thera_link_get_loc + "_no_trans_thera_email", no["no_trans_thera_email_all"])
               write_the_file(thera_link_get_loc + "_no_trans_thera_email_psychologe", no["no_trans_thera_email_all_psychologe"])
               write_the_file(thera_link_get_loc + "_no_trans_thera_email_gruppe", no["no_trans_thera_email_all_gruppe"])
               write_the_file(thera_link_get_loc + "_no_trans_thera_email_both", no["no_trans_thera_email_all_both"])
            
            change_thera(url)
            save_data(trans_profil, "trans_profil")
            save_data(no_trans_profil, "no_trans_profil")
            save_data(trans_thera_email_all_psychologe, "trans_thera_email_all_psychologe")
            save_data(no_trans_thera_email_all_psychologe, "no_trans_thera_email_all_psychologe")
            save_data(trans_thera_email_all_gruppe, "trans_thera_email_all_gruppe")
            save_data(no_trans_thera_email_all_gruppe, "no_trans_thera_email_all_gruppe")
            save_data(trans_thera_email_all_both, "trans_thera_email_all_both")
            save_data(no_trans_thera_email_all_both, "no_trans_thera_email_all_both")
            save_data(no_trans_and_sexual_thera, "no_trans_and_sexual_thera")
            save_data(no_trans_and_sexual_thera_psychologe, "no_trans_and_sexual_thera_psychologe")
            save_data(no_trans_and_sexual_thera_email_all, "no_trans_and_sexual_thera_email_all")
            save_data(no_trans_and_sexual_thera_email_all_psychologe, "no_trans_and_sexual_thera_email_all_psychologe")
            save_data(no_trans_and_sexual_thera_email_all_gruppe, "no_trans_and_sexual_thera_email_all_gruppe")
            save_data(no_trans_and_sexual_thera_email_all_both, "no_trans_and_sexual_thera_email_all_both")
        save_data(trans_profil, "trans_profil")
        save_data(no_trans_profil, "no_trans_profil")
    
    write_the_file("trans_thera_email_all", trans_thera_email_all)
    write_the_file("trans_thera_email_all_psychologe", trans_thera_email_all_psychologe)
    write_the_file("trans_thera_email_all_gruppe", trans_thera_email_all_gruppe)
    write_the_file("no_trans_thera_email_all", no_trans_thera_email_all)
    write_the_file("no_trans_thera_email_all_psychologe", no_trans_thera_email_all_psychologe)
    write_the_file("no_trans_thera_email_all_gruppe", no_trans_thera_email_all_gruppe)  
    write_the_file("no_trans_thera_email_all_both", no_trans_thera_email_all_both)  
    write_the_file("all", hel_search_results)    
        #noooo_search_results = []
        #no_trans_thera_email = []
        #trans_thera_email = []
        #for i in range(0, len(no_search_results)):
            #sr = no_search_results[i]
            #if not search_queer_words_on_thera_profil(sr, driver):
            #   if len(no_trans_thera_email) > 0:
            #      write_the_file(thera_link_get_loc + "_no_trans_thera_email", no_trans_thera_email)
            #   if len(no_trans_thera_email_all) > 0:
            #      write_the_file("all_no_trans_thera_email_all", no_trans_thera_email_all)
            #  continue
            #noo_search_results.append(sr) 
            #noooo_search_results.append(sr)
            #if len(trans_thera_email) > 0:
            #   write_the_file(thera_link_get_loc + "_trans_thera_email", trans_thera_email)
            #if len(trans_thera_email_all) > 0:
            #   write_the_file("all_trans_thera_email_all", trans_thera_email_all)
        #no_search_results = noooo_search_results  
        #if len(no_search_results) > 0:
        #   write_the_file(thera_link_get_loc, no_search_results)
        #thera_links_neww.append(no)
    trans_thera_email_all = []
    no_trans_thera_email_all = []
    has_trans_all = False
    has_no_trans_all = False
    for i in range(0, len(thera_links_loc)):
        thera_link_get_loc = thera_links_loc[i]
        hel_search_results_loc_temp = hel_search_results_loc[thera_link_get_loc]
        write_the_file(thera_link_get_loc, hel_search_results_loc_temp)
        
        #for j in range(0, len(hel_search_results_loc_temp)):
        #    url = hel_search_results_loc_temp[j]
        #    if search_queer_words_on_thera_profil_ex(url, driver):
        #       email_address_value = trans_profil[url]
        #       trans_thera_email_loc[thera_link_get_loc].append(email_address_value)
        #       trans_thera_email_all.append(email_address_value)
        #       write_the_file("trans_thera_email_all", trans_thera_email_all)
        #       write_the_file(thera_link_get_loc + "_trans_thera_email", trans_thera_email_loc[thera_link_get_loc])
        #    else:
        #       email_address_value = no_trans_profil[url]
        #       no_trans_thera_email_loc[thera_link_get_loc].append(email_address_value)
        #       no_trans_thera_email_all.append(email_address_value)
        #       write_the_file("no_trans_thera_email_all", no_trans_thera_email_all)
        #       write_the_file(thera_link_get_loc + "_no_trans_thera_email", no_trans_thera_email_loc[thera_link_get_loc])
        #   
        #if len(trans_thera_email_loc[thera_link_get_loc]) > 0:
        #   write_the_file(thera_link_get_loc + "_trans_thera_email", trans_thera_email_loc[thera_link_get_loc])
        #   has_trans_all = True
        #   
        #if len(no_trans_thera_email_loc[thera_link_get_loc]) > 0:
        #   write_the_file(thera_link_get_loc + "_no_trans_thera_email", no_trans_thera_email_loc[thera_link_get_loc])
        #   has_no_trans_all = True

    #if has_trans_all:
    #  write_the_file("trans_thera_email_all", trans_thera_email_all)
    #if has_no_trans_all:
    #   write_the_file("no_trans_thera_email_all", no_trans_thera_email_all)
    #if len(noo_search_results) > 0:
    #   write_the_file("all", noo_search_results)
    #if len(trans_thera_email_all) > 0:
    #   write_the_file("all_trans_thera_email_all", trans_thera_email_all)
    #current_i = 0
    #max_i = len(noo_search_results) - 1
    #open_urls = int(input("Wieviele Urls oeffnen?"))
    #while open_urls > 0 and current_i <= max_i:
    #    for i in range(current_i, current_i + open_urls):
    #        if i <= max_i:
    #           driver.get(noo_search_results[i])
    #           body = driver.find_element_by_tag_name("body")
    #           body.send_keys(Keys.CONTROL + 't')
    #           input("Weiter?")
    #    current_i = current_i + open_urls
    #    open_urls = int(input("Wieviele Urls oeffnen?"))
    #print(noo_search_results)   
except TimeoutException as e:
    print("Couldn't find: " + str("thera_cool"))
    pass
    
time.sleep(99999)