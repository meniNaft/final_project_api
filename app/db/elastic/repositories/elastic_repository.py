from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
index_name = "terror_attack_data"


def search_keywords(query: str):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["body", "title"]
            }
        }
    }
    response = es.search(index=index_name, body=body)
    return response['hits']['hits']


def search_news(query: str):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {"query": query, "fields": ["body", "title"]}},
                    {"term": {"category": "news"}}
                ]
            }
        }
    }
    response = es.search(index=index_name, body=body)
    return response['hits']['hits']


def search_historic(query: str):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {"query": query, "fields": ["body", "title"]}},
                    {"term": {"category": "history"}}
                ]
            }
        }
    }
    response = es.search(index=index_name, body=body)
    return response['hits']['hits']


def search_combined(query: str, start_date: str, end_date: str):
    must_clauses = [
        {"multi_match": {"query": query, "fields": ["body", "title"]}},
        {
            "range": {
                "date": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        }
    ]

    body = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }
    response = es.search(index=index_name, body=body)
    return response['hits']['hits']
