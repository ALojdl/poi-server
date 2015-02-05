from django.db import models
    
class FoursquareMainCategories (models.Model):
    id = models.CharField (max_length = 20, primary_key = True)
    pluralName = models.CharField (max_length = 50)
    name = models.CharField (max_length = 50)
    shortName = models.CharField (max_length = 20)
    
class FoursquareChildCategories (models.Model):
    id = models.CharField (max_length = 20, primary_key = True)
    pluralName = models.CharField (max_length = 50)
    name = models.CharField (max_length = 50)
    shortName = models.CharField (max_length = 20)
    parentId = models.CharField (max_length = 20)

class FoursquareGrandchildCategories (models.Model):
    id = models.CharField (max_length = 20, primary_key = True)
    pluralName = models.CharField (max_length = 50)
    name = models.CharField (max_length = 50)
    shortName = models.CharField (max_length = 20)
    parentId = models.CharField (max_length = 20)
    grandparentId = models.CharField (max_length = 20)
    
