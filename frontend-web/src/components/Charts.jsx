import React from 'react';
import { Pie, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const Charts = ({ summary }) => {
    // If summary exists but the key is missing, show a message
    if (!summary || !summary.type_dist) {
        console.log("Still waiting for correct summary keys...", summary);
        return <div>Processing statistics...</div>;
    }

    const pieData = {
        labels: Object.keys(summary.type_dist), // MATCHING DJANGO KEY
        datasets: [{
            label: 'Number of Units',
            data: Object.values(summary.type_dist),
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
        }]
    };

    const barData = {
        labels: ['Avg Pressure', 'Avg Temp', 'Avg Flowrate'],
        datasets: [{
            label: 'Process Averages',
            data: [summary.avg_pressure, summary.avg_temp, summary.avg_flow],
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
        }]
    };

    const options = {
    responsive: true,
    maintainAspectRatio: false, //  Allows chart to stretch to the 800px CSS height
    plugins: {
        legend: {
            position: 'top',
            labels: {
                font: {
                    size: 18, 
                    weight: '600'
                }
            }
        }
    },
    layout: {
        padding: 20
    }
};

    return (
    <div className="charts-container" style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
        
        {/* Left Side: Pie Chart */}
        <div className="chart-item" style={{ flex: 1, background: '#fff', padding: '30px', borderRadius: '20px' }}>
            <h3>Equipment Distribution</h3>
            <div className="chart-wrapper" style={{ height: '700px', position: 'relative' }}>
                <Pie data={pieData} options={options} /> 
            </div>
        </div>

        {/* Right Side: Bar Chart */}
        <div className="chart-item" style={{ flex: 1, background: '#fff', padding: '30px', borderRadius: '20px' }}>
            <h3>Mean Parameters</h3>
            <div className="chart-wrapper" style={{ height: '700px', position: 'relative' }}>
                <Bar data={barData} options={options} />
            </div>
        </div>

    </div>
);
};

export default Charts;