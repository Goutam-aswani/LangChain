// src/services/api.js

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const apiClient = axios.create({
    baseURL: API_BASE_URL,
});

export const setupAuthInterceptor = (logout) => {
    apiClient.interceptors.response.use(
        // If the response is successful, just return it
        (response) => response,
        // If there's an error...
        (error) => {
            // Check if the error is a 401 Unauthorized
            if (error.response && error.response.status === 401) {
                // If it is, call the logout function that we passed in
                logout();
            }
            // Be sure to return the error, so it can be handled by the component if needed
            return Promise.reject(error);
        }
    );
};

export const api = {
    async register(username, email, password) {
        try {
            const payload = { username, email, password };
            // Note: The backend returns the new user object upon successful registration
            const response = await apiClient.post('/users/register', payload);
            return response.data;
        } catch (error) {
            console.error('Registration failed:', error.response?.data || error.message);
            // Re-throw the error to be handled by the component
            throw error.response?.data || new Error('Registration failed');
        }
    },

    async verifyEmail(email, otp) {
        try {
            const payload = { email, otp };
            const response = await apiClient.post('/users/verify-email', payload);
            return response.data;
        } catch (error) {
            console.error('Email verification failed:', error.response?.data || error.message);
            throw error.response?.data || new Error('Email verification failed');
        }
    },

    async login(username, password) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        try {
            const response = await apiClient.post('/auth/token', formData);
            return response.data.access_token;
        } catch (error) {
            console.error('Login failed:', error.response?.data || error.message);
            throw new Error('Login failed');
        }
    },

    async getChatSessions(token) {
        try {
            const response = await apiClient.get('/chats/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            return response.data;
        } catch (error) {
            console.error('Failed to fetch sessions:', error.response?.data || error.message);
            throw new Error('Failed to fetch sessions');
        }
    },

    async getChatHistory(token, sessionId) {
        try {
            const response = await apiClient.get(`/chats/${sessionId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            return response.data;
        } catch (error) {
            console.error('Failed to fetch history:', error.response?.data || error.message);
            throw new Error('Failed to fetch history');
        }
    },

    async postMessage(token, prompt, sessionId) {
        try {
            const payload = { prompt, session_id: sessionId };
            const response = await apiClient.post('/chats/', payload, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            return response.data;
        } catch (error) {
            console.error('Failed to post message:', error.response?.data || error.message);
            throw new Error('Failed to post message');
        }
    },
    async deleteChatSession(token, sessionId) {
        try {
            const response = await apiClient.delete(`/chats/${sessionId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            return response.data;
        } catch (error) {
            console.error('Failed to delete session:', error.response?.data || error.message);
            throw new Error('Failed to delete session');
        }
    },
    async renameChatSession(token, sessionId, newTitle) {
        try {
            const payload = { new_title: newTitle };
            const response = await apiClient.put(`/chats/${sessionId}`, payload, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            return response.data;
        } catch (error) {
            console.error('Failed to rename session:', error.response?.data || error.message);
            throw new Error('Failed to rename session');
        }
    }
};
