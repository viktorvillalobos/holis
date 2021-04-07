Holis
========================

Holis is a toolkit for remote teams.

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


### Local Environment


1. Create tenant hosts

Holis is a multitenant application, we use the subdomain as tenant id, so, we need create local subdomains for work propertly.

Edit your host file and create and add this at the end

```shell
127.0.0.1 adslab.holis.local
127.0.0.1 firesoft.holis.local
127.0.0.1 holis.local
```

this allows you to use:

* https://adslab.holis.local:8000
* https://firesoft.holis.local:8000
* https://holis.local:8000

2. Uploading the backend

Upload containers in one single command

`make up`

This command will open a bash shell inside the backend environment, here you can execute different command like:

* `dev up`: is equivalent to `python manage.py runserver 0.0.0.0:8000`
* `dev makemig`: crate migrations, is equivalent to `python manage.py makemigrations``
* `dev migrate`: execute migrations, is equivalent to `python manage.py migrate`
* `dev sqlmig`: show sql of the migration
* `dev makemessages`: crete locations files.
* `dev compilemessages`: compile locations

3. Running the front app.

`cd webapp`
`yarn`
`yarn serve`

4. Use the default users to enter to the app.

**username:** viktor@hol.is
**password:** holis123.

**username:** julls@hol.is
**password:** holis123.


5.  (Optional) Create your user

Running tests with py.test


Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

.. _mailhog: https://github.com/mailhog/MailHog



Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Deployment
----------

The following details how to deploy this application.

We count with CI in production, so, you just need to push to master and the deploy process begin.


