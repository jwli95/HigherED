import math
import json
from playwright.sync_api import Playwright, sync_playwright, expect


all_records=[]

def run(playwright: Playwright, jobcat: int, pagenum: int, cur_page: int) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()
    start_row = cur_page*pagenum+1
    url = "https://www.higheredjobs.com/faculty/search.cfm?JobCat={}&StartRow={}&SortBy=4&NumJobs={}&filterby=&CatType=".format(jobcat, start_row, pagenum)
    page.goto(url)
    results = page.locator("#js-results")
    single_record = {}
    count = results.locator(".col-sm-7").count()
    for i in range(count):
        left = results.locator(".col-sm-7").nth(i).inner_text()
        left_all_info = left.split("\n")
        link = results.locator(".col-sm-7 a").nth(i).get_attribute('href')
        full_link = "https://www.higheredjobs.com/faculty/"+link
        right = results.locator(".col-sm-5").nth(i).inner_text()
        right_all_info = right.split("\n")

        if len(right_all_info) >= 2:
            single_record={"position":left_all_info[0],"link":full_link,"university":left_all_info[1],"location":left_all_info[2],"major":right_all_info[0],"post_date":right_all_info[1].split(' ')[1]}
        else:
            single_record={"position":left_all_info[0],"link":full_link,"university":left_all_info[1],"location":left_all_info[2],"major":right_all_info[0],"post_date":""}

        all_records.append(single_record)
    
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    # Find number of ADs
    filename = 'CE.json'

    if filename == 'CS.json':
        url = 'https://www.higheredjobs.com/faculty/search.cfm?JobCat=102&CatName=Computer%20Science'
        jobcat = 102
    elif filename == 'CE.json':
        url = 'https://www.higheredjobs.com/faculty/search.cfm?JobCat=116&CatName=Computer%20Engineering'
        jobcat = 116
    elif filename == 'EE.json':
        url = 'https://www.higheredjobs.com/faculty/search.cfm?JobCat=117&CatName=Electrical%20Engineering'
        jobcat = 117

    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    n_ad = page.locator(".text-nowrap").nth(0).inner_text().split(' ')
    n_ad = int(''.join(n_ad[5].split(',')))
    print('Total Records:', n_ad)
    context.close()
    browser.close()

    # Parameters
    total_records = n_ad
    num_single_page = 100
    

    total_page=math.ceil(total_records / num_single_page)
    print('Total Pages:', total_page)

    for cur_page in range(total_page):
        print('Current Page:', cur_page)
        run(playwright, jobcat, num_single_page, cur_page)

    print('Obtained Records:', len(all_records))

    with open(filename, 'w') as f:
        json.dump(all_records, f)
