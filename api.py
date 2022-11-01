import requests
from requests.structures import CaseInsensitiveDict

def login():
    url = 'https://api.jobcado.com/user/login'
    data = {
        "email": "string",
        "password": "string"
    }
    
    response = requests.post(url, json = data)
        
    if (response.status_code == 201):
        data = response.json()

        return data['token']
    
    return ''
    
def insert(
    title,
    link,
    description,
    category,
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
):
    token = login()

    headers = CaseInsensitiveDict()

    headers['Authorization'] = "Bearer " + token

    data = {
        "title": title,
        "link": link,
        "deadline": deadline,
        "description": description,
        "category": category,
        "requirement": requirement,
        "company_name": company_name,
        "company_description": company_description,
        "location": location,
        "company_size": company_size,
        "company_logo": company_logo,
        "salary": salary,
        "post_date": post_date,
        "language": language,
        "benefits": benefits,
        "weight": weight,
    }

    url = 'https://api.jobcado.com/job/add'
    # print('DATA >>> ',data)
    response = requests.post(url, json = data, headers = headers)
    
    print(response.status_code)
    
    if response.status_code == 200:
        print("OK")
    elif response.status_code == 409:
        print("Link is taken")
    else:
        print("FAILED")