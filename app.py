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
    lang = "en"

    if request.method == 'POST':
        age = int(request.form['age'])
        income = int(request.form['income'])
        occupation = request.form['occupation']
        gender = request.form['gender']
        state = request.form['state']
        search = request.form.get('search', '').lower()
        category = request.form.get('category', 'all')
        lang = request.form.get('lang', 'en')

        for scheme in schemes:

            reasons = []
            fail_reasons = []

            name_match = search in scheme['name'].lower()
            category_match = (category == "all" or scheme['category'] == category)

            # Eligibility checks
            if scheme['min_age'] <= age <= scheme['max_age']:
                reasons.append("Age criteria satisfied")
            else:
                fail_reasons.append("Age criteria not satisfied")

            if scheme['min_income'] <= income <= scheme['max_income']:
                reasons.append("Income criteria satisfied")
            else:
                fail_reasons.append("Income criteria not satisfied")

            if scheme['occupation'] == occupation or scheme['occupation'] == "any":
                reasons.append("Occupation criteria satisfied")
            else:
                fail_reasons.append("Occupation mismatch")

            if scheme['gender'] == gender or scheme['gender'] == "any":
                reasons.append("Gender criteria satisfied")
            else:
                fail_reasons.append("Gender mismatch")

            if scheme['state'] == state or scheme['state'] == "all":
                reasons.append("State criteria satisfied")
            else:
                fail_reasons.append("State mismatch")

            if search == "" or name_match:
                reasons.append("Search match")
            else:
                fail_reasons.append("Search mismatch")

            if category_match:
                reasons.append("Category match")
            else:
                fail_reasons.append("Category mismatch")

            if len(fail_reasons) == 0:
                scheme_copy = scheme.copy()
                scheme_copy['reasons'] = reasons
                eligible_schemes.append(scheme_copy)
            else:
                scheme_copy = scheme.copy()
                scheme_copy['fail_reasons'] = fail_reasons
                not_eligible.append(scheme_copy)

    # Language dictionary
    text = {
        "en": {
            "title": "Check Your Scheme Eligibility",
            "check": "Check Eligibility",
            "eligible": "Eligible Schemes",
            "not_eligible": "Not Eligible Schemes"
        },
        "ml": {
            "title": "പദ്ധതി അർഹത പരിശോധിക്കുക",
            "check": "അർഹത പരിശോധിക്കുക",
            "eligible": "അർഹമായ പദ്ധതികൾ",
            "not_eligible": "അർഹമല്ലാത്ത പദ്ധതികൾ"
        }
    }

    return render_template(
        'index.html',
        schemes=eligible_schemes,
        not_eligible=not_eligible,
        text=text[lang],
        lang=lang
    )

if __name__ == '__main__':
    app.run(debug=True)
