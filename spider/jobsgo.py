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
    
    if len(soup.select('div.content-group')) > 0:
        for index, content in enumerate(soup.select('div.content-group')):
            for contentTitle in content.select('h5'):
                if contentTitle.get_text(strip = True) == 'Mô tả công việc':
                    description = getTextFromList(content.select('div.clearfix'))
                if contentTitle.get_text(strip = True) == 'Yêu cầu công việc':
                    requirement = getTextFromList(content.select('div.clearfix'))
                if contentTitle.get_text(strip = True) == 'Quyền lợi được hưởng':
                    benefits = getTextFromList(content.select('div.clearfix'))
                if contentTitle.get_text(strip = True) == 'Địa điểm làm việc':
                    location = getTextFromList(content.select('div.margin-top-10'))

    # print('Description >>>> ', description)
    # print('requirement >>>> ', requirement)
    # print('benefits >>>> ', benefits)
    # print('location >>> ', location)

    salary = ''
    deadline = ''
    company_name = ''
    company_description = ''
    company_size = ''
    company_logo = ''
    language = ''
    post_date = ''

    if len(soup.select('div.company-info')) > 0:
        for index, content in enumerate(soup.select('div.company-info')[0]):
            if(content):
                if('nhân viên' in content.get_text(strip = True)):
                    company_size = content.get_text(strip = True)
                # if(content.find('i')):
                #     if(content.find('i') != -1):
                #         print(content.find('i').get('class'))
                
    # print('company_description >>> ', company_description)
    # print('post_date >>>', post_date, language)
    # print('company_size >>>', company_size) # nhân viên / glyphicon glyphicon-user

    if(len(soup.find('i', class_='glyphicon glyphicon-usd').parent()) > 0):
        for item in soup.find('i', class_='glyphicon glyphicon-usd').parent():
            salary = salary + "\b " + item.get_text(strip = True)

    if(len(soup.find('i', class_='glyphicon glyphicon-time').parent()) > 0):
        for item in soup.find('i', class_='glyphicon glyphicon-time').parent():
            deadline = deadline  + "\b " + item.get_text(strip = True)

    # print('Deadline >>>', deadline) # glyphicon glyphicon-time
    # print('SALARY >>> ' + salary) # glyphicon glyphicon-usd or Mức lương

    if(soup.select('div.profile-cover')):
        if(len(soup.select('div.profile-cover')) > 0):
            company_name = soup.select('div.profile-cover')[0].find_all('img')[0]['alt']
            # print('Company name >>> ', company_name)
            if(soup.find_all('img', alt=company_name)):
                if(len(soup.find_all('img', alt=company_name)) > 0):
                    if(soup.find_all('img', alt=company_name)[0]):
                        company_logo = soup.find_all('img', alt=company_name)[0].get('data-src') or soup.find_all('img', alt=company_name)[0].get('src')
    # print('Company logo >>>', company_logo)
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
    return

def getJobList(browser, URL):
    browser.get(URL)
    try:
        soup = BeautifulSoup(browser.page_source, features="html.parser")
    except Exception as e:
        print('Error @ 125: ', e.message)
        return

    if(len(soup.select('div.item-click  ')) > 0):
        job_elements = soup.select('div.item-click  ')
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     args = ((browser, b.select('a')[0]['href']) for b in job_elements)
        #     executor.map(lambda p: getJobInfo(*p), args)

        for job_element in job_elements:
            job_link = job_element.select('a')[0]['href']
            print('link', job_link)
            getJobInfo(browser, job_link)
            time.sleep(1)

    # pagination_List = []
    # if(len(soup.select('li.next')) > 0):
    #     if(len(soup.select('li.next')[0].select('span'))>0):
    #         if(len(soup.select('li.next disabled')) == 0):
    #             for i in range(2, 481):
    #                 pagination_List.append("https://jobsgo.vn/viec-lam-trang-" + str(i) +".html?view=ajax")
            # print(soup.select('li.next')[0].select('span')[0])
            # print(soup.select('li.next disabled'))
            # print(soup.select('li.next'))
            # data-href="/viec-lam-trang-2.html?view=ajax"
            # soup.select('li.next')[0].select('span')[0].click()

def run(browser, search_terms_list):
    URL_List = []
    link = 'https://jobsgo.vn/viec-lam-'

    for search_term in search_terms_list:
            URL_List.append(link + search_term.replace("+","").replace(" ", "-").replace("/", "") + '.html')
    URL_List.append("https://jobsgo.vn/viec-lam.html")

    for i in range(2, 481):
        URL_List.append("https://jobsgo.vn/viec-lam-trang-" + str(i) +".html?view=ajax")
    try:
        # URL_List.reverse()

        # Multi-Threading
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     args = ((browser, b) for b in URL_List)
        #     executor.map(lambda p: getJobList(*p), args)

        # Single Thread
        # for URL in URL_List:
        #     getJobList(browser, URL)

        # Multi-Threading testing
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            the_futures = [executor.submit(lambda p: getJobList(*p), (browser, URL)) for URL in URL_List]
        for future in the_futures:
            try:
                result = future.result() # could throw an exception if the thread threw an exception
                print(result)
            except Exception as e:
                print('Thread threw exception:', e)

    finally:
        time.sleep(3)
    # browser.quit()
    # print('finish jobsgo')

        # executor = concurrent.futures.ProcessPoolExecutor(max_workers=5)
        # executor = concurrent.futures.ThreadPoolExecutor()
        # futures = [executor.submit(t) for t in tasks]
        # for f in concurrent.futures.as_completed(futures):
        #     if f.result():
        #         break
        # print('Move on...')