(function (){
    "use strict";
    
    angular.module('app.scip')
    .factory('Users',Users)

    Users.$inject =  ['$resource'];
    function Users($resource)
    {
        // implementa el servicio para obtener el listado de usuarios
        return $resource('/v1/users/', {}, {
            get: { params:{}, isArray:true}

        });
    };
})();