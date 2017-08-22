$(document).ready(function () {
    // create date from years, hours, minutes, seconds passed in
    function newDateString(year, month, hours, minutes, seconds) {
        return new Date(year, month, hours, minutes, seconds);
    }

    var temp_readings = {{temp_readings|safe}};

    // Create new chart with given data points for chart
    function newChart(dataPoints, probe) {
        var chart = new CanvasJS.Chart("chartContainer-" + probe,{
            zoomEnabled: true,
            title: {
                text: "Temperature Over Time for " + "{{current_brew.current_brew_step.name}}"
            },
            toolTip: {
                shared: true

            },
            legend: {
                verticalAlign: "top",
                horizontalAlign: "center",
                                fontSize: 14,
                fontWeight: "bold",
                fontFamily: "calibri",
                fontColor: "dimGrey"
            },
            axisX: {
                title: "chart updates every 10 secs"
            },
            axisY:{
                suffix: '°',
                includeZero: false
            },
            data: [{
                // dataSeries1
                type: "line",
                showInLegend: true,
                name: "Temperature over Time",
                dataPoints: dataPoints
            }
            ],
          legend:{
            cursor:"pointer",
            itemclick : function(e) {
              if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
                e.dataSeries.visible = false;
              }
              else {
                e.dataSeries.visible = true;
              }
              chart.render();
            }
          }
        });
        chart.render();
    }

    for (probe in temp_readings) {
        var data = [];
        console.log(temp_readings[probe]);
        for (var i = 0; i < temp_readings[probe].length; i++) {
            data.push({x: new Date(temp_readings[probe][i].timestamp), y: temp_readings[probe][i].temperature});
        }

        // dataPoints
        var dataPoints1 = data;

        // Add in initial cart rendering
        newChart(dataPoints1, probe);
    }

    var updateInterval = 10000;

    var updateChart = function () {
        for (probe in temp_readings) {
            $.ajax({
                type: "GET",
                url: '/get/temp_data/',
                data: {"brew": {{current_brew.id}}, "brew_step": {{current_brew.current_brew_step.id}},
                        "probe": probe},
                success: function(response) {
                    for (probe in response.data) {
                        var dataPoints = [];
                        for (var j = 0; j < response.data[probe].length; j++) {
                            dataPoints.push({x: new Date(response.data[probe][j].x), y: response.data[probe][j].y});
                        }
                        newChart(dataPoints, probe);
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    };

    // update chart after specified interval
    setInterval(function(){updateChart()}, updateInterval);
});