import psycopg2
from psycopg2 import Error
from googletrans import Translator


def translate(text):
    if text == '':
        return ''
    
    translator = Translator()
    return str(translator.translate(text, src='vi', dest='en').text)

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
    language
):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="jcuser",
                                    password="string",
                                    host="localhost",
                                    port="5432",
                                    database="jc")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        
        sql = """
            INSERT INTO "job"(
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
                title_en,
                description_en,
                category_en,
                requirement_en,
                company_name_en,
                company_description_en,
                location_en,
                salary_en,
                language_en
            )
	        VALUES (
                %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
                %s,
                %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
	            %s,
                %s
            );
        """
        
        data = (
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
            translate(title),
            translate(description),
            translate(category),
            translate(requirement),
            translate(company_name),
            translate(company_description),
            translate(location),
            translate(salary),
            translate(language)
        )
        
        cursor.execute(sql, data)
        connection.commit()
        
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
