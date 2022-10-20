from bs4 import BeautifulSoup
import time
import api
import concurrent.futures

link = 'https://timviecnhanh.com'

def getJobInfo(browser, job_link):
    print('Link   --->  ' + job_link)
    
    browser.get(job_link)
    
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    title = ''
    
    if len(soup.select('span.title')) > 0:
        title = soup.select('span.title')[0].get_text(strip=True)
        
    print('Title ---> ' + title)
    if(title == ''):
        return
    
    description = ''
    requirement = ''
    
    table = soup.select('tbody')
    
    if len(table) > 0:
        cell = table[0].select('td')
        if len(cell) > 1:
            description = cell[1].get_text(strip=True)
        if len(cell) > 3:
            requirement = cell[3].get_text(strip=True)

    # print('Description -->  ', description)
    # print('Requirement -->  ', requirement)
    
    company_name = ''
    if len(soup.select('div.title-employer')) > 0:
        company_name = soup.select('div.title-employer')[0].get_text(strip=True)
    # print('Company name -->  ' + company_name)
    
    company_description = ''
    
    location = ''
    if len(soup.select('div.company-job-address')) > 0:
        location = soup.select('div.company-job-address')[0].get_text(strip=True)
    # print('Location --> ' + location)
    
    company_size = ''
    
    company_logo = ''
    if len(soup.select('img.lazyloaded')) > 0:
        company_logo = soup.select('img.lazyloaded')[0]['src']
    # print('Company Logo -->  ' + company_logo)
    
    salary = ''
    if len(soup.select('article')) > 0 and len(soup.select('article')[0].select('li')) and len(soup.select('article')[0].select('li')[0]):
        salary = soup.select('article')[0].select('li')[0].get_text(strip=True).split(':')[1]
    # print('Salary --> ' + salary)
    
    post_date = ''
    if len(soup.select('article')) > 0 and len(soup.select('article')[0].select('div')) > 0:
        post_date = soup.select('article')[0].select('div')[0].get_text(strip=True)
        post_date = post_date.split('|')[0].split(': ')[1]
    # print('Post date --> ' + post_date)
    
    language = ''
    benefits = ''
    deadline = ''
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
        language
        # benefits
    )
    
def getJobList(browser, URL):
    # URL = link + '/vieclam/timkiem?action=search&page=' + str(pageN)
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    table = soup.find('tbody')
    job_elements = table.find_all('a', class_="title-job", href=True)
    job_link_list = []
    for job_element in job_elements:
        job_link_list.append(link + job_element['href'])
    #     job_link = link + job_element['href']
    #     print('job_link', job_link)
    #     getJobInfo(job_link, browser)
    #     time.sleep(2)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = ((browser, b) for b in job_link_list)
        executor.map(lambda p: getJobInfo(*p), args)


    
def run(browser, search_terms_list):
    URL_List = []

    for page in range(2, 51):
        URL_List.append(link + '/vieclam/timkiem?action=search&page=' + str(page))
    #     print('search_term', page)
    #     getJobList(page, browser)
    #     time.sleep(3)

    for search_term in search_terms_list:
        URL_List.append(link + '/vieclam/timkiem?q=' + search_term)
    
    # add blank string
    URL_List.append("https://timviecnhanh.com/vieclam/timkiem?")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = ((browser, b) for b in URL_List)
        executor.map(lambda p: getJobList(*p), args)