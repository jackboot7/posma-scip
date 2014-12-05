var scipControllers = angular.module('scipControllers', ['ngResource']);

scipControllers.controller('404Controller', function($scope, $window, $route, $routeParams, $rootScope, $location){
    console.log("404 Página no existente!");
    console.log($routeParams);
    console.log($rootScope.logged);
    console.log($rootScope);
    console.log($location);
    if($window.sessionStorage.token){
       // console.log("este es el token: " + $window.sessionStorage.token);
    }else{
        console.log("no tiene token!");
    }

});

scipControllers.controller('LoginController', ['$scope', '$window', '$rootScope', '$location', 'Login', 'User', function($scope, $window, $rootScope, $location, Login, User){
    console.log("En LoginController");

    $scope.login = function() {
        Login.post(
                {username:$scope.username, password:$scope.password},

                function(data){
                    $window.sessionStorage.token = data.token;
                    User.get(
                        {username:$scope.username},

                        function(data){
                            //$window.sessionStorage.user = JSON.stringify(data);
                            //console.log(JSON.stringify(data));
                            $window.sessionStorage.user = JSON.stringify(data);
                        },
                        function(data){
                            console.log("problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
                            delete $window.sessionStorage.token;
                            delete $window.sessionStorage.user;
                            $rootScope.logged = false;
                        });

                    $rootScope.logged = true;
                    $location.path('/');

                }, 

                function(data){
                    console.log("problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
                    delete $window.sessionStorage.token;
                    delete $window.sessionStorage.user;
                    $rootScope.logged = false;
                    // problema con la conexión con el API. 
                    // Mostrar mensaje de error y redireccionar.
                });
    }

}]);

scipControllers.controller('CheckinController',['$scope', '$rootScope', '$location', '$window', function($scope, $rootScope, $location, $window){
    console.log("En CheckinController");
    if(!$rootScope.logged){
        $location.path('/login');
    }
    console.log($window.sessionStorage.user);
    $scope.user = angular.fromJson($window.sessionStorage.user);
    console.log("hola " + $scope.user['username']);
    
    // Se obtienen los datos del usuario logueado actualmente
    // Users.get(username);
    // Para ese usuario logueado: 
    //     - si el usuario no ha hecho checkin, se muestra el botón y se usa Checkin.checkin()
    //     - si el usuario ya está trabajando, se muestra el segundo botón y se usa Checkin.checkout()
    //

}]);


scipControllers.controller('UserListController', ['$scope', '$rootScope', '$location', 'Users', function($scope, $rootScope, $location, Users){
    console.log($rootScope.logged);
    if ($rootScope.logged){
        // La conexión con el API se hace sólo para usuarios loggeados.
        Users.get(
                function(data){
                    // caso exitoso.
                    $scope.users = data;
                },
                function(data){
                    // callback de error. (forbbiden por ejemplo)
                    // mostrar mensaje de error en la obtención de datos
                    // enviar a /checkin -> mostrar mensaje
                    console.log("error?");
                });
    }else{
        console.log("el usuario no está loggeado?");
        $location.path('/login');
    }
}]);


scipControllers.controller('WorkdayListController', ['$scope', '$rootScope', '$location', '$routeParams', 'Workdays', 
        function($scope, $rootScope, $location, $routeParams, Workdays){
        
    console.log("En WorkdayListController");
    if ($rootScope.logged){

        Workdays.get({username:$routeParams.username},
                function(data){
                    console.log($routeParams.username);
                    console.log(data);
                    $scope.workdays = data;
                },
                function(data){
                    // caso de error, por ejemplo 403
                    // se maneja el error acá
                    console.log("error");
                });
    }else{
        console.log("hizo login??");
        $location.path('/login');
    }
}]);


