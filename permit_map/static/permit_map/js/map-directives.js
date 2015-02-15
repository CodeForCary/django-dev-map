angular.module('mapapp.directives', [ 'mapapp.services', 'django' ])
.directive('mapView', [ '$timeout', '$q', 'permits', 'mapdata', 'model', 'gis', 'urls', function($timeout, $q, permits, mapdata, model, gis, urls) {
	function is_enabled(name, filters) {
		enabled = false;
		for (var i = 0; i < filters.length; i++) {
			if (filters[i].name == name) {
				enabled = filters[i].value;
				break;
			}
		}
		return enabled;
	}
	return {
		transclude: true,
		restrict: 'E',
		scope: {
			binding: '='
		},
		link: function($scope, $element, $attrs) {
			var map = new google.maps.Map($element[0], {
				//disableDefaultUI: true,
				//zoomControl: true,
				zoom: 15
			});
			map.setCenter(mapdata.centroid);
			map.fitBounds(mapdata.extent);
			var youAreHere = null;

			permits.all().then(function(data) {
				var regions = map.data.addGeoJson(data);
				for (i = 0; i < regions.length; i++) {
					regions[i].setProperty('first_seen', model.toMonth(regions[i].getProperty('first_seen')));// new Date(regions[i].getProperty('first_seen')).getTime());
					regions[i].setProperty('last_seen', model.toMonth(regions[i].getProperty('last_seen'))); //new Date(regions[i].getProperty('last_seen')).getTime());
				}
				$scope.regions = regions;
			});

			var unwatch = $scope.$watch('binding.colorOf', function(val) {
				if (val) {
					map.data.setStyle(function(feature) {
						return {
							fillColor: $scope.binding.colorOf(feature.getProperty('category')),
							fillOpacity: 0.5
						};
					});
					map.data.addListener('click', function(event) {
						var lat = event.latLng.lat();
						var lon = event.latLng.lng();


						$scope.$apply(function() {
							var id = event.feature.getProperty('id');
							if (id in $scope.binding.listCache) {
								model.setSelected($scope.binding.listCache[id]);
							} else {
								permits.at(lat, lon).then(function(data) {
									model.setList(data);
								});
							}
						});
					});
					gis.locate().then(function(position) {
						var latlng = model.toLatLng([ position.coords.latitude, position.coords.longitude ]);
						youAreHere = new google.maps.Marker({ 
							icon: {
								scaledSize: new google.maps.Size(36, 43),
								url: urls.images + "/you_are_here.png"
							},
							position: latlng,
							map: map
						});
					});
					unwatch();
				}
			});

			$scope.$watch('binding.filters', function(f) {
				var r = $scope.regions; // make this easier to type
				if (r) { // is called initially with 'r' as null
					map.data.revertStyle(); // revert all overrides
					for (var i = 0; i < r.length; i++) {
						var first = r[i].getProperty('first_seen');
						var last = r[i].getProperty('last_seen');
						var id = r[i].getProperty('id');

						visible = is_enabled(r[i].getProperty('category'), f.categories) &&
							  is_enabled(r[i].getProperty('township'), f.towns) &&
							  ((first >= f.dateMin && first <= f.dateMax) ||
							   (last >= f.dateMin && last <= f.dateMax))
						if (!visible) {
							map.data.overrideStyle(r[i], { visible: false });
						}
						
						// Handle any marker visible for this entry.
						var listEntry = $scope.binding.listCache[id];
						if (listEntry && listEntry.marker) {
							listEntry.marker.setMap(visible ? map : null);
						}
					}
				}
			}, true);

			$scope.$watch('binding.list.bounds', function(b) {
				if (b) {
					map.setCenter(b.getCenter());
					google.maps.event.addListenerOnce(map, 'idle', function() {
						map.panToBounds(b); // animate pan and fit to bounds using this trick
					});
					google.maps.event.addListenerOnce(map, 'idle', function() {
						  map.fitBounds(b);
					});
				}
			});

			$scope.$watch('binding.list.permits', function(l, o) {
				if (o) {
					for (var i = 0; i < o.length; i++) {
						google.maps.event.removeListener(l[i].listener);
						o[i].marker.setMap(null);
					}
				}
				if (l) {
					function listen(permit) {
						return function() {
							$scope.$apply(function() {
								model.setSelected(permit);
							});
						};
					}
					for (var i = 0; i < l.length; i++) {
						l[i].marker = new google.maps.Marker({ 
							position: l[i].centroid, 
							map: map
						});
						l[i].listener = google.maps.event.addListener(l[i].marker, 'click', listen(l[i]));
					}
				}
			});

			/*$scope.$watch('binding.selected', function(f) {
				if (f) {
					map.panTo(f.centroid);
				}
			});*/
		}
	};
}])
.directive('mapSearch', [ '$q', 'permits', 'urls', 'model', function($q, permits, urls, model) {
	var controller = {
	};
	return {
		templateUrl: urls.templates + 'search-box.html',
		transclude: true,
		restrict: 'E',
		scope: {
			binding: '='
		},
		link: function($scope, $element, $attrs) {
			$scope.search = function() {
				permits.search($scope.query).then(model.setList);
			};
		}
	};
}]);
