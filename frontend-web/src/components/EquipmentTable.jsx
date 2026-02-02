import React from 'react';

const EquipmentTable = ({ data }) => {
    if (!data || data.length === 0) return null;

    return (
         <div className="detail-list-section">
            <h2 className="section-title">Detailed Equipment Inventory</h2>
            <div className="table-wrapper">
                <table className="styled-table">
                    <thead>
                        <tr>
                            <th>Serial / Name</th>
                            <th>Category</th>
                            <th>Flow (m³/h)</th>
                            <th>Pressure (bar)</th>
                            <th>Temp (°C)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map((item, i) => (
                            <tr key={i}>
                                {/* Using double-check to find the Name regardless of CSV column naming */}
                                <td>{item['Equipment Name'] || item['name'] || "N/A"}</td>
                                <td>
                                    <span className={`type-badge ${item.Type || item.type}`}>
                                        {item.Type || item.type}
                                    </span>
                                </td>
                                <td>{item.Flowrate || item.flowrate}</td>
                                <td>{item.Pressure || item.pressure}</td>
                                <td className={(item.Temperature || item.temperature) > 150 ? "high-temp" : ""}>
                                    {item.Temperature || item.temperature}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default EquipmentTable;