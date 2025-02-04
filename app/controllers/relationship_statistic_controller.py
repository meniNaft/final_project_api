from flask import Blueprint, jsonify
import app.services.relationship_statistic_service as relationship_statistic_service

relation_statistics_blueprint = Blueprint('statistics/relationship', __name__)


@relation_statistics_blueprint.route('/shared-targets/<area_type>', methods=['GET'])
def get_shared_targets(area_type: str):
    try:
        return relationship_statistic_service.get_shared_targets(area_type)
    except Exception as e:
        return jsonify({"error": e}), 500


@relation_statistics_blueprint.route('/cooperating-groups', methods=['GET'])
def get_cooperating_groups():
    try:
        return relationship_statistic_service.get_cooperating_groups()
    except Exception as e:
        return jsonify({"error": e}), 500


@relation_statistics_blueprint.route('/shared-attack-types/<area_type>', methods=['GET'])
def get_shared_attack_types(area_type: str):
    try:
        return relationship_statistic_service.get_shared_attack_types(area_type)
    except Exception as e:
        return jsonify({"error": e}), 500


@relation_statistics_blueprint.route('/top-group-city/<area_type>', methods=['GET'])
def get_top_group_city_by_area(area_type: str):
    try:
        return relationship_statistic_service.top_group_city_by_area(area_type)
    except Exception as e:
        return jsonify({"error": e}), 500


@relation_statistics_blueprint.route('/groups-attacked-same-target-same-year/', methods=['GET'])
def get_groups_attacked_same_target_same_year():
    try:
        return relationship_statistic_service.get_groups_attacked_same_target_same_year()
    except Exception as e:
        return jsonify({"error": e}), 500
