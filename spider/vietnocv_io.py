from bs4 import BeautifulSoup
import time
import api
# Requires login, currently we have no login system that would not be tracked but we could create a junk email for a one off.
def getJobInfo(job_link, browser):
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    
    print('Vietnocv', job_link)
    
    title = ''
    if len(soup.select('h1.MuiTypography-h1')) > 0:
        title = soup.select('h1.MuiTypography-h1')[0].get_text(strip = True)
    
    #print('Title >>>>>> ' + title)

    description = ''
    if len(soup.select('div.MuiCardContent-root')) > 1:
        description = soup.select('div.MuiCardContent-root')[1].get_text(strip = True)
        if len(description.split('Chi tiết công việc')) > 1:
            description = description.split('Chi tiết công việc')[1]
            
    requirement = ''
    
    #print('Description >>>> ', description)
    
    
    content = soup.get_text(strip = True)
    
    # with open('careerlink.txt', 'w', encoding='utf-8') as f:
    #     f.write(content)
    
    salary = ''
    if len(content.split('LƯƠNG')) > 1 and len(content.split('LƯƠNG')[1].split('date_range')) > 0:
        salary = content.split('LƯƠNG')[1].split('date_range')[0].strip()
    
    #print('SALARY >>> ' + salary)
    
    deadline = ''
    if len(content.split('Hết hạn: ')) > 1:
        deadline = content.split('Hết hạn: ')[1][0:10]
    #print('Deadline >>>', deadline)
    
    location = ''
    if len(content.split('ĐỊA ĐIỂM')) > 1 and len(content.split('ĐỊA ĐIỂM')[1].split('access_time')) > 0:
        location = content.split('ĐỊA ĐIỂM')[1].split('access_time')[0].strip()
    #print('Location >>>', location)
    
    company_name = ''
    if len(soup.select('a.MuiTypography-noWrap')) > 0:
        company_name = soup.select('a.MuiTypography-noWrap')[0].get_text(strip = True)
    
    #print('Company name >>> ', company_name)
    
    company_description = ''
    company_size = ''
    
    company_logo = ''
    if len(soup.find_all('img', alt='Logo')) > 0:
        company_logo = soup.find_all('img', alt='Logo')[0]['src']
    #print('Company logo >>>', company_logo)
    language = ''
    post_date = ''
    
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
    
def getJobList(browser):
    link = 'https://vietcv.io'
    URL = link + '/jobs/discover'
    
    browser.get(URL)
    
    for page in range(0, 5):
        time.sleep(1)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    
    job_elements = soup.select('li.MuiListItem-root')
    
    for job_element in job_elements:
        job_link = link + job_element.select('a.MuiTypography-root')[0]['href']
        getJobInfo(job_link, browser)
        time.sleep(1)
        #return
        
def run(browser):
    try:
        getJobList(browser)
    finally:
        time.sleep(1)