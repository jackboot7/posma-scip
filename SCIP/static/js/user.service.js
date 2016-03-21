(function (){
    "use strict";
    
    angular.module('app.scip')
    .factory('User',User)

    User.$inject = ['$resource'];
    function User($resource)
    {
        // implementa el servicio para obtener los datos de un usuario
        return $resource('/v1/users/:username/', {username:'@username'}, {
            get: { params:{}, isArray:false}
        });
    };
})();