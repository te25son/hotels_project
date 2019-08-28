<h1 align="center">MaykinHotels Project</h1>

This is a test project which demonstrates how to access authenticated HTTP files and automatically add the accessed data to Django models.

A working version of this project can be found at [MaykinHotels](https://maykin-hotels.herokuapp.com/).

### Before Getting Started

**Note that the following instructions assume you have a .env file with all the necessary variables written in a way that can be understood by [python-decouple](https://github.com/henriquebastos/python-decouple) located in your project's root directory. Most of the following commands will not work without this file.**

Make sure that you've set up a virtual environment and run `pip install -r requirements.txt`.

Now that you have django (as well as all other requirements) installed, migrate the database by typing `python manage.py migrate` into your terminal.

MaykinHotels is a deployment-ready project (in the sense that it's already been deployed), and therefore has some features which are not ready out-of-the-box. One of these features includes the installation of `whitenoise` which serves and stores Django's static files. If you try to run the project by default, you may encounter some nasty errors telling you certain CSS files could not be accessed, especially when trying to run `python manage.py test`.

To avoid these nasty errors, run `python manage.py collectstatic`.

If you would like to populate the database with the data taken from CSV files, you can simply run `python manage.py jobs`. This is also a sample of how the cron job works.


### Outline

The MaykinHotels Project is seperated into three parts:

[Hotels App](#hotels)

[Api](#api)

[Cron Job](#cron)

## Hotels

## Api

## Cron
