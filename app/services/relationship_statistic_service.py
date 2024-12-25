from flask import jsonify

import app.db.neo4j.repositories.neo4j_repository as neo4j_repo
import app.services.map_service as map_service


def get_shared_targets(area_type: str = ''):
    if area_type not in ['city', 'state', 'country', 'region']:
        area_type = 'city'
    res = neo4j_repo.get_shared_targets(area_type)
    if res:
        print(res)
        return map_service.get_map(
            area_data=res,
            area_type=area_type,
            zoom_level="region",
            callback=map_service.add_area_terror_group_markers_to_map
        )
    else:
        return jsonify({"message": "no data found"})


def get_cooperating_groups():
    return neo4j_repo.get_cooperating_groups()


def get_shared_attack_types(area_type: str = ''):
    if area_type not in ['city', 'state', 'country', 'region']:
        area_type = 'city'
    res = neo4j_repo.get_shared_attack_types(area_type)
    if res:
        print(res)
        return map_service.get_map(
            area_data=res,
            area_type=area_type,
            zoom_level="region",
            callback=map_service.add_attack_type_terror_group_markers_to_map
        )
    else:
        return jsonify({"message": "no data found"})


def top_group_city_by_area(area_type: str = ''):
    if area_type not in ['state', 'country', 'region']:
        area_type = 'state'
    res = neo4j_repo.top_group_city_by_area(area_type)
    if res:
        print(res)
        return map_service.get_map(
            area_data=res,
            area_type=area_type,
            zoom_level="region",
            callback=map_service.add_top_group_city_by_area_markers_to_map
        )
    else:
        return jsonify({"message": "no data found"})


def get_groups_attacked_same_target_same_year():
    return neo4j_repo.get_groups_attacked_same_target_same_year()
