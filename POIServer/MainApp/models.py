from django.db import models


class FoursquareMainCategories (models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    pluralName = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    shortName = models.CharField(max_length=30)


class FoursquareChildCategories (models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    pluralName = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    shortName = models.CharField(max_length=30)
    parentId = models.CharField(max_length=50)
