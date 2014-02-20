
/*
*	user services
*/
fmApp.factory('User', ['$resource', 
	function($resource) {
		return $resource('/api/user/:arg',
			{arg: '@arg'},
			{
				query: {method: 'get', isArray: true},
			 	login: {method: 'post', isArray: false}
			}
		);
	}
]);


/*
*	music services
*/
fmApp.factory('Music', ['$resource', 
	function($resource) {
		return $resource('/api/music/', 
			{},
			{query: {method: 'get', isArray: true}
		});
	}
]);


/*
*	channel services
*/
fmApp.factory('Channel', ['$resource', 
	function($resource) {
		return $resource('/api/channel/', 
			{},
			{query: {method: 'get', isArray: true}
		});
	}
]);