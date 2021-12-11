from kubelet_stats_exporter.config import EXPORTER_PORT
from kubelet_stats_exporter.exporter import bp
from kubelet_stats_exporter.logging import logger
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app

if __name__ == "__main__":
    logger.info(f"Starting Kubelet Stats Exporter App in port: {EXPORTER_PORT}")
    app = create_app()
    app.run(host='0.0.0.0', port=EXPORTER_PORT)
