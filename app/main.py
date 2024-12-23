from flask import Flask, render_template
from app.controllers.statistic_controller import statistics_blueprint

app = Flask(__name__)
app.register_blueprint(statistics_blueprint, url_prefix="/api/statistics")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
