import json
import urllib2

from math import radians, sin, cos, atan2, sqrt, asin, degrees

earth_radius = 6371500  # radius of the earth in meters
aproximation = 111000   # 1 degree is 111 kilometers

poi_proxy_url = "http://89.216.30.67:55556/es.alrocar.poiproxy.rest"

def distance_between_GPS_coordinates(lat_a, lon_a, lat_b, lon_b):
    """
    Calculates the distance in meters between two global positioning service points
    :param lat_a: the latitude of the first point
    :param lon_a: the longitude of the first point
    :param lat_b: the latitude of the second point
    :param lon_b: the longitude of the second point
    :return: returns the distance in meters
    """
    d_lon = radians(lon_b - lon_a)
    d_lat = radians(lat_b - lat_a)
    a = ((sin(d_lat/2)) ** 2) + cos(radians(lat_a)) * cos(radians(lat_b)) * ((sin(d_lon/2)) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return earth_radius * c

def translate_coordinates(lat, lon, angle, distance):
    """
    Given a start point, bearing, and distance, function will calculate the destination point. 
    It returns really good results, but this function is time consuming.
    NOTE: Works with mathematical degrees on input.
    :param lat: the latitude of the start point
    :param lon: the longitude of the start point
    :param angle: angle of closest path between start and end point
    :return returns the GPS coordinates of end point
    """
    bearing =  radians( angle )
    angular_distance = distance / earth_radius
    rad_lat = radians(lat)
    rad_lon = radians(lon)
    latitude = asin( sin(rad_lat) * cos(angular_distance) + cos(rad_lat) * sin(angular_distance) * cos(bearing) )
    longitude = rad_lon + atan2( sin(bearing) * sin(angular_distance) * cos(rad_lat), cos(angular_distance) - sin(rad_lat) * sin(latitude))
    
    return dict([('lat', degrees(latitude) ), ('lon', degrees(longitude) )])

def translate_coordinates_lightweight(lat, lon, angle, distance):
    """
    Given a start point, bearing, and distance, function will calculate the destination point. 
    Resulting translation is not great but is fast and simple.
    NOTE: Works with mathematical degrees on input.
    :param lat: the latitude of the start point
    :param lon: the longitude of the start point
    :param angle: angle of closest path between start and end point
    :return returns the GPS coordinates of end point
    """
    aproximation = 111000
    angle_radians = radians( angle )
    aproximated_distance = float(distance) / aproximation
    latitude = lat + ( sin(angle_radians) * aproximated_distance )
    longitude = lon + ( cos(angle_radians) * aproximated_distance )
    return dict([ ('lat', latitude), ('lon', longitude) ])

def get_poi_proxy_server_response(service_request_url):
    """
    Gets the result from the POI proxy server
    :param service_request_url: the extension to the base url
    :return: the raw request string
    """
    call = urllib2.urlopen(poi_proxy_url + service_request_url, None, 5)
    if call.getcode() == 200:
        return call.read()

    return None

def get_available_categories():

    """
    Returns all the categories that the POI proxy can recognize
    :return: A list of strings each string represents a category
    """
    raw_data = get_poi_proxy_server_response("/describeServices")
    return json.loads(raw_data)['categories']


def browse_by_tile(service, x, y, z):
    """
    Browses POI by a Google tile
    :param service: pull POI's from this service
    :param x: the x of a tile in google maps
    :param y: the y of a tile in google maps
    :param z: the z of a tile in google maps
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, date_taken, date_upload, image, license, name, owner,
    owner_name, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/browse?service=%s&z=%d&x=%d&y=%d" % (service, z, y, x)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']


def browse_by_extent(service, min_x, max_x, min_y, max_y):

    """
    Browses POI within a bounding box
    :param service: pull POI's from this service
    :param min_x: a value in the coordinate reference system EPSG:4326
    :param max_x: a value in the coordinate reference system EPSG:4326
    :param min_y: a value in the coordinate reference system EPSG:4326
    :param max_y: a value in the coordinate reference system EPSG:4326
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, datetaken, dateupload, image, license, name, owner,
    ownername, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/browseByExtent?service=%s&minX=%f&minY=%f&maxX=%f&maxY=%f" % \
              (service, min_x, min_y, max_x, max_y)
    raw_data = get_poi_proxy_server_response(request)
    
    return json.loads(raw_data)['features']

def browse_by_radius(service, lat, lon, radius):
    """
    Browses POI within the radius of a certain point
    :param service: pull POI's from this service
    :param lat: latitude of a point
    :param lon: longitude of a point
    :param radius: the radius
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, date_taken, date_upload, image, license, name, owner,
    owner_name, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/browseByLonLat?service=%s&lon=%f&lat=%f&dist=%f" % (service, lon, lat, radius)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']


def search_by_tile(service, x, y, z, search_term):
    """
    Searches POI by a google tile
    :param service: pull POI's from this service
    :param x: the x of a tile in google maps
    :param y: the y of a tile in google maps
    :param z: the z of a tile in google maps
    :param search_term: the term you are searching for ex. cave, bar...
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, date_taken, date_upload, image, license, name, owner,
    owner_name, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/browse?service=%s&z=%d&x=%d&y=%d&query=%s" % (service, z, x, y, search_term)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']


def search_by_extent(service, min_x, max_x, min_y, max_y, search_term):
    """
    Searches POI within a bounding box
    :param service: pull POI's from this service
    :param min_x: a value in the coordinate reference system EPSG:4326
    :param max_x: a value in the coordinate reference system EPSG:4326
    :param min_y: a value in the coordinate reference system EPSG:4326
    :param max_y: a value in the coordinate reference system EPSG:4326
    :param search_term:  cave, bar...
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, date_taken, date_upload, image, license, name, owner,
    owner_name, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/browseByExtent?service=%s&minX=%f&minY=%f&maxX=%f&maxY=%f&query=%s" % \
              (service, min_x, min_y, max_x, max_y, search_term)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']


def search_by_radius(service, lat, lon, radius, search_term):
    """
    Searches POI within the radius of a certain point
    :param service: pull POI's from this service
    :param lat: latitude of a point
    :param lon: longitude of a point
    :param radius: the radius
    :param search_term:  cave, bar...
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, date_taken, date_upload, image, license, name, owner,
    owner_name, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/browseByLonLat?service=%s&lon=%f&lat=%f&dist=%f&query=%s" % (service, lat, lon, radius, search_term)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']
