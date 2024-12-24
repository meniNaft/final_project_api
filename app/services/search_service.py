from flask import jsonify

import app.db.elastic.repositories.elastic_repository as elastic_repo
import app.services.map_service as map_service


def search_keywords(query, limit: int = None):
    res = elastic_repo.search_keywords(query, limit)
    res = [elem['_source'] for elem in res]
    if res:
        return map_service.get_map(
            area_data=res,
            area_type="",
            zoom_level="region",
            callback=map_service.add_text_search_markers_to_map
        )
    else:
        return jsonify({"message": "no data found"})


def search_news(query, limit: int = None):
    res = elastic_repo.search_news(query, limit)
    res = [elem['_source'] for elem in res]
    if res:
        return map_service.get_map(
            area_data=res,
            area_type="",
            zoom_level="region",
            callback=map_service.add_text_search_markers_to_map
        )
    else:
        return jsonify({"message": "no data found"})


def search_historic(query, limit: int = None):
    res = elastic_repo.search_historic(query, limit)
    res = [elem['_source'] for elem in res]
    if res:
        return map_service.get_map(
            area_data=res,
            area_type="",
            zoom_level="region",
            callback=map_service.add_text_search_markers_to_map
        )
    else:
        return jsonify({"message": "no data found"})


def search_combined(query, start_date, end_date, limit: int = None):
    res = elastic_repo.search_combined(query, start_date, end_date, limit)
    res = [elem['_source'] for elem in res]
    if res:
        return map_service.get_map(
            area_data=res,
            area_type="",
            zoom_level="region",
            callback=map_service.add_text_search_markers_to_map
        )
    else:
        return jsonify({"message": "no data found"})

