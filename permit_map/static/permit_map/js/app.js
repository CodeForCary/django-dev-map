/*
 * This is our main Angular application, defined in the module format 
 * encouraged by the ionic framework. 
 */
angular.module('mapapp', [ 'mapapp.directives', 'mapapp.controllers', 'mapapp.gmap', 'ngMaterial', 'ui.router', 'django' ])
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
			;
			$mdThemingProvider.theme('default')
				.primaryPalette('green')
				.accentPalette('lime');

			// Default route
			$urlRouterProvider.otherwise('/map');
	});
