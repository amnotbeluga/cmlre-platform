import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// API methods
export const api = {
  // Ingestion
  uploadFile: (formData: FormData) =>
    apiClient.post('/api/v1/ingest/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),

  // Oceanographic
  getStations: (params: object) =>
    apiClient.get('/api/v1/oceanography/stations', { params }),
  getCTDProfile: (stationId: string) =>
    apiClient.get(`/api/v1/oceanography/profiles/${stationId}`),

  // Fisheries
  getCPUE: (params: object) =>
    apiClient.get('/api/v1/fisheries/cpue', { params }),

  // Taxonomy
  analyseOtolith: (formData: FormData) =>
    apiClient.post('/api/v1/taxonomy/otolith/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),

  // eDNA
  submitEDNA: (formData: FormData) =>
    apiClient.post('/api/v1/molecular/edna/submit', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  getEDNAResults: (sampleId: string) =>
    apiClient.get(`/api/v1/molecular/edna/${sampleId}/results`),

  // Analytics
  runCorrelation: (params: object) =>
    apiClient.post('/api/v1/analytics/correlation', params),

  // Search
  semanticSearch: (query: string) =>
    apiClient.get('/api/v1/ai/search', { params: { query } }),
};
