var scipControllers = angular.module('scipControllers', ['ngResource']);

scipControllers.controller('MainController', function($scope, $route, $routeParams, $rootScope, $location){
    console.log($routeParams);
    console.log("inicio?");
    console.log($rootScope.is_logged);
    console.log($rootScope);
    console.log($location);

});

scipControllers.controller('LoginController', ['$scope', '$window', '$rootScope', '$location', 'Login', function($scope, $window, $rootScope, $location, Login){
    console.log("En LoginController");

    $scope.login = function() {
        Login.post(
                {username:$scope.username, password:$scope.password},
                function(data){
                    $window.sessionStorage.token = data.token;
                    console.log(data.token);
                    console.log(data);
                    $rootScope.is_logged = true;
                }, 
                function(data){
                    console.log("hubo peo");
                    delete $window.sessionStorage.token;
                    $rootScope.is_logged = false;
                });
    }
    
    $rootScope.logout = function() { 
            delete $window.sessionStorage.token;
            $location.path('/login');
            $rootScope.is_logged = false;
    };
    console.log($rootScope.is_logged);

}]);

scipControllers.controller('CheckinController', function($scope){
    console.log("En CheckinController");
    // Se obtienen los datos del usuario logueado actualmente
    // Users.get(username);
    // Para ese usuario logueado: 
    //     - si el usuario no ha hecho checkin, se muestra el botón y se usa Checkin.checkin()
    //     - si el usuario ya está trabajando, se muestra el segundo botón y se usa Checkin.checkout()
    //

});


scipControllers.controller('UserListController', ['$scope', 'Users', function($scope,  Users){
    Users.get(    
            function(data){
                // caso exitoso.
                $scope.users = data;
            },
            function(data){
                // callback de error.
                console.log("error?");
            });
    console.log($rootScope.is_logged);
}]);


scipControllers.controller('WorkdayListController', ['$scope', 'Workdays', function($scope, Workdays){
    // De momento se cablea una estructura de jornadas de trabajo, en un futuro será obtenida desde el servicio.
    data = Workdays.get({username:'cbruguera'});
    $scope.username = 'cbruguera';
    $scope.workdays = data;
    console.log("En WorkdayListController");
}]);



