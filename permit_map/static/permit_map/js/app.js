angular.module('mapapp', [ 'mgcrea.ngStrap', 'mapapp.controllers', 'ui.router', 'django' ])
	.config(function($stateProvider, $urlRouterProvider, urls) {
		$stateProvider
                        .state('render', {
                                templateUrl: urls.templates + '/render.html',
                                controller: 'MapRender',
                                url: '/render'
                        });
			$urlRouterProvider.otherwise('/render');
	});
