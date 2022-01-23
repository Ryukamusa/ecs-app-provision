from flask import Flask, render_template
import os

_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.template_folder = os.path.join(_dir, "templates")


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=80)

