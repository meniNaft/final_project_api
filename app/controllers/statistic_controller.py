from flask import Blueprint, jsonify
import app.services.statistic_service as statistic_service

statistics_blueprint = Blueprint('statistics', __name__)


@statistics_blueprint.route('/deadliest-attack-types/<filter_top5>', methods=['GET'])
def get_deadliest_attack_types(filter_top5: str):
    try:
        only_top5 = filter_top5.lower() in ['y', 'yes', 'true']
        res = statistic_service.get_deadliest_attack_types(only_top5=True if only_top5 else False)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": e}), 500


@statistics_blueprint.route('/avg-casualties-per-area/<area_type>/<filter_top5>', methods=['GET'])
def get_avg_casualties_per_area(area_type, filter_top5: str):
    try:
        only_top5 = filter_top5.lower() in ['y', 'yes', 'true']
        res = statistic_service.get_avg_casualties_per_area(area_type=area_type, only_top5=True if only_top5 else False)
        return res
    except Exception as e:
        return jsonify({"error": e}), 500


@statistics_blueprint.route('/top-terror-groups-by-casualties', methods=['GET'])
def get_top_terror_groups_by_casualties():
    try:
        res = statistic_service.get_top_terror_groups_by_casualties()
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": e}), 500


@statistics_blueprint.route('/attack-percentage-change-by-year/<area_type>/<area_id>', methods=['GET'])
def attack_percentage_change_by_year(area_type: str, area_id: int):
    try:
        res = statistic_service.attack_percentage_change_by_year(area_type, area_id)
        return res
    except Exception as e:
        return jsonify({"error": e}), 500


@statistics_blueprint.route('/most-active-terror-group/<area_type>/<area_id>', methods=['GET'])
def most_active_terror_group(area_type: str, area_id: int):
    try:
        res = statistic_service.most_active_terror_group_map(area_type, area_id)
        return res
    except Exception as e:
        return jsonify({"error": e}), 500
