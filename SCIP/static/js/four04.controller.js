(function (){
    "use strict";

    angular.module('app.scip')
    .controller('Four04Controller',Four04Controller)

    Four04Controller.$inject = ['$scope', '$window', '$route', '$routeParams', '$rootScope', '$location']; 
    function Four04Controller($scope, $window, $route, $routeParams, $rootScope, $location)
    {
        if($window.sessionStorage.token){
           // console.log("este es el token: " + $window.sessionStorage.token);
        }else{
            console.log("no tiene token!");
        }
    };

})();