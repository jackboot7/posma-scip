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
                    console.log($scope.users);
                },
                function(data){
                    console.log(data);
                    console.log("Problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
                });

        $scope.getClass = function(user){
            var current_date = new Date();
            var date = new Date(user.last_workday.start);
            if (date < current_date.setHours(0,0,0,0)){
                return { nochecked: true };
            }
        }

        $scope.showStart = function(user){
            if (user.last_workday.finish == null){
                return true;
            }
        }

        $scope.showFinish = function(user){
            return !$scope.showStart(user);
        }
    };

})();
