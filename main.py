"""
# Target:	DE Candidate
<br><br>Test Concept:	You are asked to pull data from the job recruitment platform, which is linkedin using a scraping method and store the requested data feature to our data warehouse.
<br><br>In this case, we want to know about all information about hiring opportunities related to data field position, Use this keyword search tag:
-	Senior Data Engineer / Data Engineer
-	Senior Data Scientist / Data Scientist
-	Senior Data Analyst / Data Analyst
-	Senior Business Intelligence / Business Intelligence Analyst
<br><br>So, here is a detail of data feature that we want:
1.	Company Name
2.	Job Posting Time (23 hours ago, 1 minute ago, etc)
3.	Number of applicants
4.	Seniority level  (Entry level/Associate/Mid-senior level)
5.	Size of employee
6.	Company industry
7.	Detail description (job desc, job req, benefit, etc)
8.	Employment type
9.	Job Function

<br><br>Store all information into your own Data Warehouse for “Detail Description” you can store into Google Cloud Storage. You also need to visualize/present the result (aggregation, dashboard, etc) that gives meaningful insights
<br><br>Key objectives:	
-	9 features in each job opportunities
<br><br>Tools needed:	
-	Github (Documentation + File Management)
<br><br>Effort (time/duration):	
-	Until 9 April, faster, better.
<br><br>Output:	
-	Github Repository

<br><br>Notes:
-	Make sure that your script runs well before submission, we will try it!
-	Make a proper documentation, especially for flow of scraping.
-	Send Output to academi@blank-space.io cc: jedi@blank-space.io, rahadian@blank-space.io, rahul@blank-space.io 
"""

"""
# Author note
Adopted from https://amandeepsaluja.com/extracting-job-information-from-linkedin-jobs-using-beautifulsoup-and-selenium/
<br><br>Limitation:
- Only available while LinkedIn is not logged in
- Didn't include "Company Size" as it's only available when logging in
- Indonesia only location
- "Show more" in description is ignored
"""

# Install when required
# pip install selenium
# pip install webdriver_manager

# importing packages
import pandas as pd
import re

from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import numpy as np

# replace variables here.
keywords = [
    'Senior Data Engineer',
    'Data Engineer',
    'Senior Data Scientist', 
    'Data Scientist',
    'Senior Data Analyst',
    'Data Analyst',
    'Senior Business Intelligence',
    'Business Intelligence Analyst'
    ]


# Functions
def clean_number_of_applicants(string):
    string_split = string.split()
    clean_number = ''
    if len(string_split) == 6:
        clean_number = '<' + str(string_split[4])
    elif len(string_split) == 3:
        clean_number = '>' + str(string_split[1])
    elif len(string_split) == 2:
        clean_number = str(string_split[0])
    else: clean_number = np.NaN
    return clean_number

# Prepare dataframe for all data
all_data = pd.DataFrame(columns=['Company Name', 'Job Posting Time', 'Number of Applicants',
       'Seniority Level', 'Company Industry', 'Detail description',
       'Employment Type', 'Job Function'])

# Begin processing
for keyword in keywords:
    print("Processing:", keyword)
    # using quote (%20) to make sure it's exactly as it is
    url = "https://www.linkedin.com/jobs/search?keywords=%22"+ urllib.parse.quote(keyword, safe='') +"%22&location=indonesia"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    sleep(3)
    action = ActionChains(driver)

    # scroll down for all available jobs
    no_of_jobs = int(driver.find_element_by_xpath('/html/body/main/div/section[2]/div/h1/span').text)
    linkedin_job_per_page = 20
    for i in range(0, round(no_of_jobs/linkedin_job_per_page)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)

    # parsing the visible webpage
    pageSource = driver.page_source
    lxml_soup = BeautifulSoup(pageSource, 'lxml')

    # searching for all job containers
    job_container = lxml_soup.find('ul', class_ = 'jobs-search__results-list')

    print('You are scraping information about {} jobs.'.format(len(job_container)))
    # somehow not getting all..

    # setting up list for job information
    # Company Name
    company_name = []

    # Job Posting Time (23 hours ago, 1 minute ago, etc)
    post_date = []

    # for loop for job title, company, id, location and date posted
    for job in job_container:

        # company name
        company_names = job.select_one('img')['alt']
        # remove "Graphic"
        company_names = company_names[:-8]
        # Append to list
        company_name.append(company_names)
        
        # Keep this code part if maybe location is needed
        # # job location
        # job_locations = job.find("span", class_="job-result-card__location").text
        # job_location.append(job_locations)
        
        # posting date
        post_dates = job.select_one('time').text
        post_date.append(post_dates)
        
    # Check how many rows do we got
    print("Company Name:", len(company_name), "rows")
    print("Job Posting Time:", len(post_date), "rows")

    # Number of applicants
    applicants = []

    # Seniority level (Entry level/Associate/Mid-senior level)
    level = []

    # Size of employee
    # NA
    # Have to be logged in

    # Company industry
    industries = []

    # Detail description (job desc, job req, benefit, etc)
    job_desc = []

    # Employment type
    emp_type = []

    # Job Function
    functions = []

    # for loop for job description and criterias
    print("Start processing " + keyword + " detail..")
    for x in range(1,len(company_name)+1):
    # for x in range(23,24):
        
        # clicking on different job containers to view information about the job
        job_xpath = '/html/body/main/div/section/ul/li[{}]/img'.format(x)
        driver.find_element_by_xpath(job_xpath).click()
        sleep(1)
        
        # job description
        jobdesc_xpath = '/html/body/main/section/div[2]/section[2]/div'
        job_descs = driver.find_element_by_xpath(jobdesc_xpath).text
        # re-get when there exist "compensation"
        if "Base pay range" in job_descs:
            jobdesc_xpath = '/html/body/main/section/div[2]/section[3]/div'
            job_descs = driver.find_element_by_xpath(jobdesc_xpath).text
        job_desc.append(job_descs)
        
        # Seniority level
        # try-except when there exist "compensation"
        seniority_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[1]'
        try:
            seniority = driver.find_element_by_xpath(seniority_xpath).text.splitlines(0)[1]
        except:
            seniority_xpath = '/html/body/main/section/div[2]/section[3]/ul/li[1]'
            seniority = driver.find_element_by_xpath(seniority_xpath).text.splitlines(0)[1]
        level.append(seniority)
        
        # Employment type
        # try-except when there exist "compensation"
        type_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[2]'
        try:
            employment_type = driver.find_element_by_xpath(type_xpath).text.splitlines(0)[1]
        except:
            type_xpath = '/html/body/main/section/div[2]/section[3]/ul/li[2]'
            employment_type = driver.find_element_by_xpath(type_xpath).text.splitlines(0)[1]
        
        emp_type.append(employment_type)
        
        # Job function
        # try-except when there exist "compensation"
        job_function = ''
        function_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[3]/span'
        if len(driver.find_elements_by_xpath(function_xpath)) != 0:
            for function_elem in driver.find_elements_by_xpath(function_xpath):
                job_function = job_function + ',' + function_elem.text
        else:
            function_xpath = '/html/body/main/section/div[2]/section[3]/ul/li[3]/span'
            for function_elem in driver.find_elements_by_xpath(function_xpath):
                job_function = job_function + ',' + function_elem.text
        
        # remove comma in the front
        job_function = job_function[1:]
        functions.append(job_function)
        
        # Industries
        # try-except when there exist "compensation"
        industry_type = ''
        industry_xpath = '/html/body/main/section/div[2]/section[2]/ul/li[4]/span'
            
        if len(driver.find_elements_by_xpath(industry_xpath)) != 0:
            for industry_elem in driver.find_elements_by_xpath(industry_xpath):
                industry_type = industry_type + ',' + industry_elem.text
            # remove comma in the front
            industry_type = industry_type[1:]
        else:
            industry_xpath = '/html/body/main/section/div[2]/section[3]/ul/li[4]/span'
            if len(driver.find_elements_by_xpath(industry_xpath)) != 0:
                for industry_elem in driver.find_elements_by_xpath(industry_xpath):
                    industry_type = industry_type + ',' + industry_elem.text
                # remove comma in the front
                industry_type = industry_type[1:]
            else:
                # if somehow they don't give the industry type
                industry_type = 'NA'
        industries.append(industry_type)
        
        # applicants
        # try-except when "be early 25 applicants"
        applicant_xpath = '/html/body/main/section/div[2]/section/div/div/h3[2]/span[2]'  
        try:
            applicant = driver.find_element_by_xpath(applicant_xpath).text
        except:
            applicant_xpath = '/html/body/main/section/div[2]/section/div/div/h3[2]/figure'
            applicant = driver.find_element_by_xpath(applicant_xpath).text
        
        applicants.append(applicant)
        if x % 10 == 0:
            print(str(x) + "/" + str(len(company_name)) + " data processed")
        x = x+1

    # to check if we have all information
    print("Applicants:", len(applicants), "rows")
    print("Job Description:", len(job_desc), "rows")
    print("Level:", len(level), "rows")
    print("Employee Type:", len(emp_type), "rows")
    print("Functions:", len(functions), "rows")
    print("Industries:", len(industries), "rows")

    print("Finished")

    # creating a dataframe
    job_data = pd.DataFrame({
        'Company Name': company_name,
        'Job Posting Time': post_date,
        'Number of Applicants': applicants,
        'Seniority Level': level,
        # 'Size of Employee': 'NA',
        'Company Industry': industries,
        'Detail description': job_desc,
        'Employment Type': emp_type,
        'Job Function': functions
    })

    # cleaning description column
    job_data['Detail description'] = job_data['Detail description'].str.replace('\n',' ')

    # hard code size employee
    job_data['Size of Employee'] = np.NaN

    job_data.replace('NA', np.NaN, inplace=True)

    job_data['Number of Applicants'] = job_data['Number of Applicants'].apply(clean_number_of_applicants)
    job_data['Keyword'] = keyword
    job_data.to_csv('LinkedIn Job Data_' + keyword + '.csv', index=0)
    
    all_data = pd.concat([all_data, job_data])

# export all data
all_data.to_csv('LinkedIn Job Data.csv', index=0)

