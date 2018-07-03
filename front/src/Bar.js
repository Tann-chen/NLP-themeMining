import React, { Component } from "react";
import { Chart, Geom, Axis, Tooltip } from "bizcharts";

export default class BarChar extends Component {
    render() {
        const data = this.props.init;
        const cols = {
            frequency: { tickInterval: 5 }
        };
        return (
            <Chart height={400} data={data} scale={cols} forceFit>
                <Axis name="token" />
                <Axis name="frequency" />
                <Tooltip crosshairs={{ type: "y" }} />
                <Geom type="interval" position="token*frequency" />
            </Chart>
        );
    }
}
