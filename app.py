from flask import Flask, render_template, request
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
    show_only_eligible = False

    lang = request.form.get("lang", "en")
    text = languages.get(lang, languages["en"])

    if request.method == 'POST':
        submitted = True

        age = int(request.form['age'])
        income = int(request.form['income'])
        occupation = request.form['occupation']
        show_only_eligible = request.form.get("only_eligible") == "on"
        search = request.form.get("search", "").lower()
        category = request.form.get("category", "all")
        gender = request.form.get("gender", "any")
        state = request.form.get("state", "any")

        if age < 18 and occupation != "student":
            underage_warning = (
                "Applicants below 18 years are eligible only under student-specific schemes."
            )

        for scheme in schemes:
            pass_reasons = []
            fail_reasons = []
            suggestions = []

            scheme_category = scheme.get("category", "other")
            scheme_gender = scheme.get("gender", "any")
            scheme_state = scheme.get("state", "any")
            scheme_occupation = scheme.get("occupation", "any")

            if search and search not in scheme['name'].lower():
                continue

            if category != "all" and scheme_category != category:
                continue

            if gender != "any" and scheme_gender != "any" and scheme_gender != gender:
                continue

            if state != "any" and scheme_state != "any" and scheme_state != state:
                continue

            # Age check
            min_age = scheme.get('min_age', 0)
            max_age = scheme.get('max_age', 120)

            if min_age <= age <= max_age:
                pass_reasons.append(text["age_ok"])
            else:
                fail_reasons.append(text["age_fail"])
                if age < min_age:
                    suggestions.append(f"You may qualify once you turn {min_age}.")
                elif age > max_age:
                    suggestions.append(f"This scheme is only for applicants up to age {max_age}.")

            # Income check
            min_income = scheme.get('min_income', 0)
            max_income = scheme.get('max_income', 9999999)

            if min_income <= income <= max_income:
                pass_reasons.append(text["income_ok"])
            else:
                fail_reasons.append(text["income_fail"])
                if income > max_income:
                    suggestions.append(f"Income must be below ₹{max_income:,}.")
                elif income < min_income:
                    suggestions.append(f"Minimum required income is ₹{min_income:,}.")

            # Occupation check
            if scheme_occupation == "any" or scheme_occupation == occupation:
                pass_reasons.append(text["occupation_ok"])
            else:
                fail_reasons.append(text["occupation_fail"])
                suggestions.append(f"This scheme is meant for {scheme_occupation.replace('_',' ')}.")

            scheme_copy = scheme.copy()
            scheme_copy["category"] = scheme_category

            if not fail_reasons:
                scheme_copy["reasons"] = pass_reasons
                eligible_schemes.append(scheme_copy)
            else:
                if not show_only_eligible:
                    scheme_copy["fail_reasons"] = fail_reasons
                    scheme_copy["suggestions"] = suggestions
                    not_eligible.append(scheme_copy)

    return render_template(
        "index.html",
        schemes=eligible_schemes,
        not_eligible=not_eligible,
        text=text,
        lang=lang,
        underage_warning=underage_warning,
        submitted=submitted,
        show_only_eligible=show_only_eligible
    )

if __name__ == "__main__":
