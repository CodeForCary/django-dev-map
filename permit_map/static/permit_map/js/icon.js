/*
 * https://github.com/chrismatheson/ngMediaFilter
 * globals angular
 */
angular.module('iconFilter', [ 'django' ]).filter('icon', function(urls) {
	return function(name, unchanged) {
		return urls.icons + unchanged + '/svg/ic_' + name +'_24px.svg';
	};
});
