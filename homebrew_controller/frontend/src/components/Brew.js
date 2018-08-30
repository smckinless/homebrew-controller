import React, {Component} from "react";
import ReactDOM from "react-dom";
import BrewStepChart from "./BrewStepChart.js";
import { BrowserRouter, Route, Link } from "react-router-dom";

class Brew extends Component {
    constructor() {
        super();
        this.state = {
            brew: null
        };
    }

    componentDidMount() {
        var brewId = this.props.location.state.brewId;
        var apiUrl = "http://127.0.0.1:8000/api/brew/" + brewId;
        fetch(apiUrl)
            .then(function(response) {
                return response.json();
            })
            .then((brew) => {
                console.log({brew});
                this.setState(() => ({brew}));
            });
    }

    render() {
        var brew = this.state.brew;
        var brewId = brew != null ? brew.id : null;
        var title = brew != null ? brew.name : "";
        var mash = brew != null ? "/brew/" + brew.id + "/mash" : "";
        var boil = brew != null ? "/brew/" + brew.id + "/boil" : "";
        var fermentation = brew != null ? "/brew/" +  brew.id + "/fermentation" : "";
        return (
                <div>
                    <h1>{title}</h1>
                    <h2>Temperature Readings for Each Brew Step</h2>
                    <Link to={{pathname: mash, state: {brewId:brewId, step:"mash"}}}>Mash</Link>
                    <Link to={{pathname: boil, state: {brewId:brewId, step:"boil"}}}>Boil</Link>
                    <Link to={{pathname: fermentation, state: {brewId:brewId, step:"fermentation"}}}>Fermentation</Link>
                </div>
        );

    }
}

export default Brew;

//const wrapper = document.getElementById("brew");
//
//ReactDOM.render(<Brew />, wrapper);