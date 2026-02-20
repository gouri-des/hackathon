\from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load datasets
with open('schemes.json', encoding='utf-8') as f:
    schemes = json.load(f)

with open('lang.json', encoding='utf-8') as f:
    languages = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    eligible_schemes = []
    not_eligible = []
    underage_warning = None
    submitted = False

    lang = request.form.get("lang", "en")
    text = languages.get(lang, languages["en"])

    if request.method == 'POST':
        submitted = True

        age = int(request.form['age'])
        income = int(request.form['income'])
        occupation = request.form['occupation']
        search = request.form.get("search", "").lower()
        category = request.form.get("category", "all")
        gender = request.form.get("gender", "any")
        state = request.form.get("state", "any")

        # Underage warning
        if age < 18 and occupation != "student":
            underage_warning = (
                "Applicants below 18 years are eligible only under student-specific schemes."
            )

        for scheme in schemes:
            pass_reasons = []
            fail_reasons = []

            # Safe access
            scheme_category = scheme.get("category", "other")
            scheme_gender = scheme.get("gender", "any")
            scheme_state = scheme.get("state", "any")
            scheme_occupation = scheme.get("occupation", "any")

            # Search filter
            if search and search not in scheme['name'].lower():
                continue

            # Category filter
            if category != "all" and scheme_category != category:
                continue

            # Gender filter
            if gender != "any" and scheme_gender != "any" and scheme_gender != gender:
                continue

            # State filter
            if state != "any" and scheme_state != "any" and scheme_state != state:
                continue

            # -------------------------
            # Eligibility checks
            # -------------------------

            # Age
            if age >= scheme.get('min_age', 0) and age <= scheme.get('max_age', 120):
                pass_reasons.append(text["age_ok"])
            else:
                fail_reasons.append(text["age_fail"])

            # Income
            if income >= scheme.get('min_income', 0) and income <= scheme.get('max_income', 9999999):
                pass_reasons.append(text["income_ok"])
            else:
                fail_reasons.append(text["income_fail"])

            # Occupation (UPDATED LOGIC)
            if scheme_occupation == "any" or scheme_occupation == occupation:
                pass_reasons.append(text["occupation_ok"])
            else:
                fail_reasons.append(text["occupation_fail"])

            scheme_copy = scheme.copy()
            scheme_copy["category"] = scheme_category

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
        lang=lang,
        underage_warning=underage_warning,
        submitted=submitted
    )

if __name__ == "__main__":
    app.run(debug=True)
