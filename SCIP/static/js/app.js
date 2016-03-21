(function (){
    "use strict";

    angular.module('posmaSCIP', [
        'ngRoute', 
        'angular-jwt', 
        'scipServices', 
        'app.scip'
    ]);

    .config(['$routeProvider','$locationProvider',
        function($routeProvider, $locationProvider){
            $routeProvider.
                when('/', {
                    templateUrl: '/_partials/checkin',
                    controller: 'CheckinController'
                }).
                when('/checkin', {
                    templateUrl: '/_partials/checkin',
                    controller: 'CheckinController'
                }).
                when('/login', {
                    templateUrl: '/_partials/login',
                    controller: 'LoginController'
                }).
                when('/users/', {
                    templateUrl: '/_partials/users',
                    controller: 'UserListController'
                }).
                when('/users/:username/', {
                    templateUrl: '/_partials/workdays',
                    controller: 'WorkdayListController'
                }).
                when('/workdays', {
                    templateUrl: '/_partials/workdays',
                    controller: 'WorkdayListController'
                }).
                otherwise({
                    templateUrl: '/_partials/404',
                    controller: '404Controller'
                });
                $locationProvider.html5Mode(true);
        }]);

    .config(['$resourceProvider', 
        function($resourceProvider) {
            // Don't strip trailing slashes from calculated URLs
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }]);

    .config(['$httpProvider',
        function ($httpProvider){
            // Inyecta el token en todos los headers enviados al servidor.
            $httpProvider.interceptors.push('authInterceptor');
        }]);

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
