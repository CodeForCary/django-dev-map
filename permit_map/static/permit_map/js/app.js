/*
 * This is our main Angular application, defined in the module format 
 * encouraged by the ionic framework. Our application currently has a
 * single view 'render' which shows the map.
 *
 * Note the list of dependencies here:
 * - mgcrea.ngStrap -- May be removed, not adding much benefit. This is a UI
 *   library: http://mgcrea.github.io/angular-strap/
 * - mapapp.controllers -- The controllers defined in controllers.js. This is
 *   part of our permit UI.
 * - ui.router -- The defacto standard of Angular UI routing. It is what 
 *   provides the '$stateProvider'. See: https://github.com/angular-ui/ui-router
 * - django -- This is an important module. It defines all of the URL routes 
 *   exposed by our django application to this Angular app. See 
 *   permit_map/templates/base.html to see where this comes from. It provides 
 *   the 'url' object within the config.
 */
angular.module('mapapp', [ 'mapapp.controllers', 'mapapp.directives', 'ui.router', 'django', 'ui-rangeSlider', 'ngAnimate', 'mediaFilter' ])
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
	});
