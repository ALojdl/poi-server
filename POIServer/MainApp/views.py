import json 

from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.template import RequestContext, loader

from MainApp.models import FoursquareMainCategories
from MainApp.proxy.fourservice import get_main_categories, get_points_ne_sw, store_all_categories

def report(request):
    categories = FoursquareMainCategories.objects.all()
    template = loader.get_template('poi_report.html')
    context = RequestContext(request, {
        'list_cat' : categories})
    return HttpResponse(template.render(context))

def get_categories(request):
    data = get_main_categories()
    
    list_of_main_categories = []
    
    for row in data:
        list_of_main_categories.append( (row[0], row[1]) )
        
    for row in list_of_main_categories:
        read = FoursquareMainCategories.objects.filter(id = row[1]).count()
        
        if read == 0:
            store = FoursquareMainCategories(id = row[1], name = row[0])
            store.save()
        
    return HttpResponse(list_of_main_categories) 

@csrf_protect
def foursquare_service(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        NE_lat = json_data['ne_lat'];
        NE_lng = json_data['ne_lng'];
        SW_lat = json_data['sw_lat'];
        SW_lng = json_data['sw_lng'];
        categories = json_data['cat'];   
        
        raw_features = get_points_ne_sw( float(NE_lat), float(NE_lng), float(SW_lat), float(SW_lng), categories)   
        
        ''' See what POIs we want to delete - Other people here '''
        delete_elements = []
        for i in xrange( len(raw_features) ):
            if ( ((raw_features[i]) ['properties']) ['name'] == "Other people here" ):
                delete_elements.append(i);
        
        ''' Delete all element stored in delete_elements list '''
        num = 0;  
        for n in xrange( len(delete_elements) ):
            raw_features.pop( delete_elements[n] - num )
            num = num + 1
            
        ''' Pack data to JSON and send it to client '''
        return HttpResponse(json.dumps(raw_features), content_type="application/json")
    else:
        raw_data = get_points_ne_sw( 45.255, 19.845, 45.254, 19.815, [])
        return HttpResponse(raw_data)

def testing(request):
    raw_data = store_all_categories()
    return HttpResponse(raw_data)