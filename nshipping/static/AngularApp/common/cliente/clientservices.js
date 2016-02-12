(function(){
    angular.module("common.services")
        .factory("clienteService",ClienteService)

    function ClienteService($http){
        return $http.get("api/clientes");
    }
}());
