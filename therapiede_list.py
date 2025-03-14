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

search_words_queer = ["Transition", "Transitionsbegleitung", "transident", "lesbisch", "schwul", "bisexuell", "pansexuell", "intersexuell", "polyamor", "queer", "nonbinär", "trans*", "Trans*", "VLSP", "LGBTQ", "LGBTQ+", "LGBTQIA", "Geschlechtsdysphorie"]  
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
def search_queer_words_on_thera_profil_ex(url, driver):
    if url in trans_profil:
       return True
    if url in no_trans_profil:
       return False
    driver.get(url)
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#microsite .shadowbox.therapist-details')))
    except Exception as e:
        print(e)
        print("exception")
        no_trans_profil[url] = ""
        save_data(no_trans_profil, "no_trans_profil")
        return False
    is_founded_queer = search_array_in_page(search_words_queer, driver, search_words_queer_must_found)
    if is_founded_queer:
       trans_profil[url] = ""
       save_data(trans_profil, "trans_profil")
    else:
       no_trans_profil[url] = ""
       save_data(no_trans_profil, "no_trans_profil")
    try:
        contact_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#contact-button')))
    except Exception as e: 
        print(e)
        print("exception")
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
    if is_founded_queer:
       print("founded")
       if len_email_address_value > 0:
          trans_profil[url] = email_address_value
          save_data(trans_profil, "trans_profil")
          print("trans_email: " + email_address_value)
    else:
       if len_email_address_value > 0:
          no_trans_profil[url] = email_address_value
          save_data(no_trans_profil, "no_trans_profil")
          print("no_trans_email: " + email_address_value)
    return is_founded_queer
    
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


if is_data("trans_profil"):
   trans_profil = load_data("trans_profil")
   
if is_data("no_trans_profil"):
   no_trans_profil = load_data("no_trans_profil")

trans_profil_keys = list(trans_profil.keys())
no_trans_profil_keys = list(no_trans_profil.keys())

trans_profil_emails = []
no_trans_profil_emails = []

for i in range(0, len(trans_profil_keys)):
    trans_profil_key = trans_profil_keys[i]
    trans_profil_value = trans_profil[trans_profil_key]
    if not trans_profil_value in trans_profil_emails:
       trans_profil_emails.append(trans_profil_value)
       write_the_file("trans_profil_emails", trans_profil_emails)

write_quermed_online_email_files()
write_all_trans_online_theras(trans_profil_emails)
       
for i in range(0, len(no_trans_profil_keys)):
    no_trans_profil_key = no_trans_profil_keys[i]
    no_trans_profil_value = no_trans_profil[trans_profil_key]
    if not no_trans_profil_value in no_trans_profil_emails:
       no_trans_profil_emails.append(no_trans_profil_value)
       write_the_file("no_trans_profil_emails", no_trans_profil_emails)
       
if len(trans_profil_emails) > 0:
   write_the_file("trans_profil_emails", trans_profil_emails)
       
if len(no_trans_profil_emails) > 0:
   write_the_file("no_trans_profil_emails", no_trans_profil_emails)
       
try:
    thera_cool = WebDriverWait(driver, 70).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-columns.thera_cool")))
    thera_links = driver.execute_script('return document.querySelectorAll(".list-columns.thera_cool a.thera_link");')
    thera_links_new = []
    thera_links_neww = []
    thera_links_loc = []
    for i in range(0, len(thera_links)):
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
    print("len_lat " + str(len_all_lat_lon_keys))
    allDistance = 0
    flat = 0
    flng = 0
    distanceSet = False
    for i in range(0, len_all_lat_lon_keys):    
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
           new_link = "{0}/therapeutensuche/ergebnisse/?arbeitsschwerpunkt=12&verfahren=37&search_radius=0&lat={1}&lon={2}".format(st,flat,flng)
           thera_links_new.append(new_link)
           thera_links_loc.append(all_lat_lon_key)
           allDistance = 0
           distance = 0
           flat = 0
           flng = 0
           distanceSet = False
                 
        #new_link = "{0}/therapeutensuche/ergebnisse/?arbeitsschwerpunkt=12&verfahren=37&search_radius=0&lat={1}&lon={2}".format(st,lat,lng)
        #print(lng)
        #thera_links_new.append(new_link)
        #thera_links_loc.append(all_lat_lon_key)
    nos = []
    if is_data("trans_profil"):
       trans_profil = load_data("trans_profil")
    if is_data("no_trans_profil"):
       no_trans_profil = load_data("no_trans_profil")
    trans_thera_email_all = []
    for i in range(0, len(thera_links_new)):
        thera_link_get = thera_links_new[i]
        thera_link_get_loc = thera_links_loc[i]
        hel_search_results_loc[thera_link_get_loc] = []
        trans_thera_email_loc[thera_link_get_loc] = []
        no_trans_thera_email_loc[thera_link_get_loc] = []
        no = {}
        no["search_results"] = []
        no["search_results"+thera_link_get_loc] = []
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
            sr = st + driver.execute_script('return arguments[0].getAttribute("href");', search_results[x])
            if sr in creamy_thera:
               continue
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
            time.sleep(2)
            new_search_results = driver.execute_script('return document.querySelectorAll(".search-results ul.search-results-list li.panel a");')
            for x in range(0, len(new_search_results)):
                sr = st + driver.execute_script('return arguments[0].getAttribute("href");', new_search_results[x])
                if sr in creamy_thera:
                   continue
                creamy_thera[sr] = True
                save_data(creamy_thera, "creamy_thera")
                #no_search_results.append(sr)
                hel_search_results.append(sr)
                hel_search_results_loc[thera_link_get_loc].append(sr)
                no["search_results"].append(sr)
                write_the_file("all", hel_search_results)   
                write_the_file(thera_link_get_loc, hel_search_results_loc[thera_link_get_loc])
        
        no_search_results = no["search_results"]
        no["trans_thera_email_all"] = []
        no["no_trans_thera_email_all"] = []
        for k in range(0, len(no_search_results)):
            url = no_search_results[k]
            if search_queer_words_on_thera_profil_ex(url, driver):
               email_address_value = trans_profil[url]
               no["trans_thera_email_all"].append(email_address_value)
               trans_thera_email_all.append(email_address_value)
               write_the_file(thera_link_get_loc + "_trans_thera_email", no["trans_thera_email_all"])
            else:
               email_address_value = no_trans_profil[url]
               no["no_trans_thera_email_all"].append(email_address_value)
               trans_thera_email_all.append(email_address_value)
               write_the_file(thera_link_get_loc + "_no_trans_thera_email", no["no_trans_thera_email_all"])
            save_data(trans_profil, "trans_profil")
            save_data(no_trans_profil, "no_trans_profil")
        save_data(trans_profil, "trans_profil")
        save_data(no_trans_profil, "no_trans_profil")
    
    write_the_file("trans_thera_email_all", trans_thera_email_all)   
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