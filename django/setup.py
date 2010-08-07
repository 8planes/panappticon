import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name = "panappticon",
    version = "0.1",
    packages = ["panappticon"],
    package_data = { "panappticon": [ "templates/panappticon/*.html" ]
                     },
    zip_save = False,
    author = "8 Planes",
    author_email = "adam@8planes.com",
    description = "Allows developers to see the story of beta users' interaction with ad-hoc",
    url = "http://8planes.com"
)
