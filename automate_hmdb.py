from splinter import Browser
from selenium import webdriver
import time

def automate_hmdb(table):
    # add chrome driver to execute
    # To use this, you need to download chromedriver from https://chromedriver.chromium.org/downloads and choose
    # the version of google chrome you are using. Then, specify the path in executable variable like below.
    executable = {'executable_path': r'/Users/phucnguyen/Desktop/chromedriver'}

    options = webdriver.ChromeOptions()

    options.add_argument("--window-size=1400,900")
    options.add_argument("--start-maximized")

    options.add_argument("--disable-notification")

    browser = Browser('chrome', **executable, headless = False, options = options)

    browser.visit("https://hmdb.ca/spectra/ms/search")

    # find id for textarea - query_masses
    # query_mass = browser.find_by_id("query_masses")

    browser.fill("query_masses", '\n'.join(str(t) for t in table))

    adduct_type = browser.find_by_id("adduct_type")
    adduct_type.select("M+H")

    browser.fill("tolerance", "10")

    tolerance = browser.find_by_id("tolerance_units")
    tolerance.select("ppm")

    # submit button -- search
    submit = browser.find_by_name("commit").first.click()
    # time.sleep(3)
    # download as csv
    submit_1 = browser.find_by_value("Download Results As CSV").first.click()