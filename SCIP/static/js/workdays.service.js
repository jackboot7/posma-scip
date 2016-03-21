(function (){
    "use strict";
    
    angular.module('app.scip')
    .factory('Workdays',Workdays);

    Workdays.$inject = ['$resource'];
    function Workdays($resource)
    {
        return $resource('v1/users/:username/workdays', {}, {
            get: { params:{}, isArray:true}
        });

    };
})();
