// src/services/api.js

import axios from 'axios';
import { getToken } from '../utils/auth';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication
export const login = (credentials) =>
  api.post('/login', new URLSearchParams(credentials)).then((res) => res.data);
export const register = (data) => api.post('/register', data).then((res) => res.data);

// Shelter
export const getShelterDetails = () => api.get('/shelter/me').then((res) => res.data);
export const updateShelter = (data) => api.put('/shelter/me', data).then((res) => res.data);
export const deleteShelter = () => api.delete('/shelter/me').then((res) => res.data);

// Animals
export const getAnimals = () => api.get('/animals/').then((res) => res.data);
export const getAnimal = (id) => api.get(`/animals/${id}`).then((res) => res.data);
export const getMyAnimals = () => api.get('/animals/my-animals').then((res) => res.data);
export const addAnimal = (data) => api.post('/animals/', data).then((res) => res.data);
export const updateAnimal = (id, data) =>
  api.put(`/animals/${id}`, data).then((res) => res.data);
export const deleteAnimal = (id) => api.delete(`/animals/${id}`).then((res) => res.data);
export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/animals/upload-csv', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then((res) => res.data);
};

// Descriptions
export const generateDescription = (id) =>
  api.post(`/animals/${id}/generate-description`).then((res) => res.data);
export const generateTranslation = (id) =>
  api.post(`/animals/${id}/generate-translation`).then((res) => res.data);
