import axios from "axios";
import {
  Configuration,
  AuthApi,
  CalendarApi,
  CalendarProfileApi,
} from "../api-client";

const axiosInstance = axios.create();

// Automatically attach the Bearer token to every request so no component
// needs to read localStorage or pass an auth header manually.
axiosInstance.interceptors.request.use((config) => {
  if (!config.headers.authorization) {
    const token = localStorage.getItem("token");
    if (token) config.headers.authorization = `Bearer ${token}`;
  }
  return config;
});

// basePath falls back to "" so the Vite dev proxy (/api → localhost:8000)
// handles routing in development; set VITE_API_BASE_URL in production.
const configuration = new Configuration({
  basePath: import.meta.env.VITE_API_BASE_URL ?? "",
});

export const authApi = new AuthApi(configuration, undefined, axiosInstance);
export const calendarApi = new CalendarApi(
  configuration,
  undefined,
  axiosInstance
);
export const profileApi = new CalendarProfileApi(
  configuration,
  undefined,
  axiosInstance
);
