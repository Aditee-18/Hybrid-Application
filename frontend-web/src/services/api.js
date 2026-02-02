import axios from 'axios';

// Initialize the API instance with your Django Backend URL
const API = axios.create({
    baseURL:"https://hybrid-application-production.up.railway.app/api"
    // baseURL: 'http://127.0.0.1:8000/api', 
});


/**
 * AUTOMATIC TOKEN INJECTION
 * This interceptor checks LocalStorage for the JWT 'token' before 
 * every outgoing request and attaches it to the Authorization Header.
 */
API.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// API ACTIONS 

// Upload CSV for processing
export const uploadCSV = async (file) => {
    const formData = new FormData();
    formData.append('file', file); // 'file' matches the key in Django views

    try {
        const response = await API.post('/upload/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data; 
    } catch (error) {
        const msg = error.response?.data?.error || "Connection to server failed";
        console.error("Upload Error Details:", msg);
        throw new Error(msg);
    }
}

// Fetch user's upload history
export const getHistory = async () => {
    try {
        const response = await API.get('/history/');
        return response.data;
    } catch (error) {
        console.error("History fetch error", error.response?.data || error.message);
        throw error;
    }
};

// Log in user ( This function doesn't use the interceptor above, it gets the token)
export const loginUser = async (username, password) => {
    const res = await API.post('/token/', { username, password });
    localStorage.setItem('token', res.data.access);
    return res.data;
}

export default API;