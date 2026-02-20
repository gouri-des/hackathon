from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load schemes dataset
with open('schemes.json') as f:
    schemes = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    eligible_schemes = []

    if request.method == 'POST':
        age = int(request.form['age'])
        income = int(request.form['income'])
        occupation = request.form['occupation']

        # Check eligibility
        for scheme in schemes:
            if (
                age >= scheme['min_age'] and
                income <= scheme['max_income'] and
                (scheme['occupation'] == occupation or scheme['occupation'] == "any")
            ):
                eligible_schemes.append(scheme)

    return render_template('index.html', schemes=eligible_schemes)

if __name__ == '__main__':
    app.run(debug=True)
