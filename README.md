# Scatterplot Visualization Web Application

This is a web application that displays interactive scatterplots using data from REST web services.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Features

- Interactive scatterplots using Plotly.js
- Responsive design
- Ready to integrate with REST APIs

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript)
  - `css/style.css`: Custom styling
  - `js/main.js`: Plotting logic
- `requirements.txt`: Python dependencies
