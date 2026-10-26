from pathlib import Path
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "house_price_model.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"

app = Flask(__name__)

FEATURES = [
    ("CRIM", "Per-capita crime rate", "0.00632"),
    ("ZN", "Residential land zoned (%)", "18"),
    ("INDUS", "Non-retail business acres (%)", "2.31"),
    ("CHAS", "Charles River tract (0 or 1)", "0"),
    ("NOX", "Nitric oxide concentration", "0.538"),
    ("RM", "Average rooms per dwelling", "6.575"),
    ("AGE", "Owner-occupied units built before 1940 (%)", "65.2"),
    ("DIS", "Distance to employment centres", "4.09"),
    ("RAD", "Highway accessibility index", "1"),
    ("TAX", "Property-tax rate", "296"),
    ("PTRATIO", "Pupil-teacher ratio", "15.3"),
    ("B", "Dataset feature B", "396.9"),
    ("LSTAT", "Lower-status population (%)", "4.98"),
]

model = None
scaler = None
load_error = None

try:
    with MODEL_PATH.open("rb") as f:
        model = pickle.load(f)
    with SCALER_PATH.open("rb") as f:
        scaler = pickle.load(f)
    if getattr(model, "n_features_in_", 13) != 13:
        raise ValueError("The model must expect 13 input features.")
except Exception as exc:
    load_error = str(exc)

@app.get("/")
def home():
    return render_template("index.html", features=FEATURES, load_error=load_error)

@app.post("/predict")
def predict():
    if model is None or scaler is None:
        return jsonify({
            "error": "Model or scaler could not be loaded. Put house_price_model.pkl and scaler.pkl in the same folder as app.py."
        }), 500

    try:
        data = request.get_json(force=True)
        values = [float(data[name]) for name, _, _ in FEATURES]
        if not np.all(np.isfinite(values)):
            raise ValueError("Please enter valid finite numbers for every field.")

        row = np.array(values, dtype=float).reshape(1, -1)
        row_scaled = scaler.transform(row)
        price_thousands = float(model.predict(row_scaled)[0])

        return jsonify({
            "price_thousands": round(price_thousands, 2),
            "price_dollars": round(price_thousands * 1000, 2)
        })
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": f"Please check all 13 inputs. {exc}"}), 400
    except Exception:
        return jsonify({"error": "Prediction failed. Check that your model and scaler were trained together using these 13 features."}), 500

if __name__ == "__main__":
    app.run(debug=True)
