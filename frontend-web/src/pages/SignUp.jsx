import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const Signup = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            // Using your live Railway URL via the ENV variable
            const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
            await axios.post(`${baseURL}/register/`, { username, password });
            
            alert("Account created successfully! Please login.");
            navigate('/login');
        } catch (err) {
            console.error(err);
            alert("Signup Failed! This username might already be taken.");
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h2>Join <span>Chemical App</span></h2>
                    <p>Create an account to start analyzing equipment data.</p>
                </div>
                
                <form onSubmit={handleSignup} className="auth-form">
                    <div className="input-group">
                        <label>Choose Username</label>
                        <input 
                            type="text" 
                            placeholder="e.g. aditee_engineer" 
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required 
                        />
                    </div>
                    
                    <div className="input-group">
                        <label>Choose Password</label>
                        <input 
                            type="password" 
                            placeholder="At least 8 characters" 
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required 
                        />
                    </div>
                    
                    <button type="submit" className="login-submit-btn">
                        Create Free Account
                    </button>
                </form>

                <div className="auth-footer-link">
                    Already have an account? <Link to="/login">Sign In here</Link>
                </div>
            </div>
        </div>
    );
};

export default Signup;