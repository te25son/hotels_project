from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from ..admin import CityAdmin, HotelAdmin
from ..resources import CityResource, HotelResource
from ..models import City, Hotel
from ..formats import SCSV


class MockRequest:
    pass


request = MockRequest()


class CityAdminTests(TestCase):

    def setUp(self):
        self.city = City.objects.create(
            abbrv='NYC',
            name='New York'
        )
        self.site = AdminSite()
        self.cityadmin = CityAdmin(City, self.site)

    def test_admin_string(self):
        self.assertEquals(str(self.cityadmin), 'hotels.CityAdmin')

    def test_uses_city_fields(self):
        self.assertEquals(
            list(self.cityadmin.get_fields(request)),
            ['abbrv', 'name']
        )
        self.assertEquals(
            list(self.cityadmin.get_fields(request, self.city)),
            ['abbrv', 'name']
        )

    def test_uses_cityresource_instance(self):
        self.assertEquals(self.cityadmin.resource_class, CityResource)

    def test_list_display(self):
        self.assertEquals(self.cityadmin.list_display, ('abbrv', 'name'))

    def test_returns_correct_import_format(self):
        self.assertEquals(self.cityadmin.get_import_formats(), [SCSV,])


class HotelAdminTests(TestCase):

    def setUp(self):
        city = City.objects.create(
            abbrv='NYC',
            name='New York',
        )
        self.hotel = Hotel.objects.create(
            city=city,
            loc='NYC99',
            name='The Plaza'
        )
        self.site = AdminSite()
        self.hoteladmin = HotelAdmin(Hotel, self.site)

    def test_admin_string(self):
        self.assertEquals(str(self.hoteladmin), 'hotels.HotelAdmin')

    def test_uses_hotel_fields(self):
        self.assertEquals(
            list(self.hoteladmin.get_fields(request)),
            ['city', 'loc', 'name']
        )
        self.assertEquals(
            list(self.hoteladmin.get_fields(request, self.hotel)),
            ['city', 'loc', 'name']
        )

    def test_uses_hotelresource_instance(self):
        self.assertEquals(self.hoteladmin.resource_class, HotelResource)

    def test_list_display(self):
        self.assertEquals(self.hoteladmin.list_display, ('name', 'city', 'loc'))

    def test_returns_correct_import_format(self):
        self.assertEquals(self.hoteladmin.get_import_formats(), [SCSV,])
