from datetime import datetime
from flask import jsonify, Blueprint
import app.services.search_service as search_service # Import the SearchService

search_blueprint = Blueprint('search', __name__)


@search_blueprint.route('/keywords/<string:query>', methods=['GET'])
def search_keywords(query: str):
    result = search_service.search_keywords(query)
    return result


@search_blueprint.route('/news/<string:query>', methods=['GET'])
def search_news(query: str):
    result = search_service.search_news(query)
    return result


@search_blueprint.route('/historic/<string:query>', methods=['GET'])
def search_historic(query: str):
    result = search_service.search_historic(query)
    return result


@search_blueprint.route('/combined/<string:query>/<string:start_date>/<string:end_date>', methods=['GET'])
def search_combined(query: str, start_date: str, end_date: str):
    date_format = "%Y-%m-%d"
    try:
        start_date_parsed = datetime.strptime(start_date, date_format).date()
        end_date_parsed = datetime.strptime(end_date, date_format).date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    if start_date_parsed > end_date_parsed:
        return jsonify({"error": "Start date cannot be after end date"}), 400

    result = search_service.search_combined(query, start_date_parsed, end_date_parsed)
    return result