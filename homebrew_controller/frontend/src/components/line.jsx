var React = require('react');
var Chart = require('react-d3-core').Chart;
var LineChart = require('react-d3-basic').LineChart;

(function () {

    var chartData = [];

    var width = 700,
        height = 300,
        margins = {left: 100, right: 100, top: 50, bottom: 50},
        title = "Brew Step Temperature",
        // chart series,
        // field: is what field your data want to be selected
        // name: the name of the field that display in legend
        // color: what color is the line
        chartSeries = [
          {
            field: 'Temperature',
            name: 'Temperature',
            color: '#ff7f0e'
          }
        ],
        // your x accessor
        x = function(d) {
          return d.index;
        }

    ReactDOM.render(
        <Chart
          title={title}
          width={width}
          height={height}
          margins= {margins}
          >
          <LineChart
            margins= {margins}
            title={title}
            data={chartData}
            width={width}
            height={height}
            chartSeries={chartSeries}
            x={x}
          />
        </Chart>
      , document.getElementById('brew-chart')
    )
})();