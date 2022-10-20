from bs4 import BeautifulSoup
import time
import api
import concurrent.futures

link = 'https://www.careerlink.vn'

def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def flatten(input_list):
    output_list = []
    for element in input_list:
        if type(element) == list:
            output_list.extend(flatten(element))
        else:
            output_list.append(element)
    return output_list

def getTextFromList(list):
    if(len(list) > 0):
        list = flatten(list)
        answer = ''
        for item in list:
            answer = answer + "\b " + item.get_text(strip = True)
        if len(answer) > 0:
            return answer
        else:
            return
    else:
        return 0



def getJobInfo (browser, job_link):
    print('job_link ->', job_link)
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    
    title = ''
    if len(soup.select('h1.job-title')) > 0:
        title = soup.select('h1.job-title')[0].get_text(strip=True)
    
    # print('title', title)
    description = ''
    requirement = ''

    if(len(soup.select('div#section-job-skills'))>0):
        requirement = getTextFromList(soup.select('div#section-job-skills')[0].select('p'))
    if(len(soup.select('div#section-job-description'))>0):
        description = getTextFromList(soup.select('div#section-job-description')[0].select('p'))
    # print('description', description)
    # print('requirement', requirement)
    
    company_name = ''
    if len(soup.select('p.org-name')) > 0:
        company_name = soup.select('p.org-name')[0].get_text(strip=True)

    # print('company_name', company_name)
    company_description = ''
    if len(soup.select('div.company-profile')) > 0:
        company_description = soup.select('div.company-profile')[0].get_text(strip=True)

    # print('company_description', company_description)

    location = ''
    for mapParent in soup.find('i', class_='cli-map-pin-line').parent():
        if(len(mapParent.select('span'))>0):
            location = mapParent.select('span')[0].get_text(strip=True)
        if(len(mapParent.select('a'))>0):
            location = location + mapParent.select('a')[0].get_text(strip=True)

    # print('location', location)
 
    company_size = ''
    if len(soup.select('div.job-summary-item')) > 0:
        for peopleCounter in soup.select('div.job-summary-item'):
            if(len(peopleCounter.select('div'))>0):
                if(peopleCounter.select('div')[0].get_text(strip=True) == "Tuổi"):
                    company_size = peopleCounter.select('div')[1].get_text(strip=True)
        
    # print('company_size', company_size)

    company_logo = ''
    if(len(soup.find_all('img', class_='company-img'))>0):
        company_logo = soup.find_all('img', class_='company-img')[0].get('src')

    # print('company_logo', company_logo)

    salary = ''
    for currency in soup.find('i', class_='cli-currency-circle-dollar').parent():
        salary = salary + "\b " + currency.get_text(strip=True).replace('MONTH', '')

    # print('salary', salary)
    post_date = ''
    for dateParent in soup.find('i', class_='cli-calendar').parent():
        post_date = "\b " + post_date + "\b " + dateParent.get_text(strip=True)
    post_date = ' '.join(unique_list(post_date.split()))
    post_date = rchop(post_date, 'tuyển')
    # print('post_date', post_date)
    language = ''
    if len(soup.select('div.job-expire > p.mb-0 > strong')) > 0:
        language = soup.select('div.job-expire > p.mb-0 > strong')[0].get_text(strip=True)

    # print('language', language)
    benefits = ""
    deadline = ""
    print('API')

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

def searchPages (browser, URL):
    print('url', URL)
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    job_elements = soup.find_all("a", class_="job-link", href=True)
    if(len(job_elements)> 0):
        job_link_list = []
        for job_element in job_elements:
            job_link_list.append(link + job_element['href'])
            # job_link = link + job_element['href'] 
            # getJobInfo(job_link, browser)
            # time.sleep(2)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            args = ((browser, b) for b in job_link_list)
            executor.map(lambda p: getJobInfo(*p), args)
    
def getJobList (browser, URL):
    # search_term = "Quản lý dự án"
    # link = 'https://www.careerlink.vn'
    # URL = link + '/viec-lam/k/' + search_term
    print('url', URL)
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    job_link_list = []
    job_elements = soup.find_all("a", class_="job-link", href=True)
    if(len(job_elements)> 0):
        for job_element in job_elements:
            job_link_list.append(link + job_element['href'] )
    #     for job_element in job_elements:
    #         job_link = link + job_element['href'] 
    #         getJobInfo(job_link, browser)
    #         time.sleep(2)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = ((browser, b) for b in job_link_list)
        executor.map(lambda p: getJobInfo(*p), args)
    # ?page=2
    if(len(soup.select('ul.pagination'))>0):
        last_tab = len(soup.select('ul.pagination')[0].select('li')) -1
        last_page_div = soup.select('ul.pagination')[0].select('li')[last_tab -1]
        last_page_a = last_page_div.select('a')[0]
        last_page = int(last_page_a.get_text(strip=True))
        if(last_page > 1):
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     args = ((browser, b) for b in job_link_list)
            #     executor.map(lambda p: getJobList(*p), args)
            new_URL_list = []
            for i in range(2, last_page):
                new_URL_list.append(URL + '?page=' + str(i))
            with concurrent.futures.ThreadPoolExecutor() as executor:
                args = ((browser, b) for b in new_URL_list)
                executor.map(lambda p: searchPages(*p), args)
                # searchPages(browser, new_URL)
                # time.sleep(1)
            
def run(browser, search_terms_list):
    URL_List = []
    for search_term in search_terms_list:
        URL_List.append(link + '/viec-lam/k/' + search_term.replace("+","").replace(" ", "%20").replace("/", ""))
    URL_List.append("https://www.careerlink.vn/vieclam/list")
    try:
        # getJobList(browser, search_term.replace("+","").replace(" ", "%20").replace("/", ""))
        # time.sleep(1)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            args = ((browser, b) for b in URL_List)
            executor.map(lambda p: getJobList(*p), args)
    finally:
        time.sleep(3)
    # browser.quit()