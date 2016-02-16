(function(){
  angular.module("ClientApp")
      .controller("ClientCtrl", ['$http',ClientCtrl]);
  function ClientCtrl($http){
      var me = this;
/*      me.Recuperarlista = function(){
        clienteService.then(function(response){
          me.clientes = response.data;
        });
      }*/
      me.RecuperarCliente = function(value,id){
          //lamamos al servicio a recuprara
          console.log("funcion de RecuperarCliente");
          $http.get("/api/cliente/"+value).success(function(respuesta){
              console.log("Esta es la Respuesta:", respuesta);
              if (id === "sender") {
                me.name = respuesta.full_name;
                me.rs = respuesta.business_name;
              }
              else {
                me.addr_name = respuesta.full_name;
                me.addr_rs = respuesta.business_name;
              }

          }).error(function(respuesta) {
                console.log('Error:' + respuesta);
            });
      }
  }
}());
