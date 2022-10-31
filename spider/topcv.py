from pickle import FALSE
from bs4 import BeautifulSoup
import time
import api
import concurrent.futures

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

def getJobInfo(browser, job_link):
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    
    title = ''
    if len(soup.select('h1')) > 0:
        title = soup.select('h1')[0].get_text(strip = True)
    print('Title >>>>>> ' + title)

    description = ''
    requirement = ''
    benefits = ''
    location = ''
    salary = ''
    deadline = ''
    company_name = ''
    company_description = ''
    company_size = ''
    company_logo = ''
    language = ''
    post_date = ''

    if len(soup.select('div.job-deadline')) > 0:
        deadline = getTextFromList(soup.select('div.job-deadline'))
    # print('Deadline >>>', deadline)

    if len(soup.select('div.box-item')) > 0:
        for content in soup.select('div.box-item'):
            if(content):
                if(content.select('strong')):
                    if(content.select('span')):
                        if('Mức lương' in content.select('strong')[0].get_text(strip = True)):
                            salary = content.select('span')[0].get_text(strip = True)

    if len(soup.select('div.box-address')) > 0:
        answer = ''
        for item in soup.select('div.box-address'):
            if('Địa điểm' in item.select('p')[0]):
                answer = answer + "\b " + item.select('div')[0].get_text(strip = True)
            if('Địa điểm làm việc' in item.select('p')[0]):
                answer = answer + "\b " + item.select('div')[0].get_text(strip = True)
        location = answer
    
    # print('location >>> ', location)
        
    if len(soup.select('div.job-data')) > 0:
        for item in soup.select('div.job-data'):
            if(len(item) > 0):
                for index, itemTitle in enumerate(item.select('h3')):
                    if('Mô tả công việc' in itemTitle):
                        if(len(item.select('div.content-tab')[index].findChildren())> 0):
                            description = getTextFromList(item.select('div.content-tab')[index].findChildren())
                    if('Yêu cầu ứng viên' in itemTitle):
                        if(len(item.select('div.content-tab')[index].findChildren())> 0):
                            requirement = getTextFromList(item.select('div.content-tab')[index].findChildren())
                    if('Quyền lợi' in itemTitle): # 'Quyền lợi được hưởng'
                        if(len(item.select('div.content-tab')[index].findChildren())> 0):
                            benefits = getTextFromList(item.select('div.content-tab')[index].findChildren())
                for index, itemTitle in enumerate(item.select('h2')):
                    if('Mô tả công việc' in itemTitle):
                        if(len(item.select('div.content-tab')[index].findChildren())> 0):
                            description = getTextFromList(item.select('div.content-tab')[index].findChildren())
                    if('Yêu cầu ứng viên' in itemTitle):
                        if(len(item.select('div.content-tab')[index].findChildren())> 0):
                            requirement = getTextFromList(item.select('div.content-tab')[index].findChildren())
                    if('Quyền lợi' in itemTitle):
                        if(len(item.select('div.content-tab')[index].findChildren())> 0):
                            benefits = getTextFromList(item.select('div.content-tab')[index].findChildren())

    # print('SALARY >>> ' + salary) # Mức lương
    # print('Description >>>> ', description)
    # print('requirement >>>> ', requirement)
    # print('benefits >>>> ', benefits)

    if len(soup.select('div.box-info-company')) > 0:
        company = soup.select('div.box-info-company')[0]
        if(len(company.select('div.box-item')) > 0):
            item = company.select('div.box-item')
            if(len(item) > 0):
                for details in item:
                    if(len(details.select('p.title')) > 0):
                        if(details.select('p.title')[0].get_text(strip = True) == 'Giới thiệu'):
                            company_description = getTextFromList(details.select('span.content'))
                        if(details.select('p.title')[0].get_text(strip = True) == 'Quy mô'):
                            company_size = getTextFromList(details.select('span.content'))


    # print('company_description >>> ', company_description)
    # print('post_date >>>', post_date, language)
    # print('company_size >>>', company_size) # nhân viên 

    if len(soup.select('div.company-title')) > 0:
        company_name = getTextFromList(soup.select('div.company-title'))

    # print('Company name >>> ', company_name)

    if(len(soup.select('img.img-responsive')) > 0):
        company_logo = soup.select('img.img-responsive')[0]['src']

    # print('Company logo >>>', company_logo)
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

def getJobListFromPagination(browser, URL):
    # link = 'https://www.topcv.vn/tim-viec-lam-'
    # URL = link + search_term + ''
    print('URL', URL)

    browser.get(URL)
    try:
        soup = BeautifulSoup(browser.page_source, features="html.parser")
    except Exception as e:
        print('Error @ 125: ', e.message)
        return

    if(len(soup.select('div.job-item')) > 0):
        job_link_list = []
        job_elements = soup.select('div.job-item')
        # for job_element in job_elements:
        #     job_link_list.append(job_element.select('a')[0]['href'])
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     args = ((browser, b) for b in job_link_list)
        #     executor.map(lambda p: getJobInfo(*p), args)
        for job_element in job_elements:
            job_link_list.append(job_element.select('a')[0]['href'])
            job_link = job_element.select('a')[0]['href']
            print('link', job_link)
            getJobInfo(browser, job_link)
            time.sleep(1)

def getJobList(browser, URL):
    # link = 'https://www.topcv.vn/tim-viec-lam-'
    # URL = link + search_term + ''
    print('URL', URL)

    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    if(len(soup.select('div.job-item')) > 0):
        job_link_list = []
        job_elements = soup.select('div.job-item')
        for job_element in job_elements:
            job_link_list.append(job_element.select('a')[0]['href'])
            job_link = job_element.select('a')[0]['href']
            print('link', job_link)
            getJobInfo(browser, job_link)
            time.sleep(1)
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     args = ((browser, b) for b in job_link_list)
        #     executor.map(lambda p: getJobInfo(*p), args)
    if(len(soup.select('ul.pagination')) > 0):
        pagination_List = []
        pagination = soup.select('ul.pagination')[0]
        pagination_length = len(pagination.select('li'))
        if(pagination_length> 0):
            total = int(getTextFromList(pagination.select('li')[pagination_length -2]))
            if(total > 1):
                for page in range(1, total):
                    pagination_List.append(URL + '?salary=0&exp=0&sort=top_related&page=' + str(page))
                # print(len(pagination_List))
                # with concurrent.futures.ThreadPoolExecutor() as executor:
                #     args = ((browser, b) for b in pagination_List)
                #     executor.map(lambda p: getJobListFromPagination(*p), args)
                # pagination_List.reverse()
                for pagi in pagination_List:
                    getJobListFromPagination(browser, pagi)

def run(browser, search_terms_list):
    URL_List =[]
    link = 'https://www.topcv.vn/tim-viec-lam-'
    # for search_term in search_terms_list:
    #     URL_List.append(link + search_term.replace("+","").replace(" ", "-").replace("/", ""))
    # URL_List.append("https://www.topcv.vn/tim-viec-lam-moi-nhat")
    for i in range(2, 400):
        URL_List.append("https://www.topcv.vn/tim-viec-lam-moi-nhat?salary=0&exp=0&sort=top_related&page="+ str(i))
    try:
        # print('topcv', search_term)
        # getJobList(browser, search_term.replace("+","").replace(" ", "-").replace("/", ""))
        for URL in URL_List:
            getJobList(browser, URL)
            time.sleep(1)
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     args = ((browser, b) for b in URL_List)
        #     executor.map(lambda p: getJobList(*p), args)
        # time.sleep(1)
    finally:
        time.sleep(3)
    
    