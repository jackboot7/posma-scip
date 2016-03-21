(function (){
    "use strict";
    
    angular.module('app.scip')
    .factory('Login',Login)

    Login.$inject = ['$resource'];
    function Login($resource)
    {
        return $resource('/v1/auth/login/', {}, {
            post: { method:'POST', isArray: false, params:{} }
        });
    };
})();