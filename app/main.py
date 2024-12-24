from flask import Flask, render_template

from app.controllers.search_controller import search_blueprint
from app.controllers.statistic_controller import statistics_blueprint

app = Flask(__name__)
app.register_blueprint(statistics_blueprint, url_prefix="/api/statistics")
app.register_blueprint(search_blueprint, url_prefix="/api/search")


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
