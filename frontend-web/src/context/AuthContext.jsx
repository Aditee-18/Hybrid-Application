import { createContext, useState } from "react";
import axios from "axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(localStorage.getItem('token') ? true : false);

    const login = async (username, password) => {
        const res = await axios.post('http://localhost:8000/api/token/', { username, password });
        localStorage.setItem('token', res.data.access);
        setUser(true);
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(false);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};