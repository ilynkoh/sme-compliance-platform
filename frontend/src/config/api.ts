export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  AUTH: {
    REGISTER: '/api/auth/register',
    LOGIN: '/api/auth/login',
    ME: '/api/auth/me',
  },
  UPLOADS: {
    TRIAL_BALANCE: '/api/uploads/trial-balance',
    GET: (id: number) => `/api/uploads/${id}`,
  },
  REPORTS: {
    GENERATE: '/api/reports/generate',
    GET: (id: number) => `/api/reports/${id}`,
    BY_UPLOAD: (uploadId: number) => `/api/reports/upload/${uploadId}`,
  },
};
