from splinter import Browser
from selenium import webdriver
import time

# open chrome browser and visit website
def browser_open(website_path):
    # add chrome driver to execute
    # To use this, you need to download chromedriver from https://chromedriver.chromium.org/downloads and choose
    # the version of google chrome you are using. Then, specify the path in executable variable like below.
    executable = {'executable_path': r'/Users/phucnguyen/Desktop/chromedriver'}

    options = webdriver.ChromeOptions()

    options.add_argument("--window-size=1400,900")
    options.add_argument("--start-maximized")

    options.add_argument("--disable-notification")

    browser = Browser('chrome', **executable, headless=False, options=options)

    browser.visit(website_path)

    return browser

# visit hmdb.ca to automate
def automate_hmdb(table, adduct, tolerance_number):
    # open hmdb.ca website
    browser = browser_open("https://hmdb.ca/spectra/ms/search")

    # find id for textarea - query_masses
    # query_mass = browser.find_by_id("query_masses")

    browser.fill("query_masses", '\n'.join(str(t - 1) for t in table))

    adduct_type = browser.find_by_id("adduct_type")
    for a in adduct:
        adduct_type.select(a)

    browser.fill("tolerance", tolerance_number)

    tolerance = browser.find_by_id("tolerance_units")
    tolerance.select("ppm")

    # submit button -- search
    submit = browser.find_by_name("commit").first.click()
    # time.sleep(3)
    # download as csv
    submit_1 = browser.find_by_value("Download Results As CSV").first.click()




def automate_kegg(kegg_list):
    # open map pathway website
    browser = browser_open("https://www.genome.jp/kegg/tool/map_pathway1.html")
    # rno mode
    browser.fill("s_map", "rno")

    browser.fill("s_q", '\n'.join(str(k) for k in kegg_list))

    browser.find_by_value("Exec").first.click()