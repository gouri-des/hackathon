from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load schemes dataset
with open('schemes.json') as f:
    schemes = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    eligible_schemes = []
    not_eligible = []

    if request.method == 'POST':
        age = int(request.form['age'])
        income = int(request.form['income'])
        occupation = request.form['occupation']

        for scheme in schemes:
            pass_reasons = []
            fail_reasons = []

            # Age check
            if age >= scheme['min_age']:
                pass_reasons.append("Age criteria satisfied")
            else:
                fail_reasons.append("Age criteria not satisfied")

            # Income check
            if income <= scheme['max_income']:
                pass_reasons.append("Income within limit")
            else:
                fail_reasons.append("Income exceeds limit")

            # Occupation check
            if scheme['occupation'] == occupation or scheme['occupation'] == "any":
                pass_reasons.append("Occupation matched")
            else:
                fail_reasons.append("Occupation does not match")

            # Final decision
            scheme_copy = scheme.copy()

            if len(fail_reasons) == 0:
                scheme_copy["reasons"] = pass_reasons
                eligible_schemes.append(scheme_copy)
            else:
                scheme_copy["fail_reasons"] = fail_reasons
                not_eligible.append(scheme_copy)

    return render_template(
        'index.html',
        schemes=eligible_schemes,
        not_eligible=not_eligible
    )

if __name__ == '__main__':
    app.run(debug=True)
