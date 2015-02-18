/*
 * Provides the main logic for our UI.
 */
angular.module('mapapp.controllers', [ 'django', 'mapapp.services', 'mapapp.drawer', 'ngMaterial' ])
.controller('Map', function($scope, mapdata, permits, model, urls, $mdSidenav, $location, $mdBottomSheet, $mdDrawer, $mdDialog) {
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

	/*
	 * Poorly named object for interop with the gmap directive.
	 * Most of this should likely be moved to some sort of 
	 * service.
	 */
	$scope.container = {
		listener: {
			onDrawerClose: function() {
				$scope.drawerOpen = false;
			},
			onDrawerOpen: function() {
				$scope.drawerOpen = true;
			}
		},
		selected: null,
		bounds: null,
		list: [],
	};
	/*
	 * This 'should' be in a service as well. Called by
	 * the 'back' button to exit the drawer.
	 */
	$scope.closeDrawer = function() {
		$scope.container.listener.clearSelected();
	};


	/*
	 * Clear search results and the list.
	 */
	$scope.clearSearch = function() {
		$scope.model.query = '';
		$scope.container.selected = null;
		$scope.container.bounds = null;
		$scope.container.list = [];
	};

	$scope.about = function(ev) {
		$mdDialog.show({
			templateUrl: urls.templates + '/about.html',
			controller: DialogController,
			targetEvent: ev
		});
	};
	$scope.download = function(ev) {
		$mdDialog.show({
			templateUrl: urls.templates + '/download.html',
			controller: DialogController,
			targetEvent: ev
		});
	};

})
;

function DialogController($scope, $mdDialog, urls) {

	$scope.geoJson = urls.permits_all;

	$scope.hide = function() {
		$mdDialog.hide();
	};
}
