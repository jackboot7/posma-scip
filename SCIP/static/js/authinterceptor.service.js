(function (){
    "use strict";
    
    angular.module('app.scip')
    .factory('authInterceptor',authInterceptor)

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
})();
