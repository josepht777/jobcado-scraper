from bs4 import BeautifulSoup
import time
import api
link = 'https://timviec365.vn'

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


def getJobInfo(job_link, browser):
    job_link = "https://timviec365.vn/nam-ngu-lai-trong-coi-salon-oto-p130186.html"
    print('job_link', job_link)
    browser.get(job_link)
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    
    title = ''
    if len(soup.select('h1.title')) > 0:
        title = soup.select('h1.title')[0].get_text(strip = True)
    print('title', title)
    description = ''
    requirement = ''
    salary = ''
    deadline = ''
    language = ''
    post_date = ''
    location = ''
    benefits = ''

    # for detailsTitle in detailsTitles:
    #     if(detailsTitle.text.strip() == 'Mô tả công việc'):
    #         job_description_parent = detailsTitle.parent()

    # box_mota / hd_mota
    if(len(soup.select('div.box_mota')) >0):
        description = getTextFromList(soup.select('div.box_mota')[0])
    print('description', description)
    if(len(soup.select('div.box_yeucau')) >0):
        requirement = getTextFromList(soup.select('div.box_yeucau')[0])
    print('requirement', requirement)
    if(len(soup.select('div.box_quyenloi')) >0):
        benefits = getTextFromList(soup.select('div.box_quyenloi')[0])
    print('benefits', benefits)

    # p.dd_tuyen
    # Tỉnh thành tuyển dụng: = location
    # Mức lương = salary
    # Hạn nộp hồ sơ: = deadline

    # div.right_tit > p
    if(len(soup.select('div.right_tit'))>0):
        info_soup = soup.select('div.right_tit')[0]
    if(len(info_soup.select('p'))>0):
        for i in info_soup.select('p'):
            if 'Tỉnh thành tuyển dụng' in i.text.strip():
                if(len(i.select('a'))>0):
                    location = i.select('a')[0].text.strip()
                if(len(i.select('span'))>0):
                    location = i.select('span')[0].text.strip()

            if 'Quận huyện tuyển dụng' in i.text.strip():
                if(len(i.select('a'))>0):
                    location = location + '\b ' + i.select('a')[0].text.strip()
                if(len(i.select('span'))>0):
                    location = location + '\b ' + i.select('span')[0].text.strip()

            if 'Mức lương' in i.text.strip():
                if(len(i.select('a'))>0):
                    salary = i.select('a')[0].text.strip()
                if(len(i.select('span'))>0):
                    salary = i.select('span')[0].text.strip()

            if 'Hạn nộp hồ sơ' in i.text.strip():
                if(len(i.select('a'))>0):
                    deadline = i.select('a')[0].text.strip()
                if(len(i.select('span'))>0):
                    deadline = i.select('span')[0].text.strip()
    print("location, salary deadline", location, salary, deadline)

    # Ngày cập nhật: post date / span.date_update
    if(len(soup.select('span.date_update'))>0):
        post_date = getTextFromList(soup.select('span.date_update')[0])
    print('post_date', post_date)
    # company
    # a.class="ct_com"
    # a.na_cty
    company_link = ''

    company_name = ''
    company_description = ''
    company_size = ''
    company_logo = ''
    if(len(soup.select('a.ct_com', href=True))>0):
        company_link = soup.select('a.ct_com', href=True)[0]['href']
    # https://timviec365.vn/tnhh-tmdv-thien-bao-an-co37697
        browser.get(company_link)
        print('company_link', company_link)
        company_soup = BeautifulSoup(browser.page_source, features="html.parser")
        # company_name = div.name_cty
        if(len(company_soup.select('div.name_cty'))>0):
            if(len(company_soup.select('div.name_cty')[0].select('a'))>0):
                company_name = getTextFromList(company_soup.select('div.name_cty')[0].select('a')[0])
        print('company_name', company_name)        
        # div.text_ntd_2
        # company_size = Quy mô:
        # company_location = Địa chỉ:
        company_size_title = company_soup.find_all('strong', text = 'Quy mô:')
        if(len(company_size_title) > 0):
            company_size = getTextFromList(company_size_title[0].parent())
        print('company_size', company_size)
        # company_description = div.left_com
        if(len(company_soup.select('div.left_com'))>0):
            company_description = getTextFromList(company_soup.select('div.left_com')[0])
        print('company_description', company_description)
        if len(company_soup.select('img')) > 0:
            company_logo = company_soup.select('img')[0]['src']
        print('company_logo', company_logo)        
    # div.right_tit
    # div.dd_tuyen

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
    print('URL', URL)
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    job_elements = soup.select('div.item_cate')
    for job_element in job_elements:
        if len(job_element.find_all("a", class_="title_cate", href=True)) > 0:
            job_link = job_element.find_all("a", class_="title_cate", href=True)[0]
            job_link = link + job_link['href']
            getJobInfo(job_link, browser)
            time.sleep(2)
    
    
def run(browser, search_terms_list):
    # https://timviec365.vn/tin-tuyen-dung-viec-lam.html?page=297
    URL_List = []
    for page in range(1, 297):
        URL_List.append(link + '/tin-tuyen-dung-viec-lam.html?page=' + str(page))

    for URL in URL_List:
        try:
            getJobList(URL, browser)
        finally:
            time.sleep(3)