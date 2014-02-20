/*
*	 module
*/
var fmApp = angular.module('FMApp', ['ngRoute', 'ngCookies', 'ngResource']);

function fmRouteConfig($routeProvider) {
	$routeProvider.
	when('/music', {
		templateUrl: '../views/partials/music.html'
	}).
	when('/manager', {
		templateUrl: '../views/partials/manager.html'
	}).
	otherwise({
		redirectTo: '/music'
	});
}

fmApp.config(['$routeProvider', fmRouteConfig]);

/*
*	directives
*/
fmApp.directive('navigator', function() {
	return {
		restrict: 'E',
		//scope: {name: '@helloTitle'},
		template: '<ul><li><a href="#" data-toggle="modal">注册</a></li> \
                    <li><a href="#" data-target="#login" data-toggle="modal">登录</a></li></ul>', 
		replace: true,
		// compile: function compile(telement, tAttrs, transclude) {
		// }
		link: function(scope, element, attrs) {
			//console.info(scope);
			var nav = $(element).children();
			// for(var item in scope.currentUser) {
			// 	console.info(item);
			// }
			console.info(scope.currentUser);
			//nav[0].innerHTML = scope.currentUser;
			// $(nav[1]).text('nta');
		}
	};
});