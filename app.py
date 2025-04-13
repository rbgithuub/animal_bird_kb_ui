from flask import Flask, render_template
from routes.animal_routes import animal_api

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
app.register_blueprint(animal_api)

@app.route("/animals", methods=['GET'])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
