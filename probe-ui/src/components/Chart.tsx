import React from "react";
import Chart from "react-apexcharts";
import {ApexOptions} from "apexcharts";

export default (props: any) => {
    const options: ApexOptions = {
        chart: {
            zoom: {
                enabled: false
            },
            animations: {
                easing: "easeinout",
                dynamicAnimation: {
                    speed: 1
                }
            },
        },
        tooltip: {
            x: {
                format: "HH:mm:ss"
            }
        },
        xaxis: {
            type: "datetime",
            range: props.range,
        },
        yaxis: {
            labels: {
                formatter: (val: number) => val.toFixed(2)
            },
            title: {text: "Response Time (ms)"}
        }
    };
    return <Chart type="line" options={options} series={props.series}/>;
};
