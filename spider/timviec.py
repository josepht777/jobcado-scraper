from bs4 import BeautifulSoup
import time
import api
import concurrent.futures

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

link = 'https://timviec.com.vn/'

def getJobInfo (browser, job_link):
    print('job_link ->', job_link)
    
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    
    title = ''
    location = ''
    salary = ''
    post_date = ''

    if len(soup.select('div.about')) > 0:
        if(len(soup.select('div.about')[0].select('h1'))>0):
            title = soup.select('div.about')[0].select('h1')[0].text.strip()
            post_dateLong = soup.select('div.about')[len(soup.select('div.about')) -1].text.strip()
            post_date = " ".join(line.strip() for line in post_dateLong.splitlines())
        for job_details in soup.select('div.about'): 
            if(len(job_details.select('b'))>0):
                for job_title in job_details.select('b'):
                    if(job_title.text.strip() == 'Khu vực tuyển dụng:'):
                        location_parent = job_title.parent()
                        if(len(location_parent)>1):
                            location = location_parent[1].text.strip()
                    if(job_title.text.strip() == 'Mức lương:'):
                        salary_parent = job_title.parent()
                        if(len(salary_parent)>1):
                            salary = salary_parent[1].text.strip()
    
    # print('title', title)
    # print('salary', salary)
    # print('location', location)
    # print('post_date', post_date)

    # job-detail-left
    description = ''
    requirement = ''
    benefits = ''

    if len(soup.select('div.job-detail-left')) > 0:
        if len(soup.select('div.job-detail-left')[0]) > 0:
            details_row = soup.select('div.job-detail-left')[0]
            for index, details_column in enumerate(details_row):
                if(len(details_column)>1):
                    if(len(details_column.select('h2'))>0):
                        detailsTitles = details_column.select('h2')
                        # detailsContense = details_column.select('div')
                        for detailsTitle in detailsTitles:
                            if(detailsTitle.text.strip() == 'Mô tả công việc'):
                                job_description_parent = detailsTitle.parent()
                                description = job_description_parent[index].text.strip()
                            if(detailsTitle.text.strip() == 'Quyền lợi được hưởng'):
                                benefits_parent = detailsTitle.parent()
                                benefits = benefits_parent[index].text.strip()
                            if(detailsTitle.text.strip() == 'Yêu cầu công việc'):
                                requirement_parent = detailsTitle.parent()
                                requirement = requirement_parent[index].text.strip()
                            if(detailsTitle.text.strip() == 'Yêu cầu hồ sơ'):
                                REQUEST_parent = detailsTitle.parent()
                                requirement = requirement + "\b " + REQUEST_parent[index].text.strip()
    # print(description, requirement, benefits)
    company_name = ''
    company_description = ''
    company_size = ''
    company_logo = ''
    language = ''

    company_tag = soup.find_all('a', text = 'Công ty')
    if(len(company_tag)>0):
        browser.get(company_tag[0]['href'])
        company_soup = BeautifulSoup(browser.page_source, features="html.parser")

        if len(company_soup.select('h1.company-name')) > 0:
            company_name = company_soup.select('h1.company-name')[0].get_text(strip=True)
        # print('company_name', company_name)


        if len(company_soup.select('div.content-about-text')) > 0:
            company_description = company_soup.select('div.content-about-text')[0].get_text(strip=True)
        # print('company_description', company_description)
    
        if(len(company_soup.find_all('img', alt='logo'))>0):
            company_logo = company_soup.find_all('img', alt='logo')[0]['src']
        # print('company_logo', company_logo)

        # print('company_size', company_size)

        # print('language', language)
        # company_tag = soup.find_all('a', text = 'Công ty') Do for each language
    deadline = ''
    print('API insert', title)
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

    
def getJobList (browser, URL):
    # URL = link + 'tim-viec-lam?q=' + search_term
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    job_elements = soup.select("div.item-job-box")
    job_link_list = []
    if(len(job_elements)> 0):
        for job_element in job_elements:
            job_link_list.append(job_element.find_all("a", href=True)[0]['href'])
            # job_link = job_element.find_all("a", href=True)[0]['href']
        #     getJobInfo(job_link, browser)
        #     time.sleep(1)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            args = ((browser, b) for b in job_link_list)
            executor.map(lambda p: getJobInfo(*p), args)
    # &page=2
    # https://timviec.com.vn/tim-viec-lam?order_by=renew_int&page=2
    # Looks like the whole page only has 60 or so jobs.
            
def run(browser, search_terms_list):
    URL_List = []
    for search_term in search_terms_list:
        URL_List.append(link + 'tim-viec-lam?q=' + search_term.replace("+","%2B").replace(" ", "%20").replace("/", "%2F"))
    URL_List.append("https://timviec.com.vn/tim-viec-lam")
        # try:
        #     print('tim-viec', search_term)
        #     getJobList(browser, search_term.replace("+","%2B").replace(" ", "%20").replace("/", "%2F"))
        #     time.sleep(1)
        # finally:
        #     time.sleep(3)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = ((browser, b) for b in URL_List)
        executor.map(lambda p: getJobList(*p), args)