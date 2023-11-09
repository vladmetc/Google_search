"""
Collect into scv-file 500+ Google News mentions of 'entity' Kraken Cryptocurrency Exchange
over 31+ days w/i 2022-2023.
"""
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSelectorException
import pickle
import time
import pandas as pd
from GoogSrchTools.timestampFit import form_ts
from GoogSrchTools.delays import t_delay
import os

safari_options = Options()
safari_options.add_argument("user-data-dir=selenium")
safari_options.add_argument("--headless")

scam_group = ["scam", "fake", "fraud", "attack", "unauthorized", "phishing", "hack", "fraud",
              "ponzi", "decept", "swindle", "hoax", "prank", "ruse", "con", "lawsuit", "victim"
              ]

# String to search the Google News with
srch_str = '%22Kraken%22+exchange+crypto'

# Results per page
page_res = 100

# Target results to collect
given_res = 540

# Results number to search from
start_num = 0

# Custom period 'min' date(starting and exreme)
strt_date = time.mktime(time.strptime('4, 3, 2023', '%m, %d, %Y'))
strt_extr = time.mktime(time.strptime('9, 1, 2023', '%m, %d, %Y'))

page_No = 1
start_t = time.time()

# Storage for selected key values that to be unique (to check duplicates against)
unique = []

# Storage for search results
srch_res = []

while len(srch_res) < 540 or strt_date < strt_extr:
    # Set custom period 'min' date
    min_m = time.localtime(strt_date).tm_mon
    min_d = time.localtime(strt_date).tm_mday
    min_Y = time.localtime(strt_date).tm_year

    # Set custom period 'max' date as 'min' date + 5 weeks
    stp_date = strt_date + 35 * 24 * 3600
    max_m = time.localtime(stp_date).tm_mon
    max_d = time.localtime(stp_date).tm_mday
    max_Y = time.localtime(stp_date).tm_year

    q_num = f"&num={page_res}"
    q_start = f"&start={start_num}"
    q_period = (f"&tbs=cdr%3A1%2Ccd%5F"
                f"min%3A{min_m}%2F{min_d}%2F2023%2Ccd%5Fmax%3A{max_m}%2F{max_d}%2F2023%2Clr%3Alang%5F1en"
                )

    url = ('https://www.google.com/search?q=' + srch_str +
           q_period + '&tbm=nws' +
           '&gl=US&hl=en%2DGB&lr=lang%5Fen&ie=UTF%2D8&oe=UTF%2D8' +
           q_start + q_num
           )
    print("url: ", url)
    print("Searching up from result", start_num)

    driver = webdriver.Safari(options=safari_options)
    # Global implicit waiting time before throwing an exception if an element is not found:
    driver.implicitly_wait(10)

    driver.get(url)

    # Working with cookies
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except Exception:
        print("error working with cookies")
        raise

    # Pause
    start_t = t_delay(start_t, 'driver_get')

    # Check if the query matches any Google Search results
    try:
        extabar = driver.find_element(By.CSS_SELECTOR, 'div[class="WE0UJf NyYcvd"]')
        if not extabar.text:
            print("No extabar-text, found no results, trying another period")
            driver.close()
            strt_date += 35 * 24 * 3600
            start_num = 0
            continue
    except Exception:
        print("extabar error")
        raise
    print("Google search <div id='extabar'>: ", extabar.text)

    # Pause
    start_t = t_delay(start_t, 'Checking "About <number> of results"')

    # Get list of date elements
    try:
        dates = driver.find_elements(By.CSS_SELECTOR, 'div[class="OSrXXb rbYSKb LfVVr"]')
    except InvalidSelectorException:
        raise
    print("Found %d 'date' elements on page %d" % (len(dates), page_No))
    # Reformat timestamps to Y-m-d
    fdates = [form_ts(date.text) for date in dates]

    # Pause
    start_t = t_delay(start_t, 'Finding "date" elements')

    # Get list of title elements
    try:
        titles = driver.find_elements(By.CSS_SELECTOR, 'div[class="n0jPhd ynAwRc MBeuO nDgy9d"]')
    except InvalidSelectorException:
        raise
    print("Found %d 'title' elements on page %d" % (len(titles), page_No))

    # Pause
    start_t = t_delay(start_t, 'Finding "title" elements')

    # Get list of text elements
    try:
        texts = driver.find_elements(By.CSS_SELECTOR, 'div[class="GI74Re nDgy9d"]')
    except InvalidSelectorException:
        raise
    print("Found %d 'text' elements on page %d" % (len(texts), page_No))

    # Pause
    start_t = t_delay(start_t, 'Finding "text" elements')

    # Getting the links
    try:
        dyn_elems = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[jsname="YKoRaf"]')))
    except InvalidSelectorException:
        raise
    links = [href.get_attribute('href') for href in dyn_elems]

    # Pause
    start_t = t_delay(start_t, 'Finding links')

    if len(fdates) == len(titles) == len(texts) == len(links):
        # Number of articles on the current page
        cpage_res = len(fdates)
        print(f"Found {cpage_res} articles on page.{page_No}")

        # Search results => list of dicts
        for i in range(len(fdates)):
            # check if article's 'text' value is not duplicating
            if texts[i].text in unique:
                continue
            unique.append(texts[i].text)
            # Put article in the list of search results removing unneeded 'newlines' and
            # marking scam-related articles with '+'
            scam_mark = ''
            for k in scam_group:
                if k in titles[i].text or k in texts[i].text:
                    scam_mark = '+'
                    break
            srch_res.append(
                {'timestamp': fdates[i],
                 'title': titles[i].text.replace('\n', ''),
                 'text': texts[i].text.replace('\n', ''),
                 'link': links[i],
                 'scam': scam_mark
                 }
            )

        # Total number of articles found sofar
        ttl_res = len(unique)
        print(f"Total found {ttl_res} unique articles\n")

        # Run on the search taken total results found
        if ttl_res >= given_res:
            print(f"GoogleSearch reached the target number.\nTotal found {ttl_res} articles")
            pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
            driver.quit()

            # Dict to csv with pandas
            df = pd.DataFrame(srch_res)
            print("'srch_res' -> DataFrame:\n", df.tail())

            if os.path.isfile('re_csv/articles_data.csv'):
                os.remove('re_csv/articles_data.csv')
            if not os.path.isfile("re_csv/articles_data.csv") or os.stat("re_csv/articles_data.csv").st_size == 0:
                df.to_csv('articles_data.csv', index=False)
            else:
                df.to_csv('articles_data.csv', mode='a', index=False, header=False)
            pr_csv = pd.read_csv('re_csv/articles_data.csv')
            print("Pandas read 5 lines end of csv file':\n", pr_csv.iloc[-5:, :])
            break

        elif cpage_res < page_res:
            print(f"Done page {page_No}! {ttl_res} articles found so far.\n")
            strt_date += 35 * 24 * 3600
            start_num = 0
            page_No += 1
            driver.close()

        elif cpage_res == page_res:
            start_num += 100
            page_No += 1
            driver.close()
    else:
        print(f"Warning: elements count on page.{page_No} not matching!")
        break
