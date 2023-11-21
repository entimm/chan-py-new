import os

from flask import Flask
from controllers import chart_controller, index_controller, tdx_chart_controller

app = Flask(__name__, template_folder='web/templates', static_folder='web/public/static')
app.register_blueprint(index_controller.blueprint)
app.register_blueprint(chart_controller.blueprint)
app.register_blueprint(tdx_chart_controller.blueprint)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

