(function (){
    "use strict";

    angular.module('app.scip')
    .controller('UserListController',UserListController)

    UserListController.$inject = ['$scope', '$rootScope', '$location', '$window', 'Users'];
    function UserListController($scope, $rootScope, $location, $window, Users)
    {

        if (!$rootScope.logged){
            $location.path('/login');
        }
        if (!angular.fromJson($window.sessionStorage.user).is_staff) {
            $location.path('/404');
        }

        $scope.predicate = '-last_workday.start';

        // La conexión con el API se hace sólo para usuarios loggeados.
        Users.get(
                function(data){
                    $scope.users = data;
                },
                function(data){
                    console.log(data);
                    console.log("Problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
                });

        $scope.getClass = function(user){
            var current_date = Date();
            if (user.last_workday.start < current_date){
                return { nochecked: true };
            }
        }
    };

})();
