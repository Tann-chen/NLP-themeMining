import React, { Component } from "react";
import { Slider, Row, Col } from "antd";

class NumberSelector extends Component {
    state = {
        inputNum: 0
    };

    onChange = value => {
        this.setState({
            inputNum: value
        });
    };

    componentWillMount() {
        this.setState({
            inputNum: this.props.init.minNum
        });
    }

    render() {
        const { minNum, maxNum, marks } = this.props.init;
        return (
            <Row>
                <Col span={24}>
                    <Slider
                        min={minNum}
                        max={maxNum}
                        marks={marks}
                        included={true}
                        step={null}
                        onChange={this.onChange}
                        value={this.state.inputNum}
                    />
                </Col>
            </Row>
        );
    }
}

export default NumberSelector;
