import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cs1.6.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/test_cs1.6')
    def hello():
        return 'hola mundo!'
    

    from . import db
    db.init_app(app)

    from . import canciones
    app.register_blueprint(canciones.bp)
    app.add_url_rule('/', endpoint='index')

    from . import albunes
    app.register_blueprint(albunes.bp)

    
    from . import artista
    app.register_blueprint(artista.bp)
    return app
    