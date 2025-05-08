import requests
import math
from django.shortcuts import render
from django.conf import settings
from datetime import date

API_URL = "https://api.fellahedar.com/api/v1/product"
PAGE_SIZE = 6

def product_list(request):
    # Extract query parameters from the request
    page = request.GET.get('page', 1)
    size = request.GET.get('size', PAGE_SIZE)

    # Build URL with pagination
    params = {
        'page': int(page) - 1, # In the api, index starts at 0
        'size': size
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        products = data.get('content', [])
        total_elements = response.json().get("totalElements", 0)
        total_pages = math.ceil(total_elements / PAGE_SIZE)
    except Exception as e:
        products = []
        print("Error fetching products:", e)

    return render(request, "products.html", {
        "products": products,
        "current_page": page,
        "total_pages": total_pages,
        "now": date.today()
    })
