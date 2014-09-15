from distutils.core import setup
import meetup

install_requires = open("requirements.txt").read().split("\n")
readme = open('README.rst').read()+"\nLicense\n-------\n"+open("LICENSE").read()

setup(
    name="django-meetup",
    version=meetup.__version__,
    packages=['meetup'],    
    url="https://github.com/astrodsg/django-meetup",
    description="General purpose Django Meetup database to sync with Meetup.com.",
    long_description=readme,
    license="3-clause BSD style license",
    author="Dylan Gregersen",
    author_email = "gregersen.dylan@gmail.com",
    platforms=["any"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=install_requires,    
)