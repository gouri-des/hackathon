from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open('schemes.json', encoding='utf-8') as f:
    schemes = json.load(f)

with open('lang.json', encoding='utf-8') as f:
    languages = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    eligible_schemes = []
    not_eligible = []
    lang = request.form.get("lang", "en")
    text = languages[lang]

    if request.method == 'POST':
        age = int(request.form['age'])
        income = int(request.form['income'])
        occupation = request.form['occupation']

        for scheme in schemes:
            pass_reasons = []
            fail_reasons = []

            if age >= scheme['min_age']:
                pass_reasons.append(text["age_ok"])
            else:
                fail_reasons.append(text["age_fail"])

            if income <= scheme['max_income']:
                pass_reasons.append(text["income_ok"])
            else:
                fail_reasons.append(text["income_fail"])

            if scheme['occupation'] == occupation or scheme['occupation'] == "any":
                pass_reasons.append(text["occupation_ok"])
            else:
                fail_reasons.append(text["occupation_fail"])

            scheme_copy = scheme.copy()

            if not fail_reasons:
                scheme_copy["reasons"] = pass_reasons
                eligible_schemes.append(scheme_copy)
            else:
                scheme_copy["fail_reasons"] = fail_reasons
                not_eligible.append(scheme_copy)

    return render_template(
        "index.html",
        schemes=eligible_schemes,
        not_eligible=not_eligible,
        text=text,
        lang=lang
    )

if __name__ == "__main__":
    app.run(debug=True)