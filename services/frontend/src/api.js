import { authApi } from "./lib/apiClient.js";

export async function login({ email, password }) {
  const response = await authApi.login({
    email,
    password,
  });

  const token = response.data.access_token;
  localStorage.setItem("token", token);

  return response.data;
}

export async function registerAndLogin({ email, password }) {
  await authApi.register({
    email,
    password,
  });

  return login({ email, password });
}

export async function logout() {
  await authApi.logout();
}

export async function me() {
  if (!localStorage.getItem("token")) {
    return { authenticated: false };
  }

  try {
    const response = await authApi.me();
    return { authenticated: true, ...response.data };
  } catch {
    localStorage.removeItem("token");
    return { authenticated: false };
  }
}
