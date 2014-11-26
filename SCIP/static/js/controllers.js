var scipControllers = angular.module('scipControllers', ['ngResource']);

scipControllers.controller('MainController', function($scope, $route, $routeParams, $location){
    console.log($routeParams);
    console.log("inicio?");

});

scipControllers.controller('LoginController', ['$scope', 'Login', function($scope, Login){
    console.log("En LoginController");
    $scope.submitForm = function() {

        console.log("Se hizo click en el submit del formulario de login");

        Login.post(
                {username:$scope.username, password:$scope.password},
                function(data){
                    console.log(data);
                }, 
                function(data){
                    console.log("hubo peo");
                });
    }
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
}]);


scipControllers.controller('WorkdayListController', ['$scope', 'Workdays', function($scope, Workdays){
    // De momento se cablea una estructura de jornadas de trabajo, en un futuro será obtenida desde el servicio.
    data = Workdays.get({username:'cbruguera'});
    $scope.username = 'cbruguera';
    $scope.workdays = data;
    console.log("En WorkdayListController");
}]);



