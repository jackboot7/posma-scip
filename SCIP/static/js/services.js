var scipServices = angular.module('scipServices', ['ngResource']);

scipServices.factory('Users', ['$resource', function($resource){
        // implementa el servicio para obtener el listado de usuarios
        return $resource('/v1/users/', {}, {
            get: { params:{}, isArray:true}

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
}]);

scipServices.factory('Login', ['$resource', function($resource){
    return $resource('/v1/login/', {}, { });
}]);
