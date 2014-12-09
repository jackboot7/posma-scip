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

scipControllers.controller('LoginController', ['$scope', '$window', '$rootScope', '$location', 'Login', 'User', 'jwtHelper', function($scope, $window, $rootScope, $location, Login, User, jwtHelper){
    console.log("En LoginController");

    $scope.login = function() {
        Login.post(
                {username:$scope.username, password:$scope.password},

                function(data){
                    var user_obj = jwtHelper.decodeToken(data.token)

                    $window.sessionStorage.token = data.token;
                    $window.sessionStorage.user = JSON.stringify(user_obj);

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

scipControllers.controller('CheckinController',['$scope', '$rootScope', '$location', '$window', 'User', 'Checkin',  
        function($scope, $rootScope, $location, $window, User, Checkin){

    console.log("En CheckinController");
    if(!$rootScope.logged){
        $location.path('/login');
    }else{
        $scope.is_staff = JSON.parse($window.sessionStorage.user).is_staff;
        var username = JSON.parse($window.sessionStorage.user).username;
        User.get( {username:username},
                function(data){ 
                   // success
                   $scope.checked = data.is_working;
                   $scope.checkin = function(){
                       console.log("scope.checked " + $scope.checked);
                        // se  verifica el estado actual del usuario.
                        // se hace la llamada al api. para hacer checkin o checkout del usuario dependiendo del caso.
                        if(!$scope.checked){
                            // Llamada al API para hacer checkin
                            // Si el usuario no ha hecho checkin, se muestra el botón y se usa Checkin.checkin()
                            //
                            Checkin.checkin({username:username},
                                    function(data){
                                        // éxito en checkin
                                        console.log(data);
                                        $scope.checked = !$scope.checked;
                                    },
                                    function(data){
                                        // fail en el checkin
                                        console.log("fail: " + data);
                                    });

                        }else{
                            // Llamada al API para hacer checkout
                            // Si el usuario ya está trabajando, se muestra el segundo botón y se usa Checkin.checkout()
                            Checkin.checkout({username:username},
                                    function(data){
                                        // éxito en checkin
                                        console.log(data);
                                        $scope.checked = !$scope.checked;
                                    },
                                    function(data){
                                        // fail en el checkin
                                        console.log("fail: " + data);
                                    });

                        }
                    }
                },
                function(data){
                    console.log("Error en la llamada al API.");
                });
    }
}]);


scipControllers.controller('UserListController', ['$scope', '$rootScope', '$location', '$window', 'Users', function($scope, $rootScope, $location, $window, Users){
    console.log($rootScope.logged);
    if ($rootScope.logged){
        if (!JSON.parse($window.sessionStorage.user).is_staff) {
            console.log("el usuario no es admin");
            $location.path('/404');
        }
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


scipControllers.controller('WorkdayListController', ['$scope', '$rootScope', '$location', '$routeParams', '$window', 'Workdays', 
        function($scope, $rootScope, $location, $routeParams, $window, Workdays){
        
    console.log("En WorkdayListController");
    if ($rootScope.logged){
        $scope.username = ($routeParams.username)? $routeParams.username : JSON.parse($window.sessionStorage.user).username;

        Workdays.get({username: $scope.username},
                function(data){
                    console.log($scope.username);
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


