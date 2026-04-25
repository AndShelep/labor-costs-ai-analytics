from flask import Flask, render_template, send_from_directory
import os
import glob
from pathlib import Path


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", BASE_DIR / "artifacts" / "visualization"))


def get_chart_files():
    if not os.path.exists(REPORTS_DIR):
        return []

    files = glob.glob(str(REPORTS_DIR / "*.png"))
    files = [os.path.basename(f) for f in files]
    files.sort()
    return files


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/charts")
def charts():
    chart_files = get_chart_files()
    return render_template("charts.html", chart_files=chart_files)


@app.route("/figures/<path:filename>")
def figures(filename):
    return send_from_directory(REPORTS_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)