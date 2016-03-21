(function (){
    'use strict';
    
    angular.module('app.scip')
    .factory('authInterceptor',authInterceptor)
    .factory('Login',Login)
    .factory('Users',Users)
    .factory('User',User)
    .factory('Checkin',Checkin)
    .factory('Workdays',Workdays);

    // If the token is set, we inject it with every request.
    // This requests interceptor is added in app.js -> config
    authInterceptor.$inject = ['$rootScope', '$q', '$window']; 
    function authInterceptor($rootScope, $q, $window)
    {
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
    };

    Login.$inject = ['$resource'];
    function Login($resource)
    {
        return $resource('/v1/auth/login/', {}, {
            post: { method:'POST', isArray: false, params:{} }
        });
    };


    Users.$inject =  ['$resource'];
    function Users($resource)
    {
        // implementa el servicio para obtener el listado de usuarios
        return $resource('/v1/users/', {}, {
            get: { params:{}, isArray:true}

        });
    };

    User.$inject = ['$resource'];
    function User($resource)
    {
        // implementa el servicio para obtener los datos de un usuario
        return $resource('/v1/users/:username/', {username:'@username'}, {
            get: { params:{}, isArray:false}
        });
    };

    Checkin.$inject = ['$resource'];
    function Checkin($resource)
    {
        // para crear un nuevo workday, dado el usuario (:username)
        // v1/users/:username/workdays
        // para hacer update de un workdate, dado el usuario (:username)
        // v1/users/{username}/workdays/last
        return $resource('/v1/users/:username/workdays/', {username:'@username'}, {
            checkin: {
                method:'POST',
                isArray: false,
                params: {}
            },
            checkout: {
                method:'PUT',
                url: '/v1/users/:username/workdays/last',
                isArray: false,
                //params: {user_notes: '@user_notes'},
                params: {}
            }
            
        });
    };

    Workdays.$inject = ['$resource'];
    function Workdays($resource)
    {
        return $resource('v1/users/:username/workdays', {}, {
            get: { params:{}, isArray:true}
        });

    };

})();
