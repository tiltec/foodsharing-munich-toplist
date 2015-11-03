var myapp = angular.module("munich-toplist",["highcharts-ng"]);

myapp.controller("OverviewCtrl",function($scope,$http){
    $http.get("/overview").then(function(resp){
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

        function parseTime(tstring) { return new Date(tstring.replace(' ','T')) }
        function getEntriesInDateRange(all, msrange) { 
            var recent = parseTime(all[0].date);
            return all.filter(function(el) {
                    return recent-parseTime(el.date) < msrange;
                });
        }
        $scope.mostactivelist = User.map(function (el) {
            var entries = getEntriesInDateRange(el.entries, 1000*60*60*24*7.1);
            return {count: entries[0].fetchcount-entries.slice(-1)[0].fetchcount,
                    userid: el.userid};
        }).sort(function(a,b){return b.count-a.count}).slice(0,20);
        
        $scope.friendsgained = User.map(function (el) {
            var entries = getEntriesInDateRange(el.entries, 1000*60*60*24*7.1);
            return {count: entries[0].friends-entries.slice(-1)[0].friends,
                    userid: el.userid};
        }).sort(function(a,b){return b.count-a.count}).slice(0,10);

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
        $scope.highchartsNG.series = [{name:"Foodsaver Münchens",data:fetchcount_data}];
        $scope.highchartsNG2.series = [{name:"Foodsaver Münchens",data:scatter_data,point: {
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