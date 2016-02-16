(function(){
  angular.module("ShippingApp")
      .controller("CuotaCtrl", ['$http',CuotaCtrl]);
  function CuotaCtrl($http){
      var me = this;
      me.CalcularMonto = function(value){
          //lamamos al servicio a recuprara
          console.log("monto total: "+value);
          me.por_combrar = value - me.acuenta;
          console.log("por cobrar: "+me.por_combrar);
      }
  }
}());
