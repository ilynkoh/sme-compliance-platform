import api from './api';
import { API_ENDPOINTS } from '../config/api';

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export const authService = {
  register: async (email: string, password: string, fullName: string, phone?: string) => {
    const response = await api.post(API_ENDPOINTS.AUTH.REGISTER, {
      email,
      password,
      full_name: fullName,
      phone,
    });
    return response.data as User;
  },

  login: async (email: string, password: string) => {
    const response = await api.post(API_ENDPOINTS.AUTH.LOGIN, {
      email,
      password,
    });
    const data = response.data as LoginResponse;
    localStorage.setItem('access_token', data.access_token);
    return data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  getCurrentUser: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const response = await api.get(API_ENDPOINTS.AUTH.ME);
      return response.data as User;
    } catch {
      return null;
    }
  },
};
