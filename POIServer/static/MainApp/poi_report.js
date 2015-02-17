$('document').ready(function(){
	// Global variables //
	var num_clicks = 0;
	
	var base_layer = L.tileLayer(
	  'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
	    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
	    maxZoom: 18
	  }
	);
	
	// Configuration for heat map layer //
	var configuration = {
	  "radius": 20,
	  "maxOpacity": 0.7, 
	  "scaleRadius": false, 
	  "useLocalExtrema": true,
	  latField: 'lat',
	  lngField: 'lon',
	  valueField: 'count'
	};
		
	var heatmap_layer = new HeatmapOverlay(configuration);
	
	var polygon = L.FeatureGroup();
	
	var map = new L.Map('map', {
	  center: new L.LatLng(45.2554, 19.8451),
	  zoom: 14,
	  layers: [base_layer]
	});
	
	var coordinates = new Array(2);
	
	function onLeftClick(e) {			
		if (num_clicks < 2) {
			coordinates[num_clicks] = e.latlng;
			
			if(num_clicks == 1) {					
				var coor_ne = L.latLng(coordinates[0].lat, coordinates[1].lng);
				var coor_sw = L.latLng(coordinates[1].lat, coordinates[0].lng);
				
				polygon = L.polygon([ coordinates[0], coor_ne, coordinates[1], coor_sw],
										{ smoothFactor : 0.3,
										  stroke : false,
										  opacity : 0.2} 
										).addTo(map); 	
				
				map.addLayer(heatmap_layer);
				
				categories = selectedCategories();
				
				callPOIReport(coordinates[0].lat, coordinates[1].lng, coordinates[1].lat, coordinates[0].lng, categories);		
			}
			
			num_clicks = num_clicks + 1;
		}
	}
	
	var csrftoken = $.cookie('csrftoken');

	function csrfSafeMethod(method) {
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
	
	function callPOIReport(ne_lat, ne_lng, sw_lat, sw_lng, categories) {
		
		var POI_data = $.ajax({
			url : "http://localhost:8432/MainApp/fourservice",
			type : "POST",
			dataType : "json",
			async : false,
			data : JSON.stringify({
				ne_lat : ne_lat,
				ne_lng : ne_lng,
				sw_lat : sw_lat,
				sw_lng : sw_lng,
				cat : categories
			})
			}).responseText;
			
		var points = JSON.parse( POI_data );
		var i;
		var test_data = { data : [] };
		
		for (i=0; i<points.length; i++) {
			
			test_data.data[ i ] = 
				{ lat : points[i].geometry.coordinates[1],
				  lon : points[i].geometry.coordinates[0],
				  count : 1 } ;
			
		}
		
		heatmap_layer.setData(test_data);
		
	}
	
	function onRightClick() {
		map.removeLayer(heatmap_layer);
		map.removeLayer(polygon);
		num_clicks = 0;
	}
		
	function selectedCategories() {
		var categories = [];
		$("#list li button").each(function() {
			if ($(this).hasClass("on")) {
				categories.push( $(this).data("category") );
			}
		});
		return categories;
	}
	
	
	
	
	map.on('click', onLeftClick);	
	map.on('contextmenu', onRightClick)
});