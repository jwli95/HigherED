from playwright.sync_api import Playwright, sync_playwright, expect
import math

all_records=[]

def run(playwright: Playwright,pagenum:int,cur_page:int) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()
    start_row=cur_page*pagenum+1
    print(start_row)
    url="https://www.higheredjobs.com/faculty/search.cfm?JobCat=102&StartRow={}&SortBy=4&NumJobs={}&filterby=&CatType=".format(start_row,pagenum)
    page.goto(url)
    results=page.locator("#js-results")
    single_record={}
    count=results.locator(".col-sm-7").count()
    for i in range(count):
        left = results.locator(".col-sm-7").nth(i).inner_text()
        left_all_info=left.split("\n")
        right=results.locator(".col-sm-5").nth(i).inner_text()
        right_all_info=right.split("\n")

        print(left_all_info)

        # test link
        link = results.locator(".col-sm-7").nth(i).inner_html()
        print(link)

        if len(right_all_info) == 2:
            single_record={"position":left_all_info[0],"university":left_all_info[1],"location":left_all_info[2],"major":right_all_info[0],"post_date":right_all_info[1]}
        else:
            single_record={"position":left_all_info[0],"university":left_all_info[1],"location":left_all_info[2],"major":right_all_info[0],"post_date":""}
        all_records.append(single_record)

        break
    
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    # Find number of ADs
    url = 'https://www.higheredjobs.com/faculty/search.cfm?JobCat=102&CatName=Computer%20Science'
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    n_ad = page.locator(".text-nowrap").nth(0).inner_text().split(' ')
    n_ad = int(''.join(n_ad[5].split(',')))
    print(n_ad)

    # Parameters
    total_records = n_ad
    num_single_page = 100
    

    total_page=math.ceil(total_records/num_single_page)
    print(total_page)
    for cur_page in range(total_page):
        print(cur_page)
        run(playwright,num_single_page,cur_page)

        break
    print(all_records)
    print(len(all_records))
    
    context.close()
    browser.close()
