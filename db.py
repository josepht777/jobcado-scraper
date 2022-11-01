import psycopg2
from psycopg2 import Error
from unidecode import unidecode

def normalize_str( text: str ) -> str:
    """"""
    if text:
        return unidecode( text.strip() ).lower()

    return text

def insert(
    title: str,
    link: str,
    description: str,
    category: str,
    requirement: str,
    company_name: str,
    company_description: str,
    location: str,
    company_size: str,
    company_logo: str,
    salary: str,
    benefits: str,
    post_date: str,
    deadline: str,
    language: str,
    weight: int = 0,
):
    """"""
    try:
        # Connect to an existing database
        conn = psycopg2.connect(
                    user="jcuser",
                    password="string",
                    host="localhost",
                    port="5432",
                    database="jc"
                )
        with conn:
            # Create a cursor to perform database operations
            with conn.cursor() as cursor:
                # BEGIN is executed, a transaction is started

                # Insert into 'jobs' table sql string.
                sql = """
                    INSERT INTO "jobs"(
                        title,
                        title_una,
                        link,
                        description,
                        description_una,
                        category,
                        category_una,
                        requirement,
                        requirement_una,
                        company_name,
                        company_name_una,
                        company_description,
                        company_description_una,
                        location,
                        location_una,
                        company_size,
                        company_logo,
                        salary,
                        salary_una,
                        benefits,
                        benefits_una,
                        post_date,
                        deadline,
                        language,
                        language_una,
                        weight
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
                        %s,
                        %s,
                        %s,
                        %s
                    );
                """
                # data holds values to insert.
                data = (
                    title.strip(),
                    normalize_str( title ),
                    link.strip(),
                    description.strip(),
                    normalize_str( description ),
                    category.strip(),
                    normalize_str( category ),
                    requirement.strip(),
                    normalize_str( requirement ),
                    company_name.strip(),
                    normalize_str( company_name ),
                    company_description.strip(),
                    normalize_str( company_description ),
                    location.strip(),
                    normalize_str( location ),
                    company_size.strip(),
                    company_logo.strip(),
                    salary.strip(),
                    normalize_str( salary ),
                    benefits.strip(),
                    normalize_str( benefits ),
                    post_date.strip(),
                    deadline.strip(),
                    language.strip(),
                    normalize_str( language ),
                    weight,
                )
                
                cursor.execute(sql, data)
            # End of with(cursor)  
        # End of with(conn) transaction COMMIT/ROLLBACK(exception)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # Close the connection.
        conn.close()

    print("PostgreSQL connection is closed")