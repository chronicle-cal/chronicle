import { authApi } from "./lib/apiClient.js";

export async function login({ email, password }) {
  const response = await authApi.loginApiAuthLoginPost({
    email,
    password,
  });

  const token = response.data.access_token;
  localStorage.setItem("token", token);

  return response.data;
}

export async function registerAndLogin({ email, password }) {
  await authApi.registerApiAuthRegisterPost({
    email,
    password,
  });

  return login({ email, password });
}

export async function logout() {
  await authApi.logoutApiAuthLogoutPost();
}

export async function me() {
  if (!localStorage.getItem("token")) {
    return { authenticated: false };
  }

  try {
    const response = await authApi.meApiAuthMeGet();
    return { authenticated: true, ...response.data };
  } catch {
    localStorage.removeItem("token");
    return { authenticated: false };
  }
}
