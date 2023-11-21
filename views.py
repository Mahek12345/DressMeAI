from django.shortcuts import render, HttpResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd

# Create your views here.
from datetime import datetime


# Create your views here.
def index(request):
    # Context is set of variables we want to send
    context = {
        "var1": "this is sent",
        "var2": "This is done"
    }

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):



    return render(request, 'contact.html')


def cart(request):
    return render(request, 'cart.html')


def order(request):
    return render(request, 'order.html')


def search(request):
    if request.method == 'GET':
        search_query = "Colour:green"
        search = request.GET.get('search_query')

        if search_query is None:
            print(search_query)

            return HttpResponse("No search query provided.")

        df = pd.read_csv("dataset.csv")

        tfidf = TfidfVectorizer(stop_words='english')


        tfidf_matrix = tfidf.fit_transform(df[['name', 'colour', 'brand', 'price', 'description']].apply(
            lambda x: ' '.join(x.astype(str)), axis=1).values.astype('U'))
        

        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')

        knn_model.fit(tfidf_matrix)
        print(search_query)
        search_query = search
        terms = str(search_query).split(':')

        name_term = ''
        colour_term = ''
        price_term = ''
        brand_term = ''
        description_term = ''

        for term in terms:
            if term.startswith('colour:'):
                colour_term = term.split(':')[1]
            if term.startswith('name:'):
                name_term = term.split(':')[1]
            if term.startswith('price:'):
                price_term = term.split(':')[1]
            elif term.startswith('brand:'):
                brand_term = term.split(':')[1]
            else:
                description_term += ' ' + term

        search_terms = {'colour': colour_term, 'name': name_term, 'brand': brand_term, 'price': price_term,
                        'description': description_term.strip()}

        search_tfidf = tfidf.transform([' '.join(search_terms.values())])
        print(search_tfidf)

        indices = knn_model.kneighbors(
            search_tfidf, n_neighbors=5, return_distance=False)

        search_results = []
        for idx in indices[0]:
            product_name = df.iloc[idx]['name']
            p_id = df.iloc[idx]['p_id']
            image_url = df.iloc[idx]['img']
            product_color = df.iloc[idx]['colour']
            product_brand = df.iloc[idx]['brand']
            product_price = df.iloc[idx]['price']
            product_description = df.iloc[idx]['description']

            search_result = {'p_id': p_id, 'name': product_name, 'image_url': image_url, 'color': product_color,
                             'brand': product_brand, 'price': product_price, 'description': product_description}
            search_results.append(image_url)
            # print(search_results)

            context = {'search_results': search_results}

        # return render(request, 'search_results.html', context)
        return render(request, 'search.html', context)
