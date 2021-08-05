from flask import Flask, render_template, request
import requests

app = Flask(__name__)

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}


@app.route('/', methods=["GET", "POST"])
def main():
    criteria_options = [
        'brands',
        'categories',
        'packaging',
        'labels',
        'origins',
        'manufacturing_places',
        'emb_codes',
        'purchase_places',
        'stores',
        'countries',
        'additives',
        'allergens',
        'traces',
        'nutrition_grades',
        'states',
    ]
    do_contains = [
        'contains',
        'does_not_contain'
    ]
    nutriment_dict = requests.get(url='https://static.openfoodfacts.org/data/taxonomies/nutrients.json')
    nutriment_dict.raise_for_status()
    nutriment_dict = dict(nutriment_dict.json())
    operator_dict = {'<': 'lt',
                     '<=': 'lte',
                     '>': 'gt',
                     '>=': 'gte',
                     '=': 'eq'}
    if request.method == 'POST':
        url = f"https://us.openfoodfacts.org/cgi/search.pl?action=process&" \
              f"search_terms={request.form['search-term']}&" \
              f"tagtype_0={request.form['criteria-0'].replace(' ', '_').lower()}&" \
              f"tag_contains_0={request.form['criteria-0-contain'].replace(' ', '_').lower()}&" \
              f"tag_0={request.form['criteria-0-value']}&" \
              f"additives={request.form['additives']}&" \
              f"ingredients_from_palm_oil={request.form['ingredients-from-palm-oil']}&" \
              f"ingredients_that_may_be_from_palm_oil={request.form['ingredients-that-may-be-from-palm-oil']}&" \
              f"ingredients_from_or_that_may_be_from_palm_oil={request.form['ingredients-from-or-that-may-be-from-palm-oil']}&" \
              f"nutriment_0={request.form['nutriment_0']}&" \
              f"nutriment_compare_0={request.form['nutriment_compare_0']}&" \
              f"nutriment_value_0={request.form['nutriment_value_0']}" \
              f"page_size=100&" \
              f"json=true"
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        response = response.json()
        return render_template('product_search.html', info=response, criteria=criteria_options,
                               do_contains=do_contains, nutriment_dict=nutriment_dict, operator_dict=operator_dict, request_method='POST')

    return render_template('product_search.html', info=[], criteria=criteria_options, do_contains=do_contains,
                           nutriment_dict=nutriment_dict, operator_dict=operator_dict)


if __name__ == '__main__':
    app.secret_key = 'amjhgmDFSg45ty43ge434534g3gFDgvFASGDg434'
    app.run(debug=True)
