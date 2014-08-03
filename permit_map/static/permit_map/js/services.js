/**
 * Services for our Angular application. These pull AJAX data across the wire.
 */
angular.module('mapapp.services', [ 'django' ])
	/**
	 * Full text search service. Passes query strings to django and gets
	 * back JSON objects representing different permits.
	 */
	.service('search', [ '$http', '$q', 'urls', function($http, $q, urls) {
		function text_search(query) {
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
