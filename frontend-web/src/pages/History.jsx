import React, { useEffect, useState } from 'react';
import { getHistory } from '../services/api';

const History = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    // useEffect runs as soon as the component appears on screen
    useEffect(() => {
        const fetchHistoryData = async () => {
            try {
                const data = await getHistory();
                setHistory(data);
            } catch (err) {
                console.error("Could not load history");
            } finally {
                setLoading(false);
            }
        };
        fetchHistoryData();
    }, []); // Empty dependency array means "run only once"

    if (loading) return <div className="loader">Loading history...</div>;

    return (
        <div className="page">
            <h1>History</h1>
            {history.length === 0 ? (
                <p>No history found. Upload a CSV to get started.</p>
            ) : (
                <div className="history-list">
                    {history.map((record) => (
                        <div key={record.id} className="history-card">
                            <div className="history-header">
                                <strong>File: {record.filename}</strong>
                                <span>{new Date(record.uploaded_at).toLocaleString()}</span>
                            </div>
                            <div className="history-summary">
                                {/* Use parseFloat to ensure it's a number, then toFixed to round it */}
                                <span>{parseFloat(record.avg_temp).toFixed(2)} °C</span>
                                <span>{parseFloat(record.avg_pressure).toFixed(2)} bar</span>
                                <span>{record.total_count} Units</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default History;