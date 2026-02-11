import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  signup: (fullName, email, password, confirmPassword) => 
    api.post('/auth/signup', { full_name: fullName, email, password, confirm_password: confirmPassword }),
  login: (email, password) => api.post('/auth/login', { email, password }),
};

export const datasetAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/datasets/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getAnalysis: (datasetId) => api.get(`/datasets/analysis/${datasetId}`),
  list: () => api.get('/datasets/list'),
  chat: (datasetId, message) => api.post(`/chat/dataset/${datasetId}`, { message }),
};

export default api;
