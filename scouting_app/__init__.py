from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from .utils.log import log
from config import Config


def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.debug = Config.FLASK_DEBUG
    app.secret_key = Config.SECRET_KEY

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login.login"

    with app.app_context():
        from .users import login
        from .scouting_dashboard import scouting_dashboard

        login_manager.user_loader(login.load_user)

        app.register_blueprint(login.login_bp)
        app.register_blueprint(scouting_dashboard.scouting_dashboard_bp)


        if Config.ENVIRONMENT != 'PD':
            socketio = SocketIO(app)

            @socketio.on('live reload')
            def handle_live_reload(message):
                log(message)

            socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True, use_reloader=False)

        return app
