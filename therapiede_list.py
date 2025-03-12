from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
def write_the_file(name="0", content=[]):
    target = os.path.join("thera_lists", name+"_theras_online.txt")
    with open(target, 'w') as f:
         for line in content:
             f.write(f"{line}\n")

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
    zwickau = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.list-columns a[href="/psychotherapie/-verfahren-/online-therapie/-ort-/zwickau/"]')))
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

try:
    thera_cool = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-columns.thera_cool")))
    thera_links = thera_cool.find_elements(By.CSS_SELECTOR, ".list-columns a.thera_link")
    thera_links_new = []
    thera_links_neww = []
    thera_links_loc = []
    for i in range(0, len(thera_links)):
        print("hallo " + str(i))
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
    st = "https://www.therapie.de"
    creamy_thera = {}
    creamy_thera_li = {}
    for i in range(0, len(thera_links_new)):
        thera_link_get = thera_links_new[i]
        thera_link_get_loc = thera_links_loc[i]
        no = {}
        no_search_results = []
        no_search_results_li = []
        print(thera_link_get)
        try:
            driver.get(thera_link_get)
            time.sleep(3)
        except:
            print("thera_Get_linkj; " + thera_link_get)
            continue
        search_results = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results ul.search-results-list")))
        search_results = driver.execute_script('return document.querySelectorAll(".search-results ul.search-results-list li.panel a");')
        search_results_x = driver.execute_script('return document.querySelectorAll(".search-results ul.search-results-list li.panel");')
        for x in range(0, len(search_results)):
            sr = st + driver.execute_script('return arguments[0].getAttribute("href");', search_results[x])
            if sr in creamy_thera:
               continue
            creamy_thera[sr] = True
            noo_search_results.append(sr)
            no_search_results.append(sr)
        for x in range(0, len(search_results_x)):
            sr = search_results_x[x]
            if sr in creamy_thera_li:
               continue
            creamy_thera_li[sr] = True
            noo_search_results_li.append(sr)
            no_search_results_li.append(sr)
        pagenav_bottom = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#pagenav-bottom")))
        thera_link_first_href = driver.execute_script('return $("#pagenav-bottom li.active a").last().attr("href");')
        print(thera_link_first_href)
        no["fhref"] = thera_link_get
        no["href"] = thera_link_first_href
        thera_link_first =  int(driver.execute_script('return $("#pagenav-bottom li.active a").last().html();'), 10)
        no["first"] = thera_link_first
        thera_link_next = int(driver.execute_script('return $("#pagenav-bottom li.active + li a").last().html();'), 10)
        print(thera_link_next)
        no["next"] = thera_link_next
        thera_link_last = int(driver.execute_script('return $("#pagenav-bottom li:not(.active):not(.next) a").last().html();'), 10)
        print(thera_link_last)
        no["last"] = thera_link_last
        for j in range(thera_link_next, thera_link_last + 1):
            next_page_link = thera_link_first_href + "&page=" + str(j)
            driver.execute_script('document.location.href=arguments[0]', next_page_link)
            time.sleep(2)
            new_search_results = driver.execute_script('return document.querySelectorAll(".search-results ul.search-results-list li.panel a");')
            new_search_results_x = driver.execute_script('return document.querySelectorAll(".search-results ul.search-results-list li.panel");')
            for x in range(0, len(new_search_results)):
                sr = st + driver.execute_script('return arguments[0].getAttribute("href");', new_search_results[x])
                if sr in creamy_thera:
                   continue
                creamy_thera[sr] = True
                noo_search_results.append(sr)
                no_search_results.append(sr)
                
            for x in range(0, len(new_search_results_x)):
                sr = new_search_results_x[x]
                if sr in creamy_thera_li:
                   continue
                creamy_thera_li[sr] = True
                noo_search_results_li.append(sr)
                no_search_results_li.append(sr)
            
            write_the_file(thera_link_get_loc, no_search_results)
            noo_search_results_loc[thera_link_get_loc] = no_search_results
            noo_search_results_li_loc[thera_link_get_loc] = no_search_results_li
        thera_links_neww.append(no)
    write_the_file("all", noo_search_results)
    current_i = 0
    max_i = len(noo_search_results) - 1
    open_urls = int(input("Wieviele Urls oeffnen?"))
    while open_urls > 0 and current_i <= max_i:
        for i in range(current_i, current_i + open_urls):
            if i <= max_i:
               driver.get(noo_search_results[i])
               body = driver.find_element_by_tag_name("body")
               body.send_keys(Keys.CONTROL + 't')
               input("Weiter?")
        current_i = current_i + open_urls
        open_urls = int(input("Wieviele Urls oeffnen?"))
    print(noo_search_results)   
except TimeoutException as e:
    print("Couldn't find: " + str("thera_cool"))
    pass
    
time.sleep(99999)