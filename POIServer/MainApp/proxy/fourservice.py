import urllib2
import json
import math

from MainApp.proxy.toolbox import get_poi_proxy_server_response, distance_between_GPS_coordinates
from MainApp.models import FoursquareMainCategories, FoursquareChildCategories, FoursquareGrandchildCategories 

''' Client secret and client id are property of Pro develop '''
client_id = "S5MN2YCYHT5EQS31KC1I10L4ELT43IGXO0FWE0IDTMSO5J2F"
client_secret = "QUIBVAC2Q0IIYVKVLJEMMABXEUEMTR3KJC3Z12UG5MCKFTSR"
foursquare_categories_url = "https://api.foursquare.com/v2/venues/categories?client_id=%s&client_secret=%s&v=20141201" % (client_id, client_secret)

def get_foursquare_categories():
    """ 
    Add Foursquare categories to database
    :return: content of Foursquare API response
    """
    result = urllib2.urlopen(foursquare_categories_url, None, 5)
    if result.getcode() == 200:
        return result.read()
    
    return None

def store_all_categories():
    content = json.loads(get_foursquare_categories())
    categories = (content['response']) ['categories']
    lst_categories = []
    ''' Go trough main categories and store them to database. '''
    for category in categories:
        lst_categories.append(category) 
    return lst_categories

def get_main_categories():
    """
    Returns list of main categories from Foursquare API
    :return: A list of tuples (name, identification number)
    """
    
    content = get_foursquare_categories()
    json_content = json.loads( content )
    data = (( json_content['response'] ) ['categories'] )
    lst_main_categories = []
    
    for row in data:
        lst_main_categories.append( ( row['name'] , row['id'] ) )
        
    return lst_main_categories

def store_main_categories():
    """
    Stores main categories from Foursquare API to local database
    """
    lst = get_main_categories()
    for element in lst:
        read =  FoursquareMainCategories.objects.filter (
                FoursquareMainCategories.id == element[1]).count()
                
        store = FoursquareMainCategories (categoryID = element[1], name = element[0] )
        if read == 0:
            store.save()
            
def get_points_ne_sw(NE_lat, NE_lng, SW_lat, SW_lng, categories):
    """
    Function reads input north-east and south-west points and split that area in smaller areas. Areas 
    forwarded to Foursquare API are in range 150 - 300 meters in height and/or width. (NOTE: Area can be 
    smaller if original area is smaller than 300 metes in one or both dimensions.
    :param NE_lat: latitude of north-east point
    :param NE_lng: longitude of north-east point
    :param SW_lat: latitude of south-west point
    :param SW_lng: longitude of south-west point
    :return: JSON object containing all responses  
    """   
    
    ''' Split selected area to smaller areas '''
    num_width = math.ceil( distance_between_GPS_coordinates(NE_lat, NE_lng, NE_lat, SW_lng)/300.0 )
    num_height = math.ceil( distance_between_GPS_coordinates(NE_lat, NE_lng, SW_lat, NE_lng)/300.0 )
    
    delta_width = (NE_lng - SW_lng)/ float(num_width)
    delta_height = (NE_lat - SW_lat)/ float(num_height)    
    
    ''' Call foursquare API with or without category specification '''
    cat_string = ""
    raw_data_array = []
        
    for row in categories:
        cat_string = cat_string + "," + row
            
    for i in range(0, int(num_width) ):
        for j in range(0, int(num_height) ):
            
            ''' We will use these later '''
            min_lng = SW_lng + i*delta_width
            min_lat = SW_lat + j*delta_height
            max_lng = SW_lng + (i+1)*delta_width
            max_lat = SW_lat + (j+1)*delta_height
            
            ''' Check if categories or all '''
            if ( len(categories) ):
                request = "/browseByExtent?service=%s&minX=%f&minY=%f&maxX=%f&maxY=%f&categoryId=" % \
                    ('fourservice', min_lng, min_lat, max_lng, max_lat)
            else:
                request = "/browseByExtent?service=%s&minX=%f&minY=%f&maxX=%f&maxY=%f" % \
                    ('fourservice', min_lng, min_lat, max_lng, max_lat)
    
            request = request + cat_string[1:]  
    
            ''' Get Foursquare response '''
            raw_data = json.loads( get_poi_proxy_server_response(request) )['features']   
            for row in raw_data:
                row_lng = ( (row['geometry']) ['coordinates']) [0]
                row_lat = ( (row['geometry']) ['coordinates']) [1]
                if ( (row_lng < max_lng) and (row_lng > min_lng) and (row_lat < max_lat) and (row_lat > min_lat) ):
                    raw_data_array.append( row )                 
        
    return raw_data_array
           
def read_main_categories():
    """
    Enables to user to read Foursquare categories from database
    :return: List containing names and identifications of categories
    """
    lst_read = []
    read = FoursquareMainCategories.objects.all()
    
    for element in read:
        lst_read.append({ "name" : element.name, "categoryID" : element.categoryID })
        
    return lst_read