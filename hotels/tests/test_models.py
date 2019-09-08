from django.test import TestCase

from ..models import City, Hotel


class CityModelTests(TestCase):

    def setUp(self):
        City.objects.create(abbrv='NYC', name='New York')

    def test_city_created(self):
        city = City.objects.get(name='New York')
        self.assertTrue(isinstance(city, City))
        self.assertEquals(city.name, 'New York')
        self.assertEquals(city.abbrv, 'NYC')
        self.assertEquals(city.__str__(), city.name)

    def test_city_with_non_unique_abbrv_not_created(self):
        try:
            city = City.objects.create(abbrv='NYC', name='New York City')
        except:
            city = None
        self.assertFalse(isinstance(city, City))

    def test_city_with_non_unique_name_not_created(self):
        try:
            city = City.objects.create(abbrv="ABC", name="New York")
        except:
            city = None
        self.assertFalse(isinstance(city, City))


class HotelModelTests(TestCase):

    def setUp(self):
        self.city = City.objects.create(
            abbrv='NYC',
            name='New York'
        )
        Hotel.objects.create(
            city=self.city,
            loc='NYC99',
            name='The Plaza',
        )

    def test_hotel_created(self):
        hotel = Hotel.objects.get(name='The Plaza')
        self.assertTrue(isinstance(hotel, Hotel))
        self.assertEquals(hotel.city.name, 'New York')
        self.assertEquals(hotel.city.abbrv, 'NYC')
        self.assertEquals(hotel.loc, 'NYC99')
        self.assertEquals(hotel.name, 'The Plaza')
        self.assertEquals(hotel.__str__(), 'The Plaza')

    def test_hotel_with_same_name_and_city_but_diff_loc_created(self):
        hotel = Hotel.objects.create(
            city=self.city,
            loc='NYC01',
            name='The Plaza',
        )
        self.assertTrue(isinstance(hotel, Hotel))

    def test_hotel_with_non_unique_loc_and_city_not_created(self):
        try:
            hotel = Hotel.objects.create(
                city=self.city,
                loc='NYC99',
                name='The Plaza Hotel',
            )
        except:
            hotel = None
        self.assertFalse(isinstance(hotel, Hotel))
