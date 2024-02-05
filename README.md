# openIMIS Backend Patient_managment reference module
This repository holds the files of the openIMIS Backend Patient_managment reference module.
It is dedicated to be deployed as a module of [openimis-be_py](https://github.com/openimis/openimis-be_py).

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## Backend Developers setup

### To start working in openIMIS as a (module) developer:

<table align="center"><tr><td>When programming for openIMIS backend, you are highly encouraged to used the features provided in the openimis-be-core module. This includes (but is not limited to) date handling, user info,...</td></tr></table>

* clone the `openimis-be_py` repo (creates the `openimis-be_py` directory)
* install python 3, recommended in a [venv](https://docs.python.org/3/library/venv.html) or [virtualenv](https://virtualenv.pypa.io)
* install [pip](https://pip.pypa.io)
* within `openimis-be_py` directory
  * install openIMIS (external) dependencies: `pip install -r
    requirements.txt`. For development workstations, one can use `pip
    install -r dev-requirements.txt` instead for more modules.
  * generate the openIMIS modules dependencies file (from openimis.json config): `python modules-requirements.py openimis.json > modules-requirements.txt`
  * if you previously installed openIMIS on another version, it seems safe to uninstall all previous modules-requirement to be sure it match current version `pip uninstall -r modules-requirements.txt`
  * install openIMIS current modules: `pip install -r modules-requirements.txt`
  * Copy the example environment setup and adjust the settings (like database connection): `cp .env.example .env`.
    Refer to .env.example for more info.
* start openIMIS from within `openimis-be_py/openIMIS`: `python manage.py runserver`

At this stage, you may (depends on the database you connect to) need to:
* apply django migrations, from `openimis-be_py/openIMIS`: `python manage.py migrate`
* create a superuser for django admin console, from
  `openimis-be_py/openIMIS`: `python manage.py createsuperuser` (will
  not prompt for a password) and then `python manage.py changepassword
  <username>`

### Module Registration and Setup

* clone this`openimis-be-patient_management_py` repo outside of `openimis-be_py`, just next to it where other 
modules are located.
* Go to `/openimis-be_py/openIMIS` and from there:
     * register your module in the pip requirements of openIMIS, referencing your 'local' codebase: `pip install -e ../../openimis-be-patient_management_py/`
  * register your module to openIMIS django site in `/openimis-be_py/openimis.json` with `
  {	"name": "patient_management",
     "pip": "openimis-be-patient_management==1.0.0"
	}`
* From here on, your local openIMIS has this new module, directly loaded from your directory.
* Run `python manage.py migrate patient_management` to get new tables reflected in your database.
* Go to `openimis-be_py/openIMIS/openIMIS/settings.py` settings file, append `"django_filters"` to help modules endpoint to be searched and filtered.
* Add `path('api/patients/', include('patient_management.urls')),` to the global urls.py patterns.

Go back to `/openimis-be_py/openIMIS` and
start the server by `python manage.py runserver`
###1 Note: The default auth is by default basic access.

### Usage

This module exposes endpoints for creating, reading, updating and deleting patients as well as for adding, retrieve the patient's medical records.

### Exposed Endpoints

* `GET /api/patients` for retrieving all patients
* `GET /api/patients/<int:id>` for retrieving all patients
* `POST /api/patients` for creating patients
* `PUT /api/patients/<int:id>` for updating patterns
* `POST /api/patients/<int:id>/add_medical_record` to list patient medical record.
* `PUT /api/patients/<int:id>/edit_medical_record/<int:record_id>` to edit a patient medical record.
* `DEL /api/patients/<int:id>/delete_medical_record/<int:record_id>` to delete a patient medical record.

### DB

![DB Sketch](https://github.com/Chrisdanyk/openimis-be-patient_management_py/blob/main/assets/PatientData%20Diagram.png "Optional title")