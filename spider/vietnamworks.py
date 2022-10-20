from bs4 import BeautifulSoup
import time
import api
link = 'https://www.vietnamworks.com/'

def getJobInfo(job_link, browser):
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    
    title = ''
    if len(soup.select('h1.job-title')) > 0:
        title = soup.select('h1.job-title')[0].get_text(strip = True)
    
    # print('Title >>>>>> ' + title)

    description = ''
    if len(soup.select('div.description')) > 0:
        description = soup.select('div.description')[0].get_text(strip = True)
    
    # print('Description >>>> ', description)
    
    requirement = ''
    if len(soup.select('div.requirements')) > 0:
        requirement = soup.select('div.requirements')[0].get_text(strip = True)
    
    # print('requirement >>>> ', requirement)

    content = soup.get_text(strip = True)
    
    # with open('careerlink.txt', 'w', encoding='utf-8') as f:
    #     f.write(content)
    
    salary = ''
    if len(soup.select('span.salary')) > 0:
        salary = soup.select('span.salary')[0].get_text(strip = True)
    
    # print('SALARY >>> ' + salary)
    
    deadline = ''
    if len(soup.select('span.expiry')) > 0:
        deadline = soup.select('span.expiry')[0].get_text(strip = True)
    # print('Deadline >>>', deadline)
    
    location = ''
    # span.company-location or div.location-name
    if len(soup.select('div.location-name')) > 1:
        location = soup.select('div.location-name')[1].get_text(strip = True)

    # print('Company location >>> ', location)
    
    company_name = ''
    if len(soup.select('div.company-name')) > 0:
        company_name = soup.select('div.company-name')[0].get_text(strip = True)
    
    # print('Company name >>> ', company_name)
    
    # view-tab-cominfo
    # company-info__description
    # company-info__description-text
    company_description = ''
    if len(soup.select('p.company-info__description-text')) > 0:
        company_description = soup.select('p.company-info__description-text')[0].get_text(strip = True)
    
    # print('company_description >>> ', company_description)

    # company-info__contact--block
    # contact-text
    company_size = ''
    if len(soup.select('p.contact-text')) > 1:
        company_size = soup.select('p.contact-text')[1].get_text(strip = True)
    # print('company_size >>>', company_size)
    
    company_logo = ''
    if len(soup.select('img.logo')) > 0:
        company_logo = soup.select('img.logo')[0]['src']
    # print('Company logo >>>', company_logo)
    language = ''
    post_date = ''
    if len(soup.select('span.content')) > 0:
        post_date = soup.select('span.content')[0].get_text(strip = True)
        language = soup.select('span.content')[4].get_text(strip = True)
    # print('post_date >>>', post_date, language)
    
    benefits = ''
    api.insert(
        title,
        job_link,
        description,
        '',
        requirement,
        company_name,
        company_description,
        location,
        company_size,
        company_logo,
        salary,
        post_date,
        deadline,
        language,
        # benefits
    )


def getJobList(browser, URL):
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    job_elements = soup.select('div.job-info-wrapper')

    for job_element in job_elements:
        job_link = link + job_element.select('a.job-title')[0]['href']
        getJobInfo(job_link, browser)
        time.sleep(1)

def run(browser, search_terms_list):
    URL_List = []
    # https://www.vietnamworks.com/Kỹ-sư-hệ-thống-kv it add's -kv on the end.
    for search_term in search_terms_list:
        URL_List.append(link + search_term.replace("+", "_plus").replace(" ", "-").replace("/", "-") + "-kv")
    # https://www.vietnamworks.com/tim-viec-lam/tat-ca-viec-lam?filtered=true

    # https://www.vietnamworks.com/tim-viec-lam/tat-ca-viec-lam?filtered=true&page=2
    for i in range(2, 201):
        URL_List.append("https://www.vietnamworks.com/tim-viec-lam/tat-ca-viec-lam?filtered=true&page=" + str(i))

    try:
        print('vietnamworks', search_term)
        getJobList(browser, URL_List)
        time.sleep(1)
    finally:
        time.sleep(3)
    
    