import React, { Component } from "react";
import "./App.css";
import { Row, Col } from "antd";
import NumberSelector from "./NumberSelector";

const bkg = {
    background: "grey",
    board: "solid 1px black",
    height: 400
};

class App extends Component {
    state = {
        minNum: 3,
        maxNum: 10,
        marks: {
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10"
        }
    };

    render() {
        return (
            <div className="App">
                <Row gutter={32}>
                    <Col span={8} style={bkg}>
                        <NumberSelector init={this.state} />
                    </Col>
                    <Col span={16} style={bkg}>
                        article scanning board
                    </Col>
                </Row>
                <Row gutter={16}>
                    <Col span={12} style={bkg}>
                        pie chart
                    </Col>
                    <Col span={12} style={bkg}>
                        bar chart
                    </Col>
                </Row>
            </div>
        );
    }
}

export default App;
