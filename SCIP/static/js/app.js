(function (){
    "use strict";

    angular.module('posmaSCIP', [
        'angular-jwt', 
        'app.scip'
    ])


    .run(['$rootScope', '$window', '$location', function($rootScope, $window, $location){
        if ($window.sessionStorage.token){
            $rootScope.logged = true;
            $rootScope.is_staff = JSON.parse($window.sessionStorage.user).is_staff;
        }else{
            $rootScope.logged = false;
            $rootScope.is_staff = false;
        }

        // se configura una función para cerrar sesión.
        $rootScope.logout = function() { 
                delete $window.sessionStorage.token;
                $rootScope.logged = false;
                $rootScope.is_staff = false;
                $location.path('/login');
        };
    
    }]);

})();
