import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import FileUpload from '../components/FileUpload';
import Charts from '../components/Charts';
import EquipmentTable from '../components/EquipmentTable';
import axios from 'axios';
import { Link } from 'react-router-dom'; 

const Home = () => {
    const { user } = useContext(AuthContext);
    const [data, setData] = useState(null);

    const downloadPDF = async (id) => {
        const response = await axios.get(`http://localhost:8000/api/pdf/${id}/`, {
            responseType: 'blob',
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `Report_${id}.pdf`);
        document.body.appendChild(link);
        link.click();
    };

    if (!user) {
        return (
            <div className="hero-section landing-view">
                <h1>Chemical Equipment Parameter Visualizer</h1>
                <p>Advanced data analytics and visualization </p>
                <Link to="/login">
                    <button className="main-login-btn">Get Started / Login</button>
                </Link>
            </div>
        );
    }

    return (
        <div className="container">
            {!data ? (
                <div className="hero-section">
                    <h1>Ready to visualize equipment data?</h1>
                    <p>Upload your chemical equipment CSV to get started.</p>
                    <FileUpload onUploadSuccess={setData} />
                </div>
            ) : (
                <div className="dashboard-content">
                    <div className="dashboard-header">
                        <h2>Analytics Result for {data.filename || 'dataset'}</h2>
                        <div className="header-actions">
                             <button className="pdf-btn" onClick={() => downloadPDF(data.id)}>Generate PDF Report</button>
                             <button className="reset-btn" onClick={() => setData(null)}>Upload New File</button>
                        </div>
                    </div>
                    
                    <div className="stats-row">
                        <div className="card"><h3>{data.summary.total_count}</h3><p>Total Units</p></div>
                        <div className="card"><h3>{data.summary.avg_pressure.toFixed(2)}</h3><p>Avg Pressure (bar)</p></div>
                        <div className="card"><h3>{data.summary.avg_temp.toFixed(2)}</h3><p>Avg Temp (°C)</p></div>
                    </div>

                    <Charts summary={data.summary} />
                    <EquipmentTable data={data.raw_data} />
                </div>
            )}
        </div>
    );
};
export default Home;