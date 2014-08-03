angular.module('mapapp.controllers', [ 'mapapp.services', 'ngSanitize' ])
        .controller('MapRender', function($scope, $http, $location, $anchorScroll, search, geojson, permits) {
		/**
		 * Initialize the Google map.
		 */
		function map_init() {
			var map = new google.maps.Map(document.getElementById("map"), {
				disableDefaultUI: true,
				zoomControl: true,
				zoom: 15 
			});
			if(navigator.geolocation) {
				navigator.geolocation.getCurrentPosition(function(position) {
					var pos = new google.maps.LatLng(position.coords.latitude,
						position.coords.longitude);
					map.setCenter(pos);
				}, function() {
					console.log('Could not locate.');
				});
			}
			$scope.map = map;

			/*
			 * Add a click listener from our scope object.
			 */
			map.data.addListener('click', function(event) {
				var lat = event.latLng.lat();
				var lon = event.latLng.lng();
				$scope.$apply(function() {
					permits.at(lat, lon).then(function(data) {
						$scope.query = ""; // clear search
						$scope.list.open(data);
						if (data.length > 0) {
							$scope.list.select(data[0]);
						}
					});
				});
			});

			/*
			 * Now that we have a map, populate it with geoJSON
			 */
			geojson.fetch().then(function(data) {
				map.data.addGeoJson(data);
			});
		};

		/**
		 * This should really be an Angular directive, but for the 
		 * moment I don't feel like figuring out how that works. 
		 * This little stateful object manages the search/click 
		 * results view.
		 */
		$scope.list = {
			clear: function(data) {
				for (var i = 0; i < $scope.list.permits.length; i++) {
					var permit = $scope.list.permits[i];
					google.maps.event.clearListeners($scope.map, permit.mapListener);
					permit.marker.setMap(null);
				}
				$scope.list.clearSelected();
				$scope.list.permits = [];
			},
			open: function(data) {
				$scope.list.clear(); // clear the list so we can populate it
				for (var i = 0; i < data.length; i++) {
					// Figure out the lat/lng of the center of our region (according to django)
					var latlng = new google.maps.LatLng(data[i].centroid[0],
							data[i].centroid[1]);
					// Add a marker to our map at the centroid
					data[i].marker = new google.maps.Marker({
						position: latlng,
						map: $scope.map
					});
					var closure_data = data[i];
					data[i].mapListener = google.maps.event.addListener(data[i].marker, 'click', 
						$scope.list.makeMarkerListener(data[i]));
					// Link our entry to the Map region
					data[i].region = $scope.map.data.getFeatureById(data[i].id);
					data[i].selected = false;
				}
				$scope.list.permits = data;
				$scope.list.visible = true;
			},
			close: function() {
				$scope.list.visible = false;
				$scope.list.clear();
			},
			select: function(data) {
				$scope.list.clearSelected(); // clear selection if any
				$scope.map.panTo(data.marker.getPosition());
				$scope.list.selected = data;
				data.selected = true;

				$location.hash(data.id);
				$anchorScroll();
			},
			clearSelected: function() {
				if ($scope.list.selected != null) {
					$scope.list.selected.selected = false;
					$scope.list.selected = null;
				}
			},
			makeMarkerListener: function(data) {
				return function() {
					$scope.$apply(function() {
						$scope.list.select(data);
					});
				}
			},
			selected: null,
			visible: false,
			permits: []
		};

		/**
		 * Search for the contents of the query box. Once the query is 
		 * complete, populate the query_result field.
		 */
		$scope.search = function() {
			if ($scope.query != "") {
				search.text($scope.query).then(function(data) {
					$scope.list.open(data);
				});
			} else {
				$scope.search_results = null;
			}
		};


		map_init();
        });
