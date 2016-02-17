(function(){
  angular.module("ShippingApp")
      .controller("SlipCtrl", ['$http',SlipCtrl]);
  function SlipCtrl($http){
      var me = this;
      me.VelidarSerie = function(value,id){
          //verificamos que solo se ingresen numeros
          console.log("ingreso al metodo validar");
          if (id == "serie"){
              if (!/^([0-9])*$/.test(value)){
                  me.classerie = "error-shipping";
              }
              else {
                  me.classerie = "default";
              }
          }
          else if(id == "numero") {
              if (!/^([0-9])*$/.test(value)){
                  me.clasnumero = "error-shipping";
              }
              else {
                  me.clasnumero = "default";
              }
          }
          else {
              if (!/^([0-9])*$/.test(value)){
                  me.clasguide = "error-shipping";
              }
              else {
                  me.clasguide = "default";
              }
          }
      }
  }
}());
