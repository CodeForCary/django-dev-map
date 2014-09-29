/*
 * https://github.com/chrismatheson/ngMediaFilter
 * globals angular
 */
angular.module('mediaFilter', []).filter('media', [ '$window', function($window) {
	var rules = {
		sm: "(min-width: 35.5em)",
		md: "(min-width: 48em)",
		lg: "(min-width: 64em)",
		xl: "(min-width: 80em)"
	};
	return function(unchanged, rule, matchValue) {
		var mediaQueryString = rules[rule];
		var value = unchanged;
		if ($window.matchMedia(mediaQueryString).matches) {
			value = matchValue;
		}
		return value;
	};
}]);
