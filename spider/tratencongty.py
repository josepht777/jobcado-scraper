from bs4 import BeautifulSoup
import time
import api
link = 'https://www.tratencongty.com'

# https://www.tratencongty.com/company/192eed108-cong-ty-tnhh-dich-vu-du-lich-malisa/

def getJobInfo(job_link, browser):
    job_link = "https://www.tratencongty.com/company/192eed108-cong-ty-tnhh-dich-vu-du-lich-malisa/"
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    
    title = ''
    if len(soup.select('h1.title')) > 0:
        title = soup.select('h1.title')[0].get_text(strip = True)
    
    description = ''
    requirement = ''
    
    if len(soup.select('div.detail-info')) > 0:
        content = soup.select('div.detail-info')[0]
        if len(content.select('div.ct')) > 0:
            description = content.select('div.ct')[0].get_text(strip = True)
        if len(content.select('div.ct')) > 1:
            requirement = content.select('div.ct')[-1].get_text(strip = True)
            
    company_name = ''
    company_description = ''
    company_size = ''
    company_logo = ''
    
    if len(soup.select('div.box-company')) > 0:
        company_box = soup.select('div.box-company')[0]

        if len(company_box.select('img')) > 0:
            company_logo = company_box.select('img')[0]['src']
        if len(company_box.select('h2.name')) > 0:
            company_name = company_box.select('h2.name')[0].get_text(strip = True)  
    
    salary = ''
    deadline = ''
    language = ''
    post_date = ''
    location = ''
    
    if len(soup.select('div.params')) > 0:
        for item in soup.select('div.params')[0].select('div.item'):
            if len(item.select('.param')) > 0:
                item = item.select('.param')[0]
            else:
                continue
            
            label = ''
            if len(item.select('span.param-label')) > 0:
                label = item.select('span.param-label')[0].get_text(strip = True)
            value = ''
            if len(item.select('.value')) > 0:
                value = item.select('.value')[0].get_text(strip = True)
            elif len(item.select('span')) > 1:
                value = item.select('span')[-1].get_text(strip = True)
            
            if label == 'M???c l????ng':
                salary = value
                
            if label == '?????a ??i???m':
                location = value
            
            if label == 'H???n n???p h??? s??':
                deadline = value           
    benefits = ''
    weight = 1
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
        benefits,
        weight
    )


def getJobList(URL, browser):    
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    job_elements = soup.select('div.search-results')
    
    for job_element in job_elements:
        if len(job_element.find_all("a", href=True)) > 0:
            job_link = job_element.find_all("a", href=True)[0]
            job_link = link + job_link['href']
            getJobInfo(job_link, browser)
            time.sleep(2)
    
    
def run(browser, search_terms_list):
    # https://www.tratencongty.com/?page=29764
    URL_List = []
    for page in range(1, 29764):
        URL_List.append(link + '/?page=' + str(page))

    for URL in URL_List:
        try:
            getJobList(URL, browser)
        finally:
            time.sleep(3)