from flask import Blueprint, jsonify
import app.services.statistic_service as statistic_service

statistics_blueprint = Blueprint('statistics/relationship', __name__)


@statistics_blueprint.route('/shared-targets/<area_type>', methods=['GET'])
def get_shared_targets(area_type):
    try:
        res = statistic_service.get_avg_casualties_per_area(area_type=area_type, only_top5=True if only_top5 else False)
        return res
    except Exception as e:
        return jsonify({"error": e}), 500
