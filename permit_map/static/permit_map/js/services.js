/**
 * Services for our Angular application. These pull AJAX data across the wire.
 *
 * TODO: If we stick with Angular, this should really be refactored into a 
 * single service with multiple methods:
 *  - permits.search
 *  - permits.all
 *  - permits.at
 *
 * TODO: Horrible error handling in here. Would be aided by moving to a single 
 * service object, since they could share error handling code.
 *
 * Notice the declared dependency on 'django', which is an object that contains
 * all of the AJAX urls we have exposed to our Angular app. See:
 * permit_map/templates/index.html to see how this is established.
 */
angular.module('mapapp.services', [ 'django' ])
	/**
	 * Full text search service. Passes query strings to django and gets
	 * back JSON objects representing different permits.
	 */
	.service('search', [ '$http', '$q', 'urls', function($http, $q, urls) {
		function text_search(query) {
			// AJAX: /search?q=<<query>>
			var request = $http({
				url: urls.search,
				method: "GET",
				params: {
					q: query
				}
			});
			return request.then(success, error);
		}
		function error(response) {
			return $q.reject(response.data);
		}
		function success(response) {
			return response.data;
		}
		return {
			text: text_search
		};
	}])
	/**
	 * geoJSON service. Pulls the full geoJSON document from django.
	 */
	.service('geojson', [ '$http', '$q', 'urls', function($http, $q, urls) {
		function geojson() {
			// AJAX: /permits/geojson
			var request = $http({
				url: urls.permits_geojson,
				method: "GET"
			});
			return request.then(success, error);
		}
		function error(response) {
			return $q.reject(response.data);
		}
		function success(response) {
			return response.data;
		}
		return {
			fetch: geojson
		}
	}])
	/**
	 * Find all permits at the given lat/lon using django service.
	 */
	.service('permits', [ '$http', '$q', 'urls', function($http, $q, urls) {
		function permitsat(lat, lon) {
			// AJAX: /permitsat?lat=<<lat>>&lon=<<lon>>
			var request = $http({
				url: urls.permitsat,
				method: "GET",
				params: {
					lat: lat,
					lon: lon
				}
			});
			return request.then(success, error);
		}
		function error(response) {
			return $q.reject(response.data);
		}
		function success(response) {
			return response.data;
		}
		return {
			at: permitsat
		}
	}])
