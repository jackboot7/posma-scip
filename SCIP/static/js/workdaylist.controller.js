(function (){
    "use strict";

    angular.module('app.scip')
    .controller('WorkdayListController',WorkdayListController)

    WorkdayListController.$inject = ['$scope', '$rootScope', '$location', '$routeParams', '$window', 'Workdays']; 
    function WorkdayListController($scope, $rootScope, $location, $routeParams, $window, Workdays)
    {
            
        if (!$rootScope.logged){
            $location.path('/login');
        }
            
        $scope.username = ($routeParams.username)? $routeParams.username : angular.fromJson($window.sessionStorage.user).username;
        Workdays.get({username: $scope.username},
                function(data){
                    $scope.workdays = data;
                },
                function(data){
                    console.log("Problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
                });
    };

})();