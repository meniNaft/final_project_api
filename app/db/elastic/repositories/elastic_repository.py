from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
index_name = "terror_attack_data"


def search_keywords(query: str, limit: int = None):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["body", "title"]
            }
        }
    }
    if limit is not None:
        body["size"] = limit

    response = es.search(index=index_name, body=body)
    return response['hits']['hits']


def search_news(query: str, limit: int = None):
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
    if limit is not None:
        body["size"] = limit

    response = es.search(index=index_name, body=body)
    return response['hits']['hits']


def search_historic(query: str, limit: int = None):
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
    if limit is not None:
        body["size"] = limit

    response = es.search(index=index_name, body=body)
    return response['hits']['hits']


def search_combined(query: str, start_date: str, end_date: str, limit: int = None):
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
    if limit is not None:
        body["size"] = limit

    response = es.search(index=index_name, body=body)
    return response['hits']['hits']
