# HabitatIQ — House Price Predictor

A responsive HTML/CSS/JavaScript frontend backed by Flask and your supplied scikit-learn model + scaler.

## Files included

- `app.py` — Flask server and prediction API
- `templates/index.html` — HTML page
- `static/style.css` — responsive styling
- `static/script.js` — form validation and prediction request
- `house_price_model.pkl` — supplied trained model
- `scaler.pkl` — supplied feature scaler

## Run on macOS

1. Extract this ZIP file.
2. Open Terminal and enter the extracted folder. If it is in Downloads:

   ```bash
   cd ~/Downloads/HabitatIQ_House_Price_Predictor
   ```

3. Create and activate a virtual environment, then install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install flask numpy scikit-learn
   ```

4. Start the website:

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser. Keep Terminal open while using the site. Press `Control+C` to stop it.

## Model inputs

The app expects these 13 features in this exact order: `CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT`.

The model and scaler files were supplied together. Pickle files should only be loaded when trusted. If scikit-learn reports a version warning, it means the saved files were created with a different scikit-learn version; a warning may be harmless, but use the original version if you encounter load/prediction errors.

## Important limitation

This project uses the historical Boston Housing dataset format. Predictions are in thousands of dollars as expected by that dataset and are not a reliable estimate of today's real-world home prices.
