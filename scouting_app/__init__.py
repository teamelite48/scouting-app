from flask import Flask
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_socketio import SocketIO
from .utils.log import log
from config import CONFIG
# import config


def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.debug = CONFIG.DEBUG
    app.secret_key = CONFIG.SECRET_KEY

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    with app.app_context():
        from .users import routes
        from .scouting_dashboard import routes

        app.register_blueprint(users.login_bp)
        app.register_blueprint(scouting_dashboard.scouting_dashboard_bp)


    if CONFIG.PROD == False:
        socketio = SocketIO(app)

        @socketio.on('live reload')
        def handle_live_reload(message):
            log(message)

        socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True, use_reloader=False)

    return app
