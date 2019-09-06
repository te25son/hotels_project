<h1 align="center">Hotels Project</h1>

This is a test project which demonstrates how to access authenticated HTTP files and automatically add the accessed data to Django models.

A working version of this project can be found at [Hotels](https://maykin-hotels.herokuapp.com/).

### Before Getting Started

**Note that the following instructions assume you have a .env file with all the necessary variables written in a way that can be understood by [python-decouple](https://github.com/henriquebastos/python-decouple) located in your project's root directory. Most of the following commands will not work without this file.**

Make sure that you've set up a virtual environment and run `pip install -r requirements.txt`.

Now that you have Django (as well as all other requirements) installed, migrate the database by typing `python manage.py migrate` into your terminal.

MaykinHotels is a deployment-ready project (in the sense that it's already been deployed), and therefore has some features which are not ready out-of-the-box. One of these features includes the installation of `whitenoise` which serves and stores Django's static files. If you try to run the project by default, you may encounter some nasty errors telling you certain CSS files could not be accessed, especially when trying to run `python manage.py test`.

To avoid these nasty errors, run `python manage.py collectstatic`.

If you would like to populate the database with the data taken from CSV files, you can simply run `python manage.py jobs`. This is also a sample of how the cron job works.

Taken altogether the steps can be run as follows:

```console
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py jobs
```

### Outline

The Hotels Project is separated into three parts:

[Hotels App](#hotels)

[API](#api)

[Cron Job](#cron)

## Hotels

The Hotels App is the main section of Hotels and contains the models which are used by both the API and cron job. There are two models in the Hotels App, **City** and **Hotel**.

* **The City Model** is made up of two model fields [**abbrv**, **name**]. The **abbrv** field is used to get the city object when uploading data to the Hotel model from the CSV.

```python
# extract from hotels/uploader.py

for elem in listed_data:
        city = City.objects.get(abbrv=elem[0])
        hotel, _ = Hotel.objects.get_or_create(
            city=city,
            loc=elem[1],
            name=elem[2],
        )
```

* **The Hotel Model** is made up of three model fields [**city**, **loc**, **name**] whereby city is a foreignkey relationship to the City model. For the Hotel object to be added to the database, the loc and name fields must be unique together.

The hotels app contains the main **views** for Hotels. There are two class based views attached to the hotels app, **CitySearchTemplateView** and **HotelListView**.

* **CitySearchTemplateView** acts as the home page for Hotels and includes an input field in its template whereby users can search for hotels by city name. *CitySearchTemplateView is where the primary JQuery is used to access Hotels API.*

* **HotelListView** displays a list of hotel model objects matching the query from CitySearchTemplateView.

Within the hotel app is also the **uploader.py** file which is responsible for the handling, parsing, and uploading of CSV files over authenticated HTTP to the City and Hotel models. There are HTTP objects which are fetched by uploader.py and are included in the projects settings.py file under the variable names `CITY_CSV` and `HOTEL_CSV`. Uploader.py also uses the other variables in settings `CSV_USERNAME` and `CSV_PASSWORD` to authenticate its request.

**Uploader.py** is attached to a custom Django command under `hotels.management.commands.jobs.py` which allows it to be called from the root directory as `python manage.py jobs`. This custom command is used by Hotels [Cron](#cron).

In the event that downloading over authenticated HTTP does not work, the hotels app makes use of the [Django-import-export](https://Django-import-export.readthedocs.io/en/latest/) package. The package makes use of Django's admin to add import and export options available for both the City and Hotel models.

Within Hotels, the import options have been limited to CSV files delimited by a semicolon. As Django-import-export does not come default with a format capable of importing CSV files delimited by a semicolon, a custom format has been created under `hotels.formats.py`. The custom class is called `SCSV` and inherits from Django-import-exports's base CSV format. To allow for further import options in Hotels, simply add either custom or base formats from Django-import-export to the following function in `hotels.formats.py`:

```python
def return_preferred_import_formats(*args, **kwargs):
    formats = (
        SCSV,
    )
    return [f for f in formats if f().can_import()]
```

In order to import CSV files to the Django admin, it is further required to use "resources" from Django-import-export. These resources can be found under `hotels.resources.py`. According to Django-import-export's docs:

> Resource defines how objects are mapped to their import and export representations and handle importing and exporting data.

**Note that it is very important when importing CSV files to the City and Hotel models to always import to the City Model first. Hotel objects without matching foreign keys to a City model will not be able to be uploaded.**

## API

Hotel's API used [Django's rest framework](https://www.Django-rest-framework.org/), and was buit as an easy connection between the JQuery in the template `search.html` and a json representation of the City model. This allows for the dropdown selection within the search template to be automatically updated as new data is added to the City model.

JQuery uses the API url `API/?format=json` to hook into the API and access the data.

The data is rendered through the rest frameworks serializers under `API.serializers.py`. Serializers are defined by the Django rest framework's docs as:

> [allowing] complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types.

This makes connection from the City model to JQuery simple as well as allows for the possibility of future scaling.

## Cron

Hotel's Cron job makes use of python's [APScheduler](https://apscheduler.readthedocs.io/en/latest/) and is located in the project's root directory under `jobs.py`. The cron's job is to fetch and parse data from authenticated HTTP sources as described in the [Hotels App section](#hotels) and to update the City and Hotel models with the parsed data.

The cron job makes use of two files. First, the uploader file under `hotels.uploaders.py` which contains the logic behind fetching and uploading the CSVs to their corresponding models. Second, the custom Django command under `hotels.management.commands.jobs.py` which allows the logic within `uploaders.py` to easily be called from the command line using `python manage.py jobs`.

The cron job uses Python's built-in subprocess module to call `python manage.py jobs` and scheduled to run at intervals of 30 minutes. The timing of the cron job can easily be changed by passing alternative arguments to the decorator within the cron job file. The arguments must match  
