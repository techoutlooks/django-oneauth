import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oneauth",
    version="0.1.0",
    author="Edouard Carvalho",
    author_email="ceduth@techoutlooks.com",
    description="Swappable `Smart` user model with JWT-based authentication and OTP APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/techoutlooks/django-oneauth",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "Django>=2.2",
        "phonenumbers>=8.11.1",
        "django-phonenumber-field>=4.0",
        "django-cors-headers>=3.2",
        "djangorestframework>=3.10",
        "djangorestframework-simplejwt>=4.3",
        "django-rest-framework-loopback-js-filters>=1.1.4",
        "twilio>=6.33.1",
        "django-pandas>=0.6.1"
    ]
)
