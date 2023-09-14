from django.shortcuts import render
import requests
# Create your views here.

def country_search(request):
    if request.method == 'POST':
        country_name = request.POST.get('country_name')
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url)

        if response.status_code == 200:
            country_data = response.json()
            if country_data:
                country_info = country_data[0]
                return render(request, 'country_detail.html', {'country': country_info})
            else:
                error_message = "Country not found"
        else:
            error_message = "Invalid Country Name !!"

        return render(request, 'search.html', {'error_message': error_message})

    return render(request, 'search.html')