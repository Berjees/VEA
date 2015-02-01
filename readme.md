# VEA
Nea is a Python/Django backend used to fetch news using RSS feeds and then cluster similar news together and display as a REST API that can be used in other applications

#Important Reference
VEA is heavily based on https://github.com/matagus/django-planet for fetching the news feeds.

To integrate the project add 'planet' to your installed application in your project settings.

Also I have included a demo project to see the settings. The demo is called final and its accompanying virtual environment is venv.

If you wish to only see the cosine similarity code it is in the clustering folder.
But please note:
Contains only clustering algorithm. This class will not work with project and is only to give understanding of algorithm
If you wish to see the whole file it is located at 
planet/management/commands/__init__.py

Android application that is closed at the moment can be seen here: https://play.google.com/store/apps/details?id=com.iba.nea&hl=en

VEA is pronounced as NEA in English

You can see sample API at www.vea.cloudapp.net
