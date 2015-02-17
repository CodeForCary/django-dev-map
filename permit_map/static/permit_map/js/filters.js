angular.module('mapapp.directives', [])
.filter('cat_text', function() {
	return function(input) {
		if (input === 'subplan') {
			return 'site plan';
		} else if (input === 'rezone') {
			return 'rezoning case';
		}
	}
})
.filter('cat_color', function() {
	return function(input) {
		if (input === 'subplan') {
			return '#A94629';
		} else if (input === 'rezone') {
			return '#A3B489';
		}
	}
})
;
