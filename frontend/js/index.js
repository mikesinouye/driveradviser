var mymap = L.map('mapid').setView([32.231553, -110.951820], 10);
            
// Instantiate Leaflet Map
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 25,
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
		'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox.streets'
}).addTo(mymap);

$origination = $("#origination");
$destination = $("#destination");
$mode = $('#mode');
$button = $("#submit-button");
$heatmapbutton = $("#heat-button");
$('#errorModal').modal({ show: false});
var route = L.Routing.control({
				waypoints: [
				]
			}).addTo(mymap);

var markerGroup = L.layerGroup().addTo(mymap);
var heatActive = false;
var heat;
var heatmap;
var data = "";
var oldPos = 0.0
var refreshCount = 0

$heatmapbutton.click(function(event){

	if (heatActive) {
		mymap.removeLayer(heat);
		heatActive = false;
	}

	else {
		heatmap = heatmapdata;

		for (i = 0; i < heatmap.length; i++) {
			heatmap[i][2] = heatmap[i][2] / 200;
		}

		heat = L.heatLayer(heatmap, {radius: 25}).addTo(mymap);
		heatActive = true;
	}
});

setInterval(pollServer, 100);

function pollServer() {
	
	
	/*var str1 = $string1.val()
	var str2 = $string2.val()
	var dynamicPricing = document.getElementById( "dynamicPricing" )
	var mcu = document.getElementById( "mcu" )
	var requestData = JSON.stringify({'string1': str1, 'string2': str2, 'mcu': mcu.selectedIndex, 'dynamicPricing':dynamicPricing.checked})
	
	console.log("This is what we're sending to the server:")
	console.log(requestData)

	$.ajax({
		type: 'POST',
		url: 'submit',
		data: requestData,
		contentType: 'application/json',
		dataType: 'json',
		timeout: 5000,

		success: function(responseData){
			console.log("We Recieved Data from Server!")
			console.log(responseData)
			document.getElementById("success").style.display = "block"
			document.getElementById("loading").style.visibility = "hidden"
			document.getElementById("serverMessage").innerHTML = JSON.parse(responseData).data
			$('#serverSuccess').modal('show')
		},
		error: function(jqXHR, exception){
			console.log(exception)
			document.getElementById("loading").style.visibility = "hidden"
			document.getElementById("success").style.display = "none"
			$('#serverError').modal('show')
		}
	})*/
	
	$.ajax({
		type: 'GET',
		url: 'update',
		contentType: 'application/json',
		dataType: 'json',
		timeout: 500,

		success: function(responseData){
			console.log("We Recieved Data from Server!")
			console.log(responseData)
			document.getElementById("success").style.display = "block"
			document.getElementById("loading").style.visibility = "hidden"
			//data = responseData.data
			document.getElementById("serverMessage").innerHTML = responseData.OwnLat
			document.getElementById("success").innerHTML = responseData.OwnLat
			//$('#serverSuccess').modal('show')
			
			var vehicle0 = new L.LatLng(responseData.position_data[0].latitude, responseData.position_data[0].longitude)
			var vehicle1 = new L.LatLng(responseData.position_data[1].latitude, responseData.position_data[1].longitude)
			var vehicle2 = new L.LatLng(responseData.position_data[2].latitude, responseData.position_data[2].longitude)
			var vehicle3 = new L.LatLng(responseData.position_data[3].latitude, responseData.position_data[3].longitude)
			var average
			refreshCount = refreshCount + 1

			
			/*if (responseData.position_data[0].latitude > 0.001) {
				markerOrigin = new L.circleMarker(vehicle0, {radius: 5}).addTo(markerGroup)
				average = new L.LatLng(responseData.position_data[0].latitude, responseData.position_data[0].longitude)
			}
			if (responseData.position_data[1].latitude > 0.001) {
				markerOrigin = new L.circleMarker(vehicle1, {radius: 5}).addTo(markerGroup)
				average = new L.LatLng((responseData.position_data[0].latitude + responseData.position_data[1].latitude)/2, (responseData.position_data[0].longitude + responseData.position_data[1].longitude)/2)
			}
			if (responseData.position_data[2].latitude > 0.001) {
				markerOrigin = new L.circleMarker(vehicle2, {radius: 5}).addTo(markerGroup)
				average = new L.LatLng((responseData.position_data[0].latitude + responseData.position_data[1].latitude + responseData.position_data[2].latitude)/3, (responseData.position_data[0].longitude + responseData.position_data[1].longitude + responseData.position_data[2].longitude)/3)
			}
			if (responseData.position_data[3].latitude > 0.001) {
				markerOrigin = new L.circleMarker(vehicle3, {radius: 5}).addTo(markerGroup)
				average = new L.LatLng((responseData.position_data[0].latitude + responseData.position_data[1].latitude + responseData.position_data[2].latitude + responseData.position_data[3].latitude)/4, (responseData.position_data[0].longitude + responseData.position_data[1].longitude + responseData.position_data[2].longitude + responseData.position_data[3].longitude)/4)
			}*/
			
			var group
			
			if (responseData.position_data[0].latitude > 0.001) {
				marker0 = new L.circleMarker(vehicle0, {radius: 5}).addTo(markerGroup)
				group = new L.featureGroup([marker0]);
			}
			if (responseData.position_data[1].latitude > 0.001) {
				marker1 = new L.circleMarker(vehicle1, {radius: 5}).addTo(markerGroup)
				group = new L.featureGroup([marker0, marker1]);
			}
			if (responseData.position_data[2].latitude > 0.001) {
				marker2 = new L.circleMarker(vehicle2, {radius: 5}).addTo(markerGroup)
				group = new L.featureGroup([marker0, marker1, marker2]);
			}
			if (responseData.position_data[3].latitude > 0.001) {
				marker3 = new L.circleMarker(vehicle3, {radius: 5}).addTo(markerGroup)
				group = new L.featureGroup([marker0, marker1, marker2, marker3]);
			}
			
			// Same scenario
			if (Math.abs(oldPos - responseData.position_data[0].latitude) < 0.0005) {
				
			}
			
			// New scenario
			else {
				markerGroup.clearLayers()
				mymap.removeControl(route)
				//mymap.setView(average, 23)
				mymap.fitBounds(group.getBounds());
			}
			
			if (refreshCount > 5) {
				mymap.fitBounds(group.getBounds());
				refreshCount = 0
			}
	
			oldPos = responseData.position_data[0].latitude
		},
		error: function(jqXHR, exception){
			console.log(exception)
			document.getElementById("loading").style.visibility = "hidden"
			document.getElementById("success").style.display = "none"
			//$('#serverError').modal('show')
		}
	})
	
}

$button.click(function(event){
	var origin = $origination.val();
	var dest = $destination.val();
	var mode = document.getElementById( "mode" );
	var latLngOrigin;
	var latLngDest;
	var validRequest = true;

	markerGroup.clearLayers()
	mymap.removeControl(route);
	document.getElementById("loading").style.visibility = "visible";

	var match = origin.search("85719");
	if (match == -1) {
		origin = origin + " 85719";
	}

	match = dest.search("85719");
	if (match == -1) {
		dest = dest + " 85719";
	}

	geocoder = new L.Control.Geocoder.Nominatim();
	
	geocoder.geocode(origin, function(originCoords) {

		if (originCoords[0] == null) {
			validRequest = false;
			document.getElementById("routeFound").style.display = "none";
			$('#addressError').modal('show');
		}
		else {
			latLngOrigin = new L.LatLng(originCoords[0].center.lat, originCoords[0].center.lng);
			markerOrigin = new L.Marker(latLngOrigin).addTo(markerGroup);
			console.log(origin + " was found at " + latLngOrigin.toString());
		}


		geocoder.geocode(dest, function(destCoords) {

			if (destCoords[0] == null) {
				validRequest = false;
				document.getElementById("routeFound").style.display = "none";
				$('#addressError').modal('show');
			}
			else {
				latLngDest = new L.LatLng(destCoords[0].center.lat, destCoords[0].center.lng);
				markerDest = new L.Marker(latLngDest).addTo(markerGroup);
				console.log(dest + " was found at " + latLngDest.toString());
			}

			if (validRequest) {
				var requestData = JSON.stringify({'originLat': latLngOrigin.lat, 'originLng': latLngOrigin.lng, 'destLat': latLngDest.lat, 'destLng': latLngDest.lng, 'dataset': mode.selectedIndex});
				console.log(requestData);

				//start

				var xhr = new XMLHttpRequest();

				xhr.responseType = "json";
				xhr.open("POST", "http://72.200.110.63:9190/get_route", true);

				xhr.addEventListener("load", function() {
					console.log("Recieved Data from Server ");
					//console.log(xhr.responseText);
					document.getElementById("loading").style.visibility = "hidden";
					var responseData = JSON.parse(xhr.response);
					var endpoints = responseData.points;
					var path = [];

					for (i = 0; i < endpoints.length; i++) {
						path[i] = new L.LatLng(endpoints[i][0], endpoints[i][1], endpoints[i][2]);
					}

					route = L.Routing.control({
						waypoints: path,
						//createMarker: function() { return null; },
						/*lineOptions: {
							addWaypoints: false
						},*/
						waypointMode: 'snap',
						lineOptions: {
							styles: [{color: 'red', opacity: 0, weight: 5}]
						}
						
					}).addTo(mymap);

					if (window.innerWidth < 750) {
						route.hide();
					}
					else route.show();

					document.getElementById("routeFound").style.display = "block";

				});

				xhr.addEventListener("progress", function(){
					document.getElementById("loading").style.visibility = "visible";
				});

				xhr.addEventListener("error", function(jqXHR, textStatus, errorThrown){
					document.getElementById("loading").style.visibility = "hidden";
					console.log(errorThrown);
					document.getElementById("routeFound").style.display = "none";
					$('#serverError').modal('show');
				});


				xhr.setRequestHeader("Content-Type", "application/json");
				xhr.send(requestData);

			}
		});
	});
})