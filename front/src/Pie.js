import React, { Component } from "react";
import { Chart, Geom, Axis, Tooltip, Coord, Label } from "bizcharts";
import DataSet from "@antv/data-set";

const { DataView } = DataSet;

export default class PieChart extends Component {
    render() {
        const dv = new DataView();
        const data = this.props.init;
        dv.source(data).transform({
            type: "percent",
            field: "count",
            dimension: "item",
            as: "percent"
        });
        const cols = {
            percent: {
                formatter: val => {
                    val = val * 100 + "%";
                    return val;
                }
            }
        };
        return (
            <Chart
                height={300}
                data={dv}
                scale={cols}
                padding={[0, 0, 0, 0]}
                forceFit
            >
                <Coord type="theta" radius={0.75} />
                <Axis name="percent" />

                <Tooltip
                    showTitle={false}
                    itemTpl="<li><span style=&quot;background-color:{color};&quot; class=&quot;g2-tooltip-marker&quot;></span>{name}:{value}</li>"
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
                            return item.point.item + ":" + val;
                        }}
                    />
                </Geom>
            </Chart>
        );
    }
}
