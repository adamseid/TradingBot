import React from 'react';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import moment from 'moment';

const Graph = (props) => {
    const { column_names, list_of_columns } = props.state.graph;

    if (column_names.length === 0 || list_of_columns.length === 0) {
        return <div>Loading...</div>;
    }

    // Get the time column as an array of timestamps
    const timeColumn = list_of_columns[column_names.indexOf('time')];

    // Format the timestamps into desired format (e.g. 'YYYY-MM-DD HH:mm:ss')
    const labels = timeColumn.map((timestamp) => moment(timestamp).format('YYYY-MM-DD HH:mm:ss'));

    const datasets = [];

    for (let i = 1; i < column_names.length; i++) {
        if (['time', 'selectionMenu', 'analysis', 'simulation', 'unix'].includes(column_names[i])) {
            continue;
        }

        datasets.push({
            label: column_names[i],
            data: list_of_columns[i],
            fill: false,
            pointRadius: 0,
            borderColor: '#006699'//getRandomColor(),
        });
    }

    const options = {
        animation: {
            duration: 0 // Disable animations
        }
    };

    return (
        <div>
            {datasets.map((dataset) => (
                <div key={dataset.label}>
                    <h2>{dataset.label}</h2>
                    <Line data={{ labels: labels, datasets: [dataset] }} options={options} />
                </div>
            ))}
        </div>
    );
};

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }

    return color;
}

export default Graph;
