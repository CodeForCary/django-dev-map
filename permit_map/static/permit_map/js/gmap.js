angular.module('mapapp.gmap', [ 'mapapp.services', 'django', 'ngMaterial', 'mapapp.drawer', 'mapapp.directives' ])
.directive('map', [ 'gis', 'mapdata', 'permits', 'urls', '$mdBottomSheet', '$mdDrawer', '$filter', '$timeout', function(gis, mapdata, permits, urls, $mdBottomSheet, $mdDrawer, $filter, $timeout) {
	return {
		transclude: true,
		restrict: 'E',
		scope: {
			listener: '=',
			selected: '=',
			bounds: '=',
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
			var drawerOpen = false;

			var clearSelected = function() {
				if (drawerOpen) {
					var promise = $mdDrawer.hide();
					if (promise) {
						promise.then(function() {
							drawerOpen = false;
							$scope.selected = null;
							$scope.listener.onDrawerClose();
						});
					}
				} else {
					$scope.selected = null;
				}
			};
			$scope.listener.clearSelected = clearSelected;

			/*
			 * Should probably get this from the mdDrawer service. Would
			 * make more sense, no?
			 *
			 * Height of the drawer element. These are:
			 *  - Height of drawer, which TODO must vary with the
			 *    media query.
			 *  - MAX_OFFSET from drawer.js
			 */
			var drawerHeight = 500 - 80;

			var getVisibleBounds = function() {
				var scale = Math.pow(2, map.getZoom());
				var bounds = map.getBounds();
				if (drawerOpen) {
					/*
					 * If the drawer is open, we need to adjust the bounds of the
					 * map upwards to ensure that latlng isn't covered by the
					 * drawer UI.
					 *
					 * Adust the SW corder of the bounds upwards by yOffset.
					 */
					var swInPixels = map.getProjection().fromLatLngToPoint(bounds.getSouthWest());
					var swAdjusted = new google.maps.Point(
						swInPixels.x,
						swInPixels.y - ((drawerHeight / scale) || 0)
					);

					// Patch our bounds object
					bounds = new google.maps.LatLngBounds(
						map.getProjection().fromPointToLatLng(swAdjusted),
						bounds.getNorthEast()
					);
				}
				return bounds;
			}
			
			var showLatLng = function(latlng) {
				var scale = Math.pow(2, map.getZoom());
				var bounds = getVisibleBounds();
				if (!bounds.contains(latlng)) {
					if (drawerOpen) {
						/*
						 * The height of the map UI minus the height of the
						 * 'action bar'. We should probably get the action 
						 * bar height from somewhere ... ?
						 */
						var uiHeight = $element[0].offsetHeight - 86;

						/*
						 * Calculate distance from center of UI to center of space above drawer.
						 */
						var yOffset = (uiHeight / 2.0) - ((uiHeight - drawerHeight) / 2.0);
						var llInPixels = map.getProjection().fromLatLngToPoint(latlng);
						/*
						 * Adjust our center upward.
						 */
						var llAdjusted = new google.maps.Point(
							llInPixels.x,
							llInPixels.y + ((yOffset / scale) || 0)
						);
						latlng = map.getProjection().fromPointToLatLng(llAdjusted);
					}
					map.panTo(latlng);
				}
			};

			google.maps.event.addListener(map, 'click', function() {
				$scope.$apply(function() {
					clearSelected();
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

			/*$scope.$watch('bounds', function(value) {
				if (value) {
					var visible = getVisibleBounds();
					if (!visible.equals(visible.union(value))) {
						map.fitBounds(value);
					}
				}
			});*/

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
						clearSelected();
						function listen(value) {
							return function() {
								$scope.$apply(function() {
									$scope.selected = value;
								});
							};
						}
						var visible = getVisibleBounds();
						var containsAll = true;
						for (var i = 0; i < value.length; i++) {
							var category = value[i].category; // pull out the category.
							value[i].marker = new google.maps.Marker({ 
								icon: {
									anchor: new google.maps.Point(11, 11),
									url: urls.images + (category == 'subplan' ? "/hammer.svg" : "/contract.svg"),
								},
								position: value[i].centroid, 
								zIndex: 10,
								map: map
							});
							value[i].listener = google.maps.event.addListener(value[i].marker, 'click', listen(value[i]));
							if (!visible.contains(value[i].centroid)) {
								containsAll = false;
								visible.extend(value[i].centroid);
							}
						}
						if (!containsAll) {
							map.fitBounds(visible);
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
					
					if (!drawerOpen) {
						$mdDrawer.show({
							templateUrl: urls.templates + '/material_list.html',
							scope: $scope.$new(false),
							parent: '#ui'
						}).then(null, function() {
							drawerOpen = false;
							$scope.listener.onDrawerClose();
						});
						drawerOpen = true;
						showLatLng(value.centroid);
						$scope.listener.onDrawerOpen();
					}
				}
			});
		}
	};
}]);
