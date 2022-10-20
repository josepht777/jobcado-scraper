from bs4 import BeautifulSoup
import time
import api
link = 'https://vn.applycv.com'

def getJobInfo(job_link, browser):
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    print('applycv', job_link)
    
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
            
            if label == 'Mức lương':
                salary = value
                
            if label == 'Địa điểm':
                location = value
            
            if label == 'Hạn nộp hồ sơ':
                deadline = value           
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
    
def getJobList(URL, browser):    
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    job_elements = soup.select('div.item')
    
    for job_element in job_elements:
        if len(job_element.find_all("a", class_="title", href=True)) > 0:
            job_link = job_element.find_all("a", class_="title", href=True)[0]
            job_link = link + job_link['href']
            getJobInfo(job_link, browser)
            time.sleep(2)
    
    
def run(browser):
    URL_List = []
    URL_List.append("https://vn.applycv.com/viec-lam")
    for page in range(2, 8000): #20000
        URL_List.append(link + '/viec-lam?page=' + str(page))
    URL_List.reverse()
    for URL in URL_List:
        try:
            getJobList(URL, browser)
        finally:
            time.sleep(3)