Django One Auth
================

[django-oneauth](https://github.com/techoutlooks/django-smartmodels)

Django one-factor authentication using JWT tokens, resting on a "smart" User model.
Our User model is swappable and implemented as a [SmartModel](https://github.com/techoutlooks/django-smartmodels)
for tracking CRUD operations from model to view levels, which uses `email` or `phone_number` field as the USERNAME_FIELD.

Rationale
---------------

Needed introspection natively built into Django models for use in my SaaS projects,
to be enabled to leverage the power of big data analytics -slash- machine learning wherever needed.

Features
---------------

- Who created, updated or deleted a User instance? and when?
- Restore deleted user instances (not truly deleted, but hidden from the ORM to regular users).
- Pluggable RESTful authentication schemes (defaults to JWT).
- Optional sign-up validation via OTP (email, SMS).
- Model, Manager Admin and View mixins to help build custom Django components.
- Concrete User model exists that may be swapped for custom one.

Requirements
---------------

    Python 3+, Django 2.2+, 
    phonenumberslite, django-phonenumber-field, 
    djangorestframework, djangorestframework-simplejwt 
    django-cors-headers,


Setup
---------------

Install django-oneauth inside a virtual env.
Deps: 

    pip3 install -U virtualenv
    virtualenv -p /usr/bin/python3 venv
    source venv/bin/activate
    pip3 install -e git+https://github.com/techoutlooks/django-oneauth.git#egg=oneauth
    
Bootstrapping the demo project (complete example illustrating working with foreign models and signals)

    cd demo
    python manage.py migrate
    python manage.py runserver


Testing the REST API

- Requesting a JWT token:

        export EMAIL=<email-here>
        export PASSWORD=<password-here>
        
        # using curl
        curl \
          -X POST \
          -H "Content-Type: application/json" \
          -d "{\"email\": \"${EMAIL}\", \"password\": \"$PASSWORD\"}" \
        http://localhost:8001/api/o/token/
        
        # or, using httpie
        http post http://127.0.0.1:8001/api/o/token/ email=$EMAIL password=$PASSWORD
    
- Accessing protected resources using the JWT token obtained previously:

        curl \
          -H "Authorization: Bearer <JWT-token>" \
        http://localhost:8001/api/accounts/
    
TODO
=====
- management commands for creating restoring users, users stats, etc.