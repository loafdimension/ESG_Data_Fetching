# ESG Data Fetching

## How I accessed WikiRate's data
I created an account with WikiRate, generated an API key, and then read on the WikiRates API page that they had provided a link to an API wrapper called "WikiRate4py". I didn't know much about API wrappers so I looked in to what it does and read through the WikiRate4py documentation. I then saw that it really simplifies interactions with an API, as it handles request URLs, query parameters, HTTP headers, has built in error handling features, and allows you to combine several API calls in to a single function. This sounded great, so I installed WikiRate4py and used that to access WikiRate's data.

## The Chosen Metrics
1 - Total energy consumption, GRI 302-1-e (formerly G4-EN3-e)  

2 - Direct greenhouse gas (GHG) emissions (Scope 1), GRI 305-1-a (formerly G4-EN15-a)  

3 - Incidents of discrimination, GRI 406-1 (G4-HR3-a)

## Data Quality Issues
- Excludes companies with partial reporting of data as they would not have met the requirements of having a "known" status.  
- Some records reference source documents that aren't accessible via the API, which results in missing or incomplete source metadata.

## Assumptions or trade-offs
Assumptions 
- The "get_company_ids__in_all_metrics" function currently assumes that with a limit of 100 (or whatever it is set to), it will find at least 10 companies that have a known status across the specified metrics.
- All sources are equally trustworthy, there is no distinguishment between audits, and self reported data.

Trade off - Simplicity over performance
- The code is readable but isn't very efficient as it makes API calls inside nested loops which is computationally heavy.
- It can survive here but it wouldn't scale very well.

## What I would improve with more time
Code optimisation 
- Cache metric and company objects instead of repeatedly fetching them.
- Batch API calls to reduce latency and API load.

Filtering
- Refactor so the records that come back in the dataset can be by year, or a variety of other options.
- Refactor the function so it can return companies based on highest or lowest answers, and more filtering options.

Use of "limit" in "get_company_ids__in_all_metrics"
- Find a different way to return the specified number of companies rather than guessing a limit that should have a crossover of the desired amount, and then fetching data for way more than I actually need.

Schema validation
- To ensure that every dataset record is consistent and to prevent inconsistent entries from entering the dataset and then potentially causing issues for systems that use it.


