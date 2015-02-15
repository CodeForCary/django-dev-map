(function() {
'use strict';

angular.module('mapapp.drawer', [
	'material.core',
	'material.components.backdrop'
])
	.directive('drawer', DrawerDirective)
	.provider('$drawer', DrawerProvider);

function DrawerDirective() {
	return {
		restrict: 'E'
	};
}

function DrawerProvider($$interimElementProvider) {

	return $$interimElementProvider('$drawer').setDefaults({
		options: defaults
	});

  	function defaults($animate, $mdConstant, $timeout, $compile, $mdTheming, $drawer) {
		var backdrop;

		return {
			themable: true,
			onShow: onShow,
			onRemove: onRemove
		};

		function onShow(scope, element, options) {
			backdrop = $compile('<md-backdrop class="md-opaque md-bottom-sheet-backdrop">')(scope);
			backdrop.on('click', function() {
				$timeout($drawer.cancel);
			});
			$mdTheming.inherit(backdrop, options.parent);
			$animate.enter(backdrop, options.parent, null);

			var drawer = new Drawer(element);
			options.element = drawer.element;
			options.drawer = drawer;

			return $animate.enter(drawer.element, options.parent)
				.then(function() {
					// do stuff
					drawer.open();
				});
		}

		function onRemove(scope, element, options) {
			var drawer = options.drawer;
			$animate.leave(backdrop);
			
			return $animate.leave(drawer.element).then(function() {
				drawer.cleanup();
			});
		}

		function Drawer(element) {
			// coercion incase $mdCompiler returns multiple elements
			var element = element.eq(0);
			var header = element.children()[0];

			//element.offsetHeight = header.offsetHeight;

			/*element.on('touchstart', onTouchStart)
				.on('touchmove', onTouchMove)
				.on('touchend', onTouchEnd);*/

			element.on('touchstart', onTouchStart)
			       .on('touchmove', onTouchMove);

			function setHeight(height) {
				element[0].style['height'] = height + 'px';
			}
			function getHeight() {
				return parseInt(element[0].style['height']);
			}
			
			function onTouchStart(e) {
				this.startHeight = getHeight();
			}

			function onTouchMove(e) {
				console.log(e);
				//var height = this.startHeight - e.pointer.distanceY;
				//setHeight(height);
			}

			return {
				element: element,
				cleanup: function cleanup() {
					element.off('touchstart', onTouchStart)
						.off('touchmove', onTouchMove)
						.off('touchend', onTouchEnd); },
				open: function() {
					setHeight(header.offsetHeight);
				}
			};

			/*function onTouchStart(e) {
			}

			function onTouchEnd(e) {
			}

			function onTouchMove(e) {
			}*/
		}

	}

}

})();
