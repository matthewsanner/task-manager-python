from flask import Flask, render_template
from tasks import tasks_bp
import config

app = Flask(__name__)
app.config.from_object(config.Config)

# Register blueprints
app.register_blueprint(tasks_bp, url_prefix='/api')

# Serve index page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=app.config['DEBUG'])