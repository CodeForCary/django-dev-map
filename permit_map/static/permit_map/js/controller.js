/*
 * Provides the main logic for our UI.
 */
angular.module('mapapp.controllers', [ 'mapapp.services' ])
	/*
	 * This code will get executed when our application is initialized (see app.js). 
	 *
	 * Note that we have a declared dependency on 'mapapp.services', which is defined in services.js and 
	 * gives us access to django over AJAX.
	 */
        .controller('Map', function($scope, $timeout, permits, model) {
		$scope.filters = { display: false }; // set to empty object on page init
		model.load().then(function(data) {
			$scope.model = data;
		});
		$scope.colorOf = permits.colorOf;
		permits.search('towne').then(function(xxx) {
			console.log(xxx);
		});
//		permits.overview().then(function(data) {
//			// convert the list of categories into a map we can filter onto
//			data.cat_sel = {};
//			for (i = 0; i < data.categories.length; i++) {
//				data.cat_sel[data.categories[i]] = true;
//			}
//			// do the same thing with our townships
//			data.town_sel = {};
//			for (i = 0; i < data.towns.length; i++) {
//				data.town_sel[data.towns[i]] = true;
//			}
//
//			// dates come back from the server as strings -- the slider needs numbers
//			data.dateMaxEpoch = data.dates[data.dates.length - 1].getTime();
//			data.dateMinEpoch = data.dates[0].getTime();
//			data.dateMax = data.dateMaxEpoch;
//			data.dateMin = data.dateMinEpoch;
//
//			/*
//			 * Inject all this data into the scope. We'll now use 
//			 * this data to drive the search results and map 
//			 * filtering.
//			 */
//			$scope.filters = data;
//		});
	});
