/*
 * This is our main Angular application, defined in the module format 
 * encouraged by the ionic framework. 
 */
/*angular.module('mapapp', [ 'mapapp.controllers', 'mapapp.directives', 'ui.router', 'django', 'ui-rangeSlider', 'ngAnimate', 'mediaFilter' ])
	.config(function($stateProvider, $urlRouterProvider, urls) {
		$stateProvider
                        .state('map', {
				// Map to the render.html template in our STATIC directory
                                templateUrl: urls.templates + '/map.html',
				// Render with the MapRender controller (controllers.js)
                                controller: 'Map',
				// Use this URL
                                url: '/map'
                        })
                        .state('mobile', {
				// Map to the render.html template in our STATIC directory
                                templateUrl: urls.templates + '/mobile.html',
				// Render with the MapRender controller (controllers.js)
                                controller: 'Map',
				// Use this URL
                                url: '/mobile'
                        });
			// Map all requests not coming via Ajax to '/render'
			$urlRouterProvider.otherwise('/map');
	});*/
angular.module('mapapp', [ 'mapapp.directives', 'mapapp.controllers', 'mapapp.gmap', 'ngMaterial', 'ui.router', 'django', 'iconFilter' ])
	.config(function($stateProvider, $urlRouterProvider, urls, $mdThemingProvider) {
		$stateProvider
                        .state('map', {
				// Map to the render.html template in our STATIC directory
                                templateUrl: urls.templates + '/material_map.html',
				// Render with the MapRender controller (controllers.js)
                                controller: 'Map',
				// Use this URL
                                url: '/map'
                        })
			.state('list', {
                                templateUrl: urls.templates + '/material_list.html',
                                controller: 'List',
                                url: '/list'
			})
			.state('map.at', {
				url: '/map/:test',
				onEnter: function($stateParams, $state) {
					console.log('hello?');
					$state.transitionTo("map");
				}
			})
			;
			$mdThemingProvider.theme('default')
				.primaryPalette('green')
				.accentPalette('lime');
			//$urlRouterProvider.otherwise('/map');
	});
