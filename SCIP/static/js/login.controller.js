(function (){
    "use strict";

    angular.module('app.scip')
    .controller('LoginController',LoginController)

    LoginController.$inject = ['$scope', '$window', '$rootScope', '$location', 'Login', 'User', 'jwtHelper'];
    function LoginController($scope, $window, $rootScope, $location, Login, User, jwtHelper)
    {

        $scope.login = function() {
            Login.post(
                    {username:$scope.username, password:$scope.password},

                    function(data){
                        var user_obj = jwtHelper.decodeToken(data.token)
                        $window.sessionStorage.token = data.token;
                        $window.sessionStorage.user = JSON.stringify(user_obj);
                        $rootScope.logged = true;
                        $rootScope.is_staff = user_obj.is_staff;
                        $location.path('/');
                    }, 

                    function(data){
                        console.log("Problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
                        delete $window.sessionStorage.token;
                        delete $window.sessionStorage.user;
                        $rootScope.logged = false;
                        $rootScope.is_staff = false;
                    });
        }
    };

})();
