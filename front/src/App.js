import React, { Component } from "react";
import "./App.css";
import { Row, Col } from "antd";
import NumberSelector from "./NumberSelector";
import PieChart from "./Pie";
import BarChar from "./Bar";

const bkg = {
    background: "white",
    board: "solid 1px black",
    height: 400
};

const pieData = [
    { item: "事例一", count: 40 },
    { item: "事例二", count: 21 },
    { item: "事例三", count: 17 },
    { item: "事例四", count: 13 },
    { item: "事例五", count: 9 }
];

const barData = [
    { token: "natual", frequency: 23 },
    { token: "language", frequency: 10 },
    { token: "process", frequency: 5 },
    { token: "hello", frequency: 20 },
    { token: "world", frequency: 8 },
    { token: "tomorrow", frequency: 12 },
    { token: "come", frequency: 36 },
    { token: "go", frequency: 9 }
];

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
        console.log(pieData);
        return (
            <div className="App">
                <Row gutter={32}>
                    <Col span={8} style={bkg}>
                        <NumberSelector init={this.state} />
                    </Col>
                    <Col span={16} style={bkg} />
                </Row>
                <Row gutter={16}>
                    <Col span={10} style={bkg}>
                        <PieChart init={pieData} />
                    </Col>
                    <Col span={14} style={bkg}>
                        <BarChar init={barData} />
                    </Col>
                </Row>
            </div>
        );
    }
}

export default App;
