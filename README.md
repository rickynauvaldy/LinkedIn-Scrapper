# LinkedIn Scrapper
 Placement Test for Academi by blank-space.io Data Enginering Track

## Concept
Pulling data from LinkedIn as the job recruitment platform using a scraping method and store the requested data feature to our data warehouse.

## Keywords for search tag
-	Senior Data Engineer / Data Engineer
-	Senior Data Scientist / Data Scientist
-	Senior Data Analyst / Data Analyst
-	Senior Business Intelligence / Business Intelligence Analyst

## Features
1.	Company Name
2.	Job Posting Time (23 hours ago, 1 minute ago, etc)
3.	Number of applicants
4.	Seniority level  (Entry level/Associate/Mid-senior level)
5.	Size of employee
6.	Company industry
7.	Detail description (job desc, job req, benefit, etc)
8.	Employment type
9.	Job Function

## Limitation
- Tested only when LinkedIn is not logged in
- Didn't include "Company Size" as it's only available when logging in
- Indonesia only location
- "Show more" in description is ignored
- Data is stored as CSV, not stored in data warehouse

## Usage
- open main.py and store keywords in the "keywords" variable in list (in this example: 'Senior Data Engineer', 'Data Engineer', 'Senior Data Scientist', 'Data Scientist', 'Senior Data Analyst',
'Data Analyst', 'Senior Business Intelligence', 'Business Intelligence Analyst')
- run main.py by executing "python main.py"
- notebook_scrap.ipynb is available for exploring scrapping process in Jupyter Notebook
- notebook_explore.ipynb is available for exploring scrapped data in Jupyter Notebook

## Implications on Exploration
Based on data scrapped in 8th of April 2021,
- Most job scrapped are posted around 1-2 week
- Data Analyst keyword has the most scrapped job post, followed by Data Engineer
- Most job scrapped are looking for Associate and Entry Level Seniority
- Most job scrapped are applied less than 50 applicants

## Author note
- Adopted from https://amandeepsaluja.com/extracting-job-information-from-linkedin-jobs-using-beautifulsoup-and-selenium/