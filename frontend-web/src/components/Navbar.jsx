import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Navbar = () => {
    const { user, logout } = useContext(AuthContext);

    return (
        <nav className="navbar">
            <div className="nav-container"> 
                <div className="logo">Chemical<span>Visualizer</span></div>
                <div className="nav-links">
                    <Link to="/">Dashboard</Link>
                    <Link to="/history">History</Link>
                    {user ? (
                        <button onClick={logout} className="logout-link">Logout</button>
                    ) : (
                        <Link to="/login" className="login-btn">Login</Link>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;