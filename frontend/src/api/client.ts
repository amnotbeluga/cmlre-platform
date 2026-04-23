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
  if (token && config.headers) {
    config.headers.set('Authorization', `Bearer ${token}`);
  }
  return config;
});


export const api = {

  uploadFile: (formData: FormData) =>
    apiClient.post('/api/v1/ingest/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),


  getStations: (params: Record<string, any>) =>
    apiClient.get('/api/v1/oceanography/stations', { params }),
  getCTDProfile: (stationId: string) =>
    apiClient.get(`/api/v1/oceanography/profiles/${stationId}`),


  getCPUE: (params: Record<string, any>) =>
    apiClient.get('/api/v1/fisheries/cpue', { params }),


  getSpecies: () =>
    apiClient.get('/api/v1/taxonomy/species'),
  analyseOtolith: (formData: FormData) =>
    apiClient.post('/api/v1/taxonomy/otolith/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),


  submitEDNA: (formData: FormData) =>
    apiClient.post('/api/v1/molecular/edna/submit', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  getEDNAResults: (sampleId: string) =>
    apiClient.get(`/api/v1/molecular/edna/${sampleId}/results`),
  getEDNAComposition: () =>
    apiClient.get('/api/v1/molecular/edna/composition'),
  getEDNASamples: () =>
    apiClient.get('/api/v1/molecular/edna/samples'),
  getEDNASequence: () =>
    apiClient.get('/api/v1/molecular/edna/sequence'),
  getPipelineStatus: () =>
    apiClient.get('/api/v1/molecular/pipeline/status'),


  runCorrelation: (params: Record<string, any>) =>
    apiClient.post('/api/v1/analytics/correlation', params),
  getDepthProfile: () =>
    apiClient.get('/api/v1/analytics/depth-profile'),
  getSSTAnomaly: () =>
    apiClient.get('/api/v1/analytics/sst-anomaly'),
  getAnalyticsSummary: () =>
    apiClient.get('/api/v1/analytics/summary'),


  getAbundance: () =>
    apiClient.get('/api/v1/fisheries/abundance'),


  semanticSearch: (query: string) =>
    apiClient.get('/api/v1/ai/search', { params: { query } }),
};
