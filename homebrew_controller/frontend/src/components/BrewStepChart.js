import React, {Component} from "react";
import ReactDOM from "react-dom";
import {LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip} from "recharts";

class BrewStepChart extends Component {
    constructor() {
        super();
        this.state = {
            tempReadings: []
        };
    }

    componentDidMount() {
        const step = this.props.location.state.step;
        const brewId = this.props.location.state.brewId;

        fetch("http://127.0.0.1:8000/api/brew/" + brewId + "/" + step)
            .then(function(response) {
                return response.json();
            })
            .then((tempReadings) => {
                this.setState(() => ({tempReadings}));
            });
    }

    render() {
        var chartData = this.state.tempReadings;

        return (
            <div>
                <LineChart width={600} height={300} data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                  <Line type="monotone" dataKey="temperature" stroke="#8884d8" />
                  <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                  <XAxis dataKey="timestamp" />
                  <YAxis />
                  <Tooltip />
                </LineChart>
            </div>
        );
    }
}

export default BrewStepChart;

//ReactDOM.render(
//  <BrewStepChart />,
//  document.getElementById('brew-chart')
//);