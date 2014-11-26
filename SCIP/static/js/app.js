"use strict";

var posmaSCIP = angular.module('posmaSCIP', ['ngRoute', 'scipServices', 'scipControllers']);

//posmaSCIP.config(['$httpProvider',
//        function($httpProvider) {
//            //Enable cross domain calls
//            $httpProvider.defaults.useXDomain = true;
//            delete $httpProvider.defaults.headers.common['X-Requested-With'];
//        }]);

posmaSCIP.config(['$routeProvider','$locationProvider',
    function($routeProvider, $locationProvider){
        $routeProvider.
            when('/login', {
                templateUrl: '/_partials/login',
                controller: 'LoginController'
            }).
            when('/logout', {
                templateUrl: '/_partials/hello',
                controller: 'LoginController'
            }).
            when('/checkin', {
                templateUrl: '/_partials/checkin',
                controller: 'CheckinController'
            }).
            when('/users/', {
                templateUrl: '/_partials/users',
                controller: 'UserListController'
            }).
            when('/workdays', {
                templateUrl: '/_partials/workdays',
                controller: 'WorkdayListController'
            }).
            otherwise({
                templateUrl: '/_partials/hello',
                controller: 'MainController'
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
            $httpProvider.interceptors.push('authInterceptor');
        }]);

posmaSCIP.config(['$rootScope',
        function ($rootScope){
            if (!$rootScope.is_logged){
                $rootScope.is_logged = false;
            }
        }]);
