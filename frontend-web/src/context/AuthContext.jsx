import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    // Initializing state directly from localStorage so it doesn't "blink" or crash on refresh
    const [user, setUser] = useState(() => {
        const savedToken = localStorage.getItem('token');
        return savedToken ? { loggedIn: true } : null;
    });

    const login = async (username, password) => {
        const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
        const res = await axios.post(`${baseURL}/token/`, { username, password });
        localStorage.setItem('token', res.data.access);
        setUser({ loggedIn: true });
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
        window.location.href = '/login'; // Hard redirect is safer than navigate for logout
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};