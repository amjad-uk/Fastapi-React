import { ApiError } from './types';
const API_BASE = (window.__APP_CONFIG__?.API_BASE) || '/api';
export async function http<T>(path:string, init?:RequestInit){
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, { headers: {'Content-Type':'application/json'}, ...init });
  const text = await res.text();
  const json = text ? JSON.parse(text) : undefined;
  if(!res.ok){
    const message = (json?.detail?.[0]?.msg) || json?.error || `HTTP ${res.status}`;
    throw new ApiError(message, res.status, json);
  }
  return json as T;
}
