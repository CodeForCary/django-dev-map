angular.module('mapapp.gmap', [ 'mapapp.services', 'django', 'ngMaterial', 'mapapp.drawer', 'mapapp.directives' ])
.directive('map', [ 'gis', 'mapdata', 'permits', 'urls', '$mdBottomSheet', '$mdDrawer', '$filter', function(gis, mapdata, permits, urls, $mdBottomSheet, $mdDrawer, $filter) {
	return {
		transclude: true,
		restrict: 'E',
		scope: {
			selected: '=',
			list: '='
		},
		link: function($scope, $element, $attrs) {
			/*
			 * Define our Map object and center it over the region
			 * provided by django. The 'mapdata' object is injected
			 * into our 'material.html' file by django.
			 */
			var map = new google.maps.Map($element[0], {
				disableDefaultUI: true,
				zoomControl: false,
				zoom: 15
			});
			map.setCenter(mapdata.centroid);
			map.fitBounds(mapdata.extent);
			
			google.maps.event.addListener(map, 'click', function() {
				$scope.$apply(function() {
					$scope.selected = null;
				});
			});

			/*
			 * Load the permits from the server via the permits 
			 * service. Once they're loaded, establish all context 
			 * that needs the map data.
			 */
			permits.all().then(function(data) {
				// Sets the default styles/color for each region on the map
				map.data.setStyle(function(feature) {
					return {
						fillColor: $filter('cat_color')(feature.getProperty('category')),
						strokeColor: '#000000',
						strokeOpacity: 0.5,
						fillOpacity: 0.5,
						strokeWeight: 1
					};
				});
				/*
				 * When a click event occurs, ask the server 
				 * what regions live at that point. Copy those
				 * values into the binding.
				 */
				map.data.addListener('click', function(event) {
					var lat = event.latLng.lat();
					var lon = event.latLng.lng();
					permits.at(lat, lon).then(function(data) {
						//$scope.bind.bounds = data.bounds;
						$scope.list = data.permits;
						/*if (data.permits.length == 1) {
							$scope.bind.selected = data.permits[0];
						} else {
							$scope.bind.selected = null;
						}*/
					});

				});
				// This simple line loads the shapes
				map.data.addGeoJson(data);
			});

			/*
			 * Highlight our location with a marker.
			 */
			gis.locate().then(function(position) {
				var latlng = gis.toLatLng([ position.coords.latitude, position.coords.longitude ]);
				new google.maps.Marker({ 
					icon: {
						anchor: new google.maps.Point(11, 11),
						url: urls.images + "/star.svg",
					},
					position: latlng,
					map: map
				});
			});

			/*
			 * Watch the list of values. Place an icon over each
			 * entry in the list.
			 *
			 * TODO: Auto pan/zoom (watch bounds?)
			 */
			$scope.$watch('list', function(value, old) {
				if (old) {
					for (var i = 0; i < old.length; i++) {
						google.maps.event.removeListener(old[i].listener);
						if (old[i].marker) {
							old[i].marker.setMap(null);
						}
					}
				}
				if (value) {
					if (value.length > 1) {
						$scope.selected = null;
						function listen(value) {
							return function() {
								$scope.$apply(function() {
									$scope.selected = value;
								});
							};
						}
						for (var i = 0; i < value.length; i++) {
							var category = value[i].data.category[0].value; // pull out the category.
							value[i].marker = new google.maps.Marker({ 
								icon: {
									anchor: new google.maps.Point(11, 11),
									url: urls.images + (category == 'Site/Sub Plan' ? "/hammer.svg" : "/contract.svg"),
								},
								position: value[i].centroid, 
								zIndex: 10,
								map: map
							});
							value[i].listener = google.maps.event.addListener(value[i].marker, 'click', listen(value[i]));
						}
					} else {
						$scope.selected = value[0];
					}
				}
			});

			/*
			 * Watch the currently selected region. Mark it with a 
			 * pin.
			 */
			$scope.$watch('selected', function(value, old) {
				if (old && old.pin) {
					old.pin.setMap(null);
				}
				if (value) {
					value.pin = new google.maps.Marker({ 
						position: value.centroid, 
						zIndex: 100,
						map: map
					});
					
					$mdDrawer.show({
                                		templateUrl: urls.templates + '/material_list.html',
						scope: $scope.$new(false),
						parent: '#ui'
					}).then(null, function() {
						$scope.selected = null;
					});
				}
			});
		}
	};
}]);
