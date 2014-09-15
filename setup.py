from distutils.core import setup
import meetup

readme = open('README.md').read()+open("LICENSE").read()
packages = ['meetup']
install_requires = open("requirements.txt").read().split("\n")
ext_modules = []

setup(
    name="django-meetup",
    version=meetup.__version__,
    py_modules=["meetup"],
    description="General purpose Django Meetup database to sync with Meetup.com.",
    author="Dylan Gregersen",
    author_email = "gregersen.dylan@gmail.com",
    license="3-clause BSD style license",
    long_description=readme,
    platforms=["any"],
    classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=packages,
    ext_modules=ext_modules,
    install_requires=install_requires,    
)