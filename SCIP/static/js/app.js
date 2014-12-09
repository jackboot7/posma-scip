"use strict";

var posmaSCIP = angular.module('posmaSCIP', ['ngRoute', 'angular-jwt', 'scipServices', 'scipControllers']);

posmaSCIP.config(['$routeProvider','$locationProvider',
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

posmaSCIP.config(['$resourceProvider', 
        function($resourceProvider) {
            // Don't strip trailing slashes from calculated URLs
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }]);

posmaSCIP.config(['$httpProvider',
        function ($httpProvider){
            // Inyecta el token en todos los headers enviados al servidor.
            $httpProvider.interceptors.push('authInterceptor');
        }]);

posmaSCIP.run(['$rootScope', '$window', '$location', function($rootScope, $window, $location){
    if ($window.sessionStorage.token){
        $rootScope.logged = true;
    }else{
        $rootScope.logged = false;
    }

    // se configura una función para cerrar sesión.
    $rootScope.logout = function() { 
            delete $window.sessionStorage.token;
            $rootScope.logged = false;
            $location.path('/login');
        };
}]);



