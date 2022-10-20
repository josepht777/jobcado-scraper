from bs4 import BeautifulSoup
import time
import api

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

def getAlternativeJobInfo(job_link, browser):
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    title = ''
    company_name = ''
    company_link = ''
    if(len(soup.select('div.title'))>0):
        title_div = soup.select('div.title')[0].select('h2')
        if(len(title_div)>0):
            title = title_div[0].get_text(strip = True)
    # print('Title >>>>>> ' + title)
    if(len(title) < 1):
        return
    
    if len(soup.select('a.company')[0]) > 0:
        company_name = soup.select('a.company')[0].get_text(strip = True)
        company_link = soup.select('a.company')[0]['href']

    # print('company_name >>>>>> ' + company_name)
    salary = ''
    if len(soup.select('p.salary')[0]) > 0:
        salary = soup.select('p.salary')[0].get_text(strip = True)
    # print('SALARY >>> ' + salary) 

    description = ''
    requirement = ''
    benefits = ''
    location = ''
    if len(soup.select('div.full-content')) > 0:
        for index, content in enumerate(soup.select('div.full-content')):
            for content_title in content.select('h3'):
                if content_title.get_text(strip = True) == 'Mô tả Công việc':
                        content_div = content_title.parent()[1]
                        for content_paragraph in content_div.select('p'):
                            description = description + content_paragraph.get_text(strip = True)
                if content_title.get_text(strip = True) == 'Yêu Cầu Công Việc':
                        requirement_content_div = content_title.parent()[1]
                        for requirement_content_paragraph in requirement_content_div.select('p'):
                            requirement = requirement + requirement_content_paragraph.get_text(strip = True)
                if content_title.get_text(strip = True) == 'THÔNG TIN KHÁC':
                        benefits_content_div = content_title.parent()[1]
                        for benefits_content_paragraph in benefits_content_div.select('li'):
                            benefits = benefits + benefits_content_paragraph.get_text(strip = True)

    # print('Description >>>> ', description)
    # print('requirement >>>> ', requirement)
    # print('benefits >>>> ', benefits)

    if len(soup.select('p.list-workplace')) > 0:
        location = soup.select('p.list-workplace')[0].get_text(strip = True)

    # print('location >>> ', location)

    deadline = ''
    post_date = ''
    if(len(soup.select('em.fa-calendar-times-o'))>0):
        deadline_parent = soup.select('em.fa-calendar-times-o')[0].find_parent('tr')
        if(len(deadline_parent.select('p'))> 1):
            deadline = deadline_parent.select('p')[1].get_text(strip = True)
    # print('Deadline >>>', deadline) 

    if(len(soup.select('em.fa-calendar'))>0):
        post_date_parent = soup.select('em.fa-calendar')[0].find_parent('tr')
        if(len(post_date_parent.select('p'))> 1):
            post_date = post_date_parent.select('p')[1].get_text(strip = True)
    # print('post_date >>>', post_date)
    company_description = ''
    company_size = ''
    company_logo = ''
    language = ''
    if(len(company_link)>0):
        # print('company_link', company_link)    
        browser.get(company_link)
        company_soup = BeautifulSoup(browser.page_source, features="html.parser")
        if(len(company_soup.select('div.main-about-us'))>0):
            company_description = getTextFromList(company_soup.select('div.main-about-us')[0].select('div.row'))
        if(len(company_soup.select('img'))>0):
            company_logo = company_soup.select('img')[0]['src']
    # print('company_description >>> ', company_description)
    # print('company_size >>>', company_size) 
    # print('Company logo >>>', company_logo)
    print('API >>>>>> ' + title)
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


def getJobInfo(job_link, browser):
    # job_link = "https://careerbuilder.vn/vi/tim-viec-lam/lap-trinh-vien-nodejs.35BA7F1C.html"
    # job_link = "https://careerbuilder.vn/vi/tim-viec-lam/lap-trinh-vien-php.35BA69A9.html"
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    if(len(soup.select('div.full-content'))>0):
        getAlternativeJobInfo(job_link, browser)
        return
    title = ''
    company_name = ''
    company_link = ''
    if(len(soup.select('div.job-desc'))>0):
        job_desc = soup.select('div.job-desc')[0]
        if len(job_desc.select('h1.title')) > 0:
            title = job_desc.select('h1.title')[0].get_text(strip = True)
        if len(job_desc.select('a.employer')[0]) > 0:
            company_name = job_desc.select('a.employer')[0].get_text(strip = True)
            company_link = job_desc.select('a.employer')[0]['href']
    # print('Title >>>>>> ' + title)
    if(len(title) < 1):
        return
    # print('company_name >>>>>> ' + company_name)
    description = ''
    requirement = ''
    benefits = ''
    location = ''
    
    if len(soup.select('div.detail-row')) > 0:
        for index, content in enumerate(soup.select('div.detail-row')):
            for content_title in content.select('h2'):
                if content_title.get_text(strip = True) == 'Mô tả Công việc':
                    description = getTextFromList(content.select('p'))
                if content_title.get_text(strip = True) == 'Yêu Cầu Công Việc':
                    requirement = getTextFromList(content.select('p'))

    if len(soup.select('div.map')) > 0:
        location_list = soup.select('div.map')[0].select('p')
        if(len(location_list)>0):
            location = location_list[0].get_text(strip = True)
    # print('Description >>>> ', description)
    # print('requirement >>>> ', requirement)
    # print('benefits >>>> ', benefits)
    # print('location >>> ', location)

    salary = ''
    deadline = ''
    post_date = ''
    details_box = soup.select('div.detail-box')
    if(len(details_box)>0):
        for _details in details_box:
            details_title_list = _details.select('strong')
            for details_title in details_title_list:
                if(details_title.get_text(strip = True) == 'Lương'):
                    salary_parent = details_title.parent()
                    salary = salary_parent[2].get_text(strip = True)
                if(details_title.get_text(strip = True) == 'Ngày cập nhật'):
                    deadline_parent = details_title.parent()
                    deadline = deadline_parent[2].get_text(strip = True)
                if(details_title.get_text(strip = True) == 'Hết hạn nộp'):
                    post_date_parent = details_title.parent()
                    post_date = post_date_parent[2].get_text(strip = True)

    # print('post_date >>>', post_date)
    # print('Deadline >>>', deadline) 
    # print('SALARY >>> ' + salary) 

    company_description = ''
    company_size = ''
    company_logo = ''
    language = ''
    if(len(company_link)>0):
        # print('company_link', company_link)    
        browser.get(company_link)
        company_soup = BeautifulSoup(browser.page_source, features="html.parser")
        if(len(company_soup.select('div.main-about-us'))>0):
            company_description = getTextFromList(company_soup.select('div.main-about-us')[0].select('div.row'))
        if(len(company_soup.select('img'))>0):
            company_logo = company_soup.select('img')[0]['src']
    # print('company_description >>> ', company_description)
    # print('company_size >>>', company_size) 
    # print('Company logo >>>', company_logo)
    # print('API >>>>>> ' + title)
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

def searchPages(browser, i, search_term):
    page = str(i)
    print('page', page)
    link = 'https://careerbuilder.vn/viec-lam/'
    URL = link + search_term + '-k-trang-' + page + '-vi.html'
    print('URL', URL)
    browser.get(URL)
    page_soup = BeautifulSoup(browser.page_source, features="html.parser")

    if(len(page_soup.select('div.job-item ')) > 0):
        job_elements = page_soup.select('div.job-item ')
        for job_element in job_elements:
            job_link = job_element.select('a.job_link')[0]['href']
            print('job_link', job_link)
            getJobInfo(job_link, browser)
            time.sleep(1)


def getJobList(browser, search_term):
    print('search_term', search_term)
    link = 'https://careerbuilder.vn/viec-lam/'
    URL = link + search_term + '-k-vi.html'
    print('URL', URL)
    # https://careerbuilder.vn/viec-lam/Kỹ-sư-an-ninh-thông-tin-k-vi.html
    browser.get(URL)

    soup = BeautifulSoup(browser.page_source, features="html.parser")

    if(len(soup.select('div.job-item ')) > 0):
        job_elements = soup.select('div.job-item ')
        for job_element in job_elements:
            if(len(job_element.select('a.job_link'))>0):
                job_link = job_element.select('a.job_link')[0]['href']
                print('job_link', job_link)
                getJobInfo(job_link, browser)
                time.sleep(1)

    if(len(soup.select('div.pagination'))>0):
        pages = len(soup.select('div.pagination')[0].select('li')) -1
        if(pages > 1):
            for i in range(2, pages):
                searchPages(browser, i , search_term)

def run(browser, search_terms_list):
    for search_term in search_terms_list:
        try:
            getJobList(browser, search_term.replace("+","").replace(" ", "-").replace("/", ""))
            time.sleep(1)
        finally:
            time.sleep(3)
    
    