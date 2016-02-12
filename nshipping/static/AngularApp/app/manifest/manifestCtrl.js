(function(){
  angular.module("ClientApp")
      .controller("ManifestCtrl", ['$http',ManifestCtrl]);
  function ManifestCtrl($http){
      var me = this;
      /* recupramos la lista de manifiestos */
      me.RecuperarManifest = function(value,id){
          //lamamos al servicio a recuprarar
          console.log("funcion de Manifiesto");
          $http.get("/api/manifiesto/"+value).success(function(respuesta){
              console.log("Esta es la Respuesta:", respuesta);
                me.deposit_count = respuesta.deposit_slip;
          });
      }
      me.deposit_count = 0;
      me.change = function(value){
          console.log("este es el valor :"+value);
          $http.get("/api/manifiesto/"+value).success(function(respuesta){
              console.log("Esta es la Respuesta:", respuesta);
              if (respuesta.deposit_slip.length>0) {
                  me.deposit_count = respuesta.deposit_slip.length;
              }
          });
      }
  }
}());
