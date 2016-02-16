(function(){
  angular.module("ShippingApp")
      .controller("ClientCtrl", ['$http',ClientCtrl]);
  function ClientCtrl($http){
      var me = this;
      me.ValidarID = function(value, id){
          //metodo para validar casilla id__sender
          if (id == "sender"){
              if ((value.length != 8) && (value.length != 11)) {
                  console.log("el id es incorrecto");
                  me.classender = "error-shipping";
              }
              else {
                  me.classender = "default";
              }
          }
          else {
            if ((value.length != 8) && (value.length != 11)) {
                console.log("el id es incorrecto");
                me.clasaddr = "error-shipping";
            }
            else {
                me.clasaddr = "default";
            }
          }
      }

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
