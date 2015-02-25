var scipControllers = angular.module('scipControllers', ['ngResource']);

scipControllers.controller('404Controller', function($scope, $window, $route, $routeParams, $rootScope, $location){
    if($window.sessionStorage.token){
       // console.log("este es el token: " + $window.sessionStorage.token);
    }else{
        console.log("no tiene token!");
    }
});

scipControllers.controller('LoginController', ['$scope', '$window', '$rootScope', '$location', 'Login', 'User', 'jwtHelper', function($scope, $window, $rootScope, $location, Login, User, jwtHelper){

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
}]);

scipControllers.controller('CheckinController',['$scope', '$rootScope', '$location', '$window', 'User', 'Checkin',  
        function($scope, $rootScope, $location, $window, User, Checkin){

    var user_obj, username;

    if(!$rootScope.logged){
        $location.path('/login');
    }
    
    user_obj = angular.fromJson($window.sessionStorage.user);
    username = user_obj.username;

    $scope.first_name = user_obj.first_name;
    
    User.get({username:username},
            function(data){ 
                $scope.checked = data.is_working;

                if (data.last_workday.start) {
                    $scope.workday_started = data.last_workday.start;
                }

                if (data.last_workday.finish) {
                    $scope.workday_finished = data.last_workday.finish;
                } else {
                    $scope.notes = data.last_workday.user_notes;
                }

                $scope.checkin = function(){
                    // se  verifica el estado actual del usuario.
                    // se hace la llamada al api. para hacer checkin o checkout del usuario dependiendo del caso.
                    if(!$scope.checked){
                        // Llamada al API para hacer checkin
                        // Si el usuario no ha hecho checkin, se muestra el botón y se usa Checkin.checkin()
                        Checkin.checkin({username:username, user_notes:$scope.notes},
                                function(data){
                                    // éxito en checkin
                                    $scope.checked = !$scope.checked;
                                    $scope.workday_started = data.start;
                                },
                                function(data){
                                    console.log("Problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
                                });

                    }else{
                        // Llamada al API para hacer checkout
                        // Si el usuario ya está trabajando, se muestra el segundo botón y se usa Checkin.checkout()
                        Checkin.checkout({username:username, user_notes:$scope.notes},
                                function(data){
                                    // éxito en checkout
                                    $scope.checked = !$scope.checked;
                                    $scope.workday_finished = data.finish;
                                    $scope.notes = "";
                                },
                                function(data){
                                    console.log("Problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
                                });
                    }
                }
            },
            function(data){
                console.log("Problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
            });
}]);


scipControllers.controller('UserListController', ['$scope', '$rootScope', '$location', '$window', 'Users', function($scope, $rootScope, $location, $window, Users){

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
                console.log("Problema con la conexión del API. Mostrar mensaje de error y redireccionar.");
            });
}]);


scipControllers.controller('WorkdayListController', ['$scope', '$rootScope', '$location', '$routeParams', '$window', 'Workdays', 
        function($scope, $rootScope, $location, $routeParams, $window, Workdays){
        
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
}]);
