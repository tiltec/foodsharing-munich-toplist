var myapp = angular.module("munich-toplist",["highcharts-ng"]);

myapp.controller("OverviewCtrl",function($scope,$http){
    $http.get("http://localhost:5000/overview").then(function(resp){
        var User = resp.data.entries;
        console.log(User);
        $scope.data = User.slice(0,10);
        var fetchcount_sum = 0;
        var fetchcount_data = User.map(function (el) {
            fetchcount_sum += el.entries[0].fetchcount;
            return el.entries[0].fetchcount;
        }).sort(function(a,b){return b-a});
        var scatter_data = User.map(function (el) {
            return [+el.userid,el.entries[0].fetchcount];
        }).filter(function (el) {
            return el[1];
        });
        var quantil_80;
        fetchcount_sum *= 0.8;
        fetchcount_data.some(function (c,i) {
            fetchcount_sum -= c;
            if(fetchcount_sum<=0){
                quantil_80 = i;
                return true;
            }
        })
        $scope.quantil_80 = quantil_80;
        $scope.highchartsNG.series = [{name:"Foodsaver M�nchens",data:fetchcount_data}];
        $scope.highchartsNG2.series = [{name:"Foodsaver M�nchens",data:scatter_data,point: {
            events: {
                click: function (ev) {
                    var win = window.open("https://foodsharing.de/profile/"+ev.currentTarget.x, '_blank');
                    win.focus();
                }
            }
        }}];
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
    $scope.highchartsNG2 = {
        options: {
            chart: {
                type: 'scatter'
            }
        },
        series: [],
        title: {
            text: 'Abholungen/UserID'
        },
        loading: false,
        yAxis: {
            title: {
                text: 'Anzahl der Abholungen'
            }
        },
        xAxis: {
            title: {
                text: 'UserID'
            }
        }
    }

});