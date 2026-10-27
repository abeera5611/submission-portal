import json, os
from flask import Flask, request, render_template
from validators import validate

def create_app(data_file="submissions.json"):
    app = Flask(__name__)

    def load():
        return json.load(open(data_file)) if os.path.exists(data_file) else []

    @app.route("/", methods=["GET", "POST"])
    def index():
        errors = []
        if request.method == "POST":
            form = {k: request.form.get(k, "").strip() for k in ("name", "reg_no", "title", "url")}
            errors = validate(form)
            if not errors:
                items = load(); items.append(form)
                json.dump(items, open(data_file, "w"))
        return render_template("index.html", errors=errors, submissions=load())

    return app

if __name__ == "__main__":
    create_app().run(port=5000)