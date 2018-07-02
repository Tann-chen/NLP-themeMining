import React, { Component } from "react";
import { Chart, Geom, Axis, Tooltip, Legend, Coord } from "bizcharts";

class PieChart extends Component {
    constructor() {
        super();
        this.status = {
            data: [
                { item: "token_1", count: 40 },
                { item: "token_2", count: 21 },
                { item: "token_3", count: 17 },
                { item: "token_4", count: 13 },
                { item: "token_5", count: 9 }
            ]
        };
    }
    render() {
        return (
            <div>
                <Chart
                    height={window.innerHeight}
                    data={dv}
                    scale={cols}
                    padding={[80, 100, 80, 80]}
                    forceFit
                >
                    <Coord type="theta" radius={0.75} />
                    <Axis name="percent" />
                    <Legend
                        position="right"
                        offsetY={-window.innerHeight / 2 + 120}
                        offsetX={-100}
                    />
                    <Tooltip
                        showTitle={false}
                        itemTpl="<li><span style=&quot;background-color:{color};&quot; class=&quot;g2-tooltip-marker&quot;></span>{name}: {value}</li>"
                    />
                    <Geom
                        type="intervalStack"
                        position="percent"
                        color="item"
                        tooltip={[
                            "item*percent",
                            (item, percent) => {
                                percent = percent * 100 + "%";
                                return {
                                    name: item,
                                    value: percent
                                };
                            }
                        ]}
                        style={{ lineWidth: 1, stroke: "#fff" }}
                    >
                        <Label
                            content="percent"
                            formatter={(val, item) => {
                                return item.point.item + ": " + val;
                            }}
                        />
                    </Geom>
                </Chart>
            </div>
        );
    }
}
