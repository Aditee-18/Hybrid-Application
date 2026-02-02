import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Navbar = () => {
    const { user, logout } = useContext(AuthContext); // logout comes from your context
    const navigate = useNavigate();

    const handleLogout = () => {
        logout(); // Deletes token
        navigate('/login'); // Sends user back to login
    };

    return (
        <nav className="navbar">
            <div className="logo">Chemical <span>Visualizer</span></div>
            <div className="nav-links">
                <Link to="/">Dashboard</Link>
                <Link to="/history">History</Link>
                {user ? (
                    <button className="logout-btn" onClick={handleLogout}>Logout</button>
                ) : (
                    <Link to="/login">Login</Link>
                )}
            </div>
        </nav>
    );
};

export default Navbar;