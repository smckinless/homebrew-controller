import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import AllBrews from "./AllBrews.js";
import Brew from "./Brew.js";
import BrewStepChart from "./BrewStepChart.js"

class App extends React.Component {
    render() {
        return (
            <BrowserRouter>
                <div>
                    <AllBrews />
                    <Switch>
                        <Route exact path="/" component={AllBrews} />
                        <Route exact path="/brew/:brewId" component={Brew} />
                        <Route exact path="/brew/:brewId/:step" component={BrewStepChart} />
                    </Switch>
                </div>
            </BrowserRouter>
        );
    }
}

export default App;

const wrapper = document.getElementById("app");

ReactDOM.render(<App />, wrapper);