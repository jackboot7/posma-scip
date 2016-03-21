/* Define routes and basic config. for the core module */

(function(){
    'use strict';

    angular
        .module("app.scip", ['ngRoute', 'ngResource'])

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
                        controller: 'Four04Controller'
                    });
                    $locationProvider.html5Mode(true);
                }])

    .config(['$resourceProvider', 
            function($resourceProvider) {
                // Don't strip trailing slashes from calculated URLs
                $resourceProvider.defaults.stripTrailingSlashes = false;
            }])

    .config(['$httpProvider',
            function ($httpProvider){
                // Inyecta el token en todos los headers enviados al servidor.
                $httpProvider.interceptors.push('authInterceptor');
            }])

})();
