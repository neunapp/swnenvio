(function(){
    var app = angular.module("ShippingApp",[
                            'common.services',
        ])
        .config(
        function($interpolateProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }
);
}());
