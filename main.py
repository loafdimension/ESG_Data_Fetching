from dotenv import load_dotenv
import os
import wikirate4py

load_dotenv()
api_key = os.getenv("WIKIRATE_API_KEY")
api = wikirate4py.API(api_key)

# my chosen metrics 
# 1 - Total energy consumption
# 2 - Direct greenhouse gas emissions
# 3 - Incidents of discrimination

def get_companies_all_metrics(identifier1, identifier2, identifier3, limit):
    metric_one_company_names = []
    metric_two_company_names = []
    metric_three_company_names = []

    metric_one_company_data = api.get_answers(identifier=identifier1, limit=limit, status="known")
    metric_two_company_data = api.get_answers(identifier=identifier2, limit=limit, status="known")
    metric_three_company_data = api.get_answers(identifier=identifier3, limit=limit, status="known")


    for metric_one_company in metric_one_company_data:
        metric_one_company_names.append(metric_one_company.company)

    for metric_two_company in metric_two_company_data:
        metric_two_company_names.append(metric_two_company.company)

    for metric_three_company in metric_three_company_data:
        metric_three_company_names.append(metric_three_company.company)

    company_IDs_in_all_metrics = list(set(metric_one_company_names) & set(metric_two_company_names) & set(metric_three_company_names))
          
    return company_IDs_in_all_metrics[:10]

all_companies = get_companies_all_metrics(846580, 826615, 836314, 100)
#print(all_companies)
#print(len(all_companies))

# TEST COMPANY IS EQUINOR
# INPUT
# question
metric = api.get_metric(identifier=846580)
print("Question: ", metric.question)

# custom id
print("Custom_id: ", metric.name)

# data type
print("Data_type: ", metric.value_type)

# company 
company = api.get_company(5760335)
print("Company: ", company.name)

# file metas / source documents api request
answers = api.get_answers(identifier=846580, company=5760335, limit=100, status="known")
source = api.get_source(identifier="Source-000206657")

# answer value and year

for answer in answers:
    value = answer.value
    year = answer.year
    print("Answer: ", value)
    print("Year: ", year)

# file name, file url, and page number 
    sources = answer.sources
    for source_id in sources:
        try:
            source = api.get_source(identifier=source_id)
            file_name = source.title
            file_url = source.file_url
            print("File Name: ", file_name)
            print("File URL: ", file_url)
        except wikirate4py.exceptions.NotFoundException:
            print(f"Source {source_id} could not be found")

