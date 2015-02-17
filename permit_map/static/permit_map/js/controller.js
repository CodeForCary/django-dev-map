/*
 * Provides the main logic for our UI.
 */
angular.module('mapapp.controllers', [ 'django', 'mapapp.services', 'mapapp.drawer', 'ngMaterial' ])
.controller('Map', function($scope, mapdata, permits, model, urls, $mdSidenav, $location, $mdBottomSheet, $mdDrawer) {
	/*
	 * TODO: Move this to a directive
	 */
	/*var map = new google.maps.Map(document.getElementById('map'), {
		disableDefaultUI: true,
		zoom: 15
	});
	map.setCenter(mapdata.centroid);
	map.fitBounds(mapdata.extent);
	permits.all().then(function(data) {
		map.data.addGeoJson(data);
	});
	map.data.addListener('click', function(event) {
		var lat = event.latLng.lat();
		var lon = event.latLng.lng();
		$scope.$apply(function() {
			permits.at(lat, lon).then(function(data) {
				$scope.selected = data.permits;
			});
		});

	});*/

	/*
	 * Load the shared model data into our scope.
	 */
	model.load().then(function(data) {
		$scope.model = data;
	});

	/*
	 * Open the left menu when clicked.
	 */
	$scope.toggleMenu = function() {
		$mdSidenav('left').toggle();
	};

	/*
	 * Execute a search and store the result in the model
	 */
	$scope.search = function() {
		permits.search($scope.model.query).then(function(data) {
			$scope.container.bounds = data.bounds;
			$scope.container.list = data.permits;
			if (data.permits.length == 1) {
				$scope.container.selected = data.permits[0];
			}
		});
	};

	$scope.container = {
		selected: null,
		bounds: null,
		list: []
	};

	/*
	 * Clear search results and the list.
	 */
	$scope.clearSearch = function() {
		$scope.model.query = '';
		$scope.container = {
			selected: null,
			bounds: null,
			list: []
		};
	};

	/*$scope.openDrawer = function($event) {
		$mdBottomSheet.show({
   			template: '<md-bottom-sheet>Hello!</md-bottom-sheet>',
			targetEvent: $event,
			parent: '#ui'
		});
	};*/

	/*$scope.$watch('container.selected', function(value) {
		console.log(value);
		if (value) {
			var sheet = $mdBottomSheet.show({
				template: '<md-bottom-sheet>Hello!</md-bottom-sheet>'
			});
			console.log(sheet);
		} 
	});*/

	/*$scope.showList = function() {
		$location.path('/map/test');
	};

	$scope.list = {
		closeEl: '#close',
		overlay: {
			templateUrl: urls.templates + '/material_list.html'
		}
	};*/
})
;
