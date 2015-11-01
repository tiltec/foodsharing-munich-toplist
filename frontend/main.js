var myapp = angular.module("munich-toplist",["highcharts-ng"]);

myapp.controller("OverviewCtrl",function($scope,$http){
    $http.get("http://localhost:5000/overview").then(function(resp){
        var User = resp.data.entries;
        console.log(User);
        $scope.data = User.slice(0,10);
        $scope.highchartsNG.series = [{name:"Foodsaver Münchens",data:User.map(function (el) {
            return el.entries[0].fetchcount;
        })}]
    },function(resp){
        console.log("Error retrieving overview data")
    })

    $scope.highchartsNG = {
        options: {
            chart: {
                type: 'scatter'
            }
        },
        series: [],
        title: {
            text: 'Verteilung der aktuellen Abholungszahlen'
        },
        loading: false,
        yAxis: {
            title: {
                text: 'Anzahl der Abholungen'
            }
        }
    }

});