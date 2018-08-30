import React, {Component} from "react";
import ReactDOM from "react-dom";
import { Link } from "react-router-dom";
import Brew from "./Brew.js";

class AllBrews extends Component {
    constructor() {
        super();
        this.state = {
            brews: []
        };
    }

    componentDidMount() {
        fetch("http://127.0.0.1:8000/get/all/brews")
            .then(function(response) {
                return response.json();
            })
            .then((brews) => {
                this.setState(() => ({brews}));
            });
    }

    render() {
        var brewItems = this.state.brews.map((brew) => {
            var brewUrl = `/brew/${brew.id}`;
            return (<li><Link to={{pathname: brewUrl, state: {brewId:brew.id}}} >{brew.name}</Link></li>);
        });
        return (
            <ul>
                {brewItems}
            </ul>
        );
    }
}

export default AllBrews;
