(function (){
    "use strict";
    
    angular.module('app.scip')
    .factory('Checkin',Checkin)

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
})();