import logging

from flask import Flask, redirect, url_for


def create_app(config, debug=False, testing=False,config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    with app.app_context():
        from . import model
        model.init_app(app)

    # registering my CRUD blueprint
    from .crud import crud
    app.register_blueprint(crud)


    # the default page if all else fails
    @app.route("/")
    def index():
        return redirect(url_for('crud.list'))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.

    @app.errorhandler(500)
    def server_error(e):
        return """
           An internal error occurred: <pre>{}</pre>
           See logs for full stacktrace.
           """.format(e), 500

    return app


