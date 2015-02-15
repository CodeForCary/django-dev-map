/**
 * Services for our Angular application. These pull AJAX data across the wire.
 *
 * TODO: Horrible error handling in here. Would be aided by moving to a single 
 * service object, since they could share error handling code.
 *
 * Notice the declared dependency on 'django', which is an object that contains
 * all of the AJAX urls we have exposed to our Angular app. See:
 * permit_map/templates/index.html to see how this is established.
 */
angular.module('mapapp.services', [ 'django' ])
.service('gis', [ '$q', function($q) {
	function locate() {
		var future = $q.defer();

		if(navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(function(position) {
				future.resolve(position);
			}, function() {
				future.reject();
			});
		} else {
			future.reject();
		}

		return future.promise;
	}
	function toLatLng(arr) {
		return new google.maps.LatLng(arr[0], arr[1]);
	}
	return {
		toLatLng: toLatLng,
		locate: locate
	};
}])
.service('permits', [ '$http', '$q', 'urls', 'gis', function($http, $q, urls, gis) {
	function all() {
		var request = $http({
			url: urls.permits_all,
			method: 'GET'
		});
		return request.then(success, error);
	}
	function overview() {
		var future = $q.defer();
		function load(position) {
			var params = {};
			if (position) {
				params.lon = position.coords.longitude;
				params.lat = position.coords.latitude;
			}
			var request = $http({
				url: urls.permits_overview,
				params: params,
				method: 'GET'
			});
			request.then(function(response) {
				future.resolve(response.data);
			}, error);
		}
		gis.locate().then(load, load);
		return future.promise;
	}
	function search(query) {
		var future = $q.defer();
		var request = $http({
				url: urls.permits_search,
				params: { q: query },
				method: 'GET'
		});
		request.then(function(response) {
			future.resolve(decodeBundle(response.data));
		}, error);
		return future.promise;
	}
	function at(lat, lon) {
		var future = $q.defer();
		var request = $http({
			url: urls.permits_at,
			params: { 
				lat: lat, 
				lon: lon
			},
			method: 'GET'
		});
		request.then(function(response) {
			future.resolve(decodeBundle(response.data));
		}, error);
		return future.promise;
	}
	function colorOf(category) {
		if (category == 'Rezoning Case') {
			return '#A3B489';
		} else {
			return '#A94629';
		}
	}
	/*
	 * TODO: Error handling.
	 */
	function error(response) {
		return $q.reject(response.data);
	}
	function success(response) {
		return response.data;
	}
	/*
	 * Convert the bounds into a Google Maps object.
	 */
	function decodeBounds(bbox) {
		var swLatLng = new google.maps.LatLng(bbox[1], bbox[0]);
		var neLatLng = new google.maps.LatLng(bbox[3], bbox[2]);
		return new google.maps.LatLngBounds(swLatLng, neLatLng);
	}
	/*
	 * Convert a bundle of regions to the JS format.
	 */
	function decodeBundle(bundle) {
		bundle.bounds = decodeBounds(bundle.bounds);
		var permits = bundle.permits;
		for (var i = 0; i < permits.length; i++) {
			permits[i].centroid = gis.toLatLng(permits[i].centroid);
		}
		return bundle;
	}
	return {
		overview: overview,
		colorOf: colorOf,
		search: search,
		all: all,
		at: at
	};
}])
.service('model', [ '$q', 'permits', function($q, permits) {
	var shared_data = {
		filters: {
		}
	};
	var loaded = false;
	function load() {
		var future = $q.defer();
		if (loaded) {
			future.resolve(shared_data);
		} else {
			loaded = true;
			permits.overview().then(function(data) {
				/*
				 * Build up all of our filters
				 */
				var categories = [];
				for (i = 0; i < data.categories.length; i++) {
					categories.push({ name: data.categories[i], value: true });
				}
				var towns = [];
				for (i = 0; i < data.towns.length; i++) {
					towns.push({ name: data.towns[i], value: true });
				}
				shared_data.filters.categories = categories;
				shared_data.filters.towns = towns;

				// Return our shared objecct by resolving the promise
				future.resolve(shared_data);
			});
		}
		return future.promise;
	}
	function list(data) {
		shared_data.list = data;
	};
	return {
		list: list,
		load: load
	};
}]);
//.service('model', [ '$http', '$q', 'urls', 'permits', function($http, $q, urls, permits) {
//	var shared_data = {
//		listCache: {},
//		filters: {
//			display: false
//		}
//	};
//	//var colors = [ '#dc504f', '#e2ba74', '#79af7b', '#4b80b6', '#a267a7', '#139180' ];
//	var colors = [ '#242858', '#88C448', '#3299BB', '#FF9900', '#C7390B' ];
//	var color_cache = {};
//	var loaded = false;
//	function load() {
//		var future = $q.defer();
//		if (loaded) {
//			future.resolve(shared_data);
//		} else {
//			loaded = true; // we are attempting to load
//			permits.overview().then(function(data) {
//				/*shared_data.centroid = toLatLng(data.centroid);
//				var bbox = data.extent;
//				var swLatLng = new google.maps.LatLng(bbox[1], bbox[0]);
//				var neLatLng = new google.maps.LatLng(bbox[3], bbox[2]);
//				shared_data.extent = new google.maps.LatLngBounds(swLatLng, neLatLng);
//
//				data.closest.centroid = toLatLng(data.closest.centroid);
//				shared_data.selected = data.closest;*/
//
//				/*
//				 * Build up all of our filters
//				 */
//				var categories = [];
//				for (i = 0; i < data.categories.length; i++) {
//					categories.push({ name: data.categories[i], value: true });
//					color_cache[data.categories[i]] = colors[i];
//				}
//				var towns = [];
//				for (i = 0; i < data.towns.length; i++) {
//					towns.push({ name: data.towns[i], value: true });
//				}
//				var dateMaxEpoch = toMonth(data.dates[data.dates.length - 1]); //new Date(data.dates[data.dates.length - 1]).getTime();
//				var dateMinEpoch = toMonth(data.dates[0]); // new Date(data.dates[0]).getTime();
//
//				shared_data.filters.dateMaxEpoch = dateMaxEpoch;
//				shared_data.filters.dateMinEpoch = dateMinEpoch;
//				shared_data.filters.categories = categories;
//				shared_data.filters.dateMax = dateMaxEpoch;
//				shared_data.filters.dateMin = dateMinEpoch;
//				shared_data.filters.towns = towns;
//
//				setList(data.closest);
////				if (shared_data.list.permits.length > 0) {
////					shared_data.selected = shared_data.list.permits[0];
////				}
//
//				shared_data.colorOf = function(category) {
//					return color_cache[category];
//				}
//
//				// Pass data to the caller.
//				future.resolve(shared_data);
//			});
//		}
//		return future.promise;
//	}
//	function toMonth(string) {
//		var date = new Date(string);
//		return new Date(date.getFullYear(), date.getMonth()).getTime();
//	}
//	function toLatLng(arr) {
//		return new google.maps.LatLng(arr[0], arr[1]);
//	}
//	function setSelected(obj) {
//		shared_data.selected = obj;
//	}
//	function setList(obj) {
//		if (obj.permits) { /* && obj.permits.length > 0) {*/
//			shared_data.listCache = {};
//
//			var bbox = obj.bounds;
//			if (bbox && bbox.length == 4) {
//				var swLatLng = new google.maps.LatLng(bbox[1], bbox[0]);
//				var neLatLng = new google.maps.LatLng(bbox[3], bbox[2]);
//				obj.bounds = new google.maps.LatLngBounds(swLatLng, neLatLng);
//			} else {
//				obj.bounds = null;
//			}
//
//			/*
//			 * Do we need to convert all these dates? Let's wait until 
//			 * there's a need in the UI...
//			 *
//			 * If you do...factor it out so it can be used everywhere.
//			 */
//			for (var i = 0; i < obj.permits.length; i++) {
//				obj.permits[i].centroid = toLatLng(obj.permits[i].centroid);
//				shared_data.listCache[obj.permits[i].id] = obj.permits[i];
//			}
//
//			if (obj.permits.length > 0) {
//				shared_data.selected = obj.permits[0];
//			} else {
//				shared_data.selected = null;
//			}
//			
//			shared_data.list = obj;
//		}
//	}
//	return {
//		setSelected: setSelected,
//		toLatLng: toLatLng,
//		toMonth: toMonth,
//		setList: setList,
//		load: load
//	}
//}]);
