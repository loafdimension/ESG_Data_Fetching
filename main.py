from dotenv import load_dotenv
import os
import wikirate4py
import json

load_dotenv()
api_key = os.getenv("WIKIRATE_API_KEY")
api = wikirate4py.API(api_key)

metrics = [
    846580, # total energy consumption
    826615, # direct greenhouse gas emissions (scope 1)
    836314 # incidents of discriimination
]

def get_company_ids__in_all_metrics(metrics, limit):
    metric_one_company_names = []
    metric_two_company_names = []
    metric_three_company_names = []

    metric_one_company_data = api.get_answers(identifier=metrics[0], limit=limit, status="known")
    metric_two_company_data = api.get_answers(identifier=metrics[1], limit=limit, status="known")
    metric_three_company_data = api.get_answers(identifier=metrics[2], limit=limit, status="known")


    for metric_one_company in metric_one_company_data:
        metric_one_company_names.append(metric_one_company.company)
        

    for metric_two_company in metric_two_company_data:
        metric_two_company_names.append(metric_two_company.company)

    for metric_three_company in metric_three_company_data:
        metric_three_company_names.append(metric_three_company.company)

    companies_in_all_metrics = list(set(metric_one_company_names) & set(metric_two_company_names) & set(metric_three_company_names))
          
    companies_in_all_metrics = companies_in_all_metrics[:10]

    company_ids = []

    for company in companies_in_all_metrics:
        id = api.get_company(company).id
        company_ids.append(id)

    return company_ids

company_ids_list = get_company_ids__in_all_metrics(metrics, 100)

dataset = []

for metric_id in metrics:
    for company_id in company_ids_list:

        metric = api.get_metric(identifier=metric_id)
        company = api.get_company(company_id)

        answers = api.get_answers(identifier=metric_id, company=company_id, limit=100, status="known")

        for answer in answers:

            source_docs = [] 

            sources = answer.sources
            for source_id in sources:
                try:
                    source = api.get_source(identifier=source_id)
                    source_docs.append({
                        "file_name": source.title,
                        "file_url": source.file_url,
                    })
                    
                except wikirate4py.exceptions.NotFoundException:
                    source_docs.append({
                        "file_name": "None",
                        "file_url": "None",
                        "source_id": source_id
                    })

            record = {
                "input": {
                    "question": metric.question,
                    "custom_id": metric.name,
                    "data_type": metric.value_type,
                    "company": company.name,
                    "file_metas": source_docs
                },
                "reference_output": {
                    "answer": answer.value,
                    "source_documents": source_docs
                },
                "structured_data": {
                    "time_period": answer.year
                }
            }

            dataset.append(record)


with open("dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)
    