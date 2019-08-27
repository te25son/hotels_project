from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.db.models import Q

from .models import Hotel


class CitySearchTemplateView(TemplateView):
    """
    Basic template view to act as home page
    and displays a searchbar whereby users
    can search by city names.

    Upon search, the user is redirected to
    the HotelListView.
    """
    template_name = 'search.html'


class HotelListView(ListView):
    """
    A view that lists the hotels located
    within the searched for city.
    """
    model = Hotel
    template_name = 'hotel_results.html'

    def get(self, request, *args, **kwargs):
        """
        Custom get request that gets the queried object
        from CitySearchTemplateView and returns a
        view that displays all hotels which are located
        within the query.

        Uses an empty string as a query object if no
        object is given.
        """
        query = request.GET.get('q')
        if not query:
            query = ""
        hotels = Hotel.objects.filter(
            city__name__icontains=query
        )
        return render(request, self.template_name, {'hotels':hotels, 'query':query})
