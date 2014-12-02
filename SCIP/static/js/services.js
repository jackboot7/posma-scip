var scipServices = angular.module('scipServices', ['ngResource']);


// If the token is set, we inject it with every request.
// This requests interceptor is added in app.js -> config
scipServices.factory('authInterceptor', function($rootScope, $q, $window){
    return {
        request: function(config) {
            config.headers = config.headers || {};
            if ($window.sessionStorage.token) {
                config.headers.Authorization = 'JWT ' + $window.sessionStorage.token;
            }
            return config;
        },
        response: function(response) {
            if (response == 401) {
                // We show a message for unauthorized user.
            }
            return response ||  $q.when(response);
        }
    };
});

scipServices.factory('Login', ['$resource', function($resource){
    return $resource('/v1/auth/login/', {}, {
        post: { method:'POST', isArray: false, params:{} }
    });
}]);


scipServices.factory('Users', ['$resource', function($resource){
    // implementa el servicio para obtener el listado de usuarios
    return $resource('/v1/users/', {}, {
        get: { params:{}, isArray:true}

    });
}]);

scipServices.factory('User', ['$resource', function($resource){
    // implementa el servicio para obtener los datos de un usuario
    return $resource('/v1/users/:username/', {username:'@username'}, {
        get: { params:{}, isArray:false}
    });
}]);

scipServices.factory('Checkin', ['$resource', function($resource){
    // para crear un nuevo workday, dado el usuario (:username)
    // v1/users/:username/workdays
    // para hacer update de un workdate, dado el usuario (:username)
    // v1/users/{username}/workdays/last
    return $resource('/v1/users/:username/workdays', {username:'@username'}, {
        checkin: {
            method:'POST',
            isArray: false,
            params: {},
        },
        checkout: {
            method:'PUT',
            url: '/v1/users/:username/workdays/last',
            isArray: false,
            params: {},
        }
        
    });
}]);

scipServices.factory('Workdays', ['$resource', function($resource){
    // implementa el servicio para obtener el listado de workdays
    return $resource('v1/workdays/', {}, {
        get: { params:{}, isArray:true}
    });
}]);
