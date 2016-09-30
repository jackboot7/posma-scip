(function (){
    "use strict";

    angular.module('app.scip')
    .controller('CheckinController',CheckinController)

    CheckinController.$inject = ['$scope', '$rootScope', '$location', '$window', 'User', 'Checkin']; 
    function CheckinController($scope, $rootScope, $location, $window, User, Checkin)
    {

        var user_obj, username;
        $scope.checkout = false;

        if(!$rootScope.logged){
            $location.path('/login');
        }
        
        user_obj = angular.fromJson($window.sessionStorage.user);
        username = user_obj.username;

        $scope.first_name = user_obj.first_name;
        
        User.get({username:username},
                function(data){ 
                    $scope.checked = data.is_working;

                    var getCoordinates = function(position){
                        $scope.latitude = position.coords.latitude;
                        $scope.longitude = position.coords.longitude;
                    };
                    
                    if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition(getCoordinates);
                    } else {
                        // geolocalization is not supported
                        $scope.latitude = null;
                        $scope.longitude = null;
                    }

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
                            Checkin.checkin({username:username, user_notes:$scope.notes, user_agent:navigator.userAgent, latitude:$scope.latitude, longitude:$scope.longitude},
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
                                        $scope.checkout = true;
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
    };

})();
