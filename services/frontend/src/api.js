import { Configuration, AuthApi } from "./api-client";

const client = new AuthApi(
  new Configuration({
    basePath: "http://localhost:8000",
  })
);

export async function login({ email, password }) {
  const response = await client.loginApiAuthLoginPost({
    email,
    password,
  });

  const token = response.data.access_token;
  localStorage.setItem("token", token);

  return response.data;
}

export async function registerAndLogin({ email, password }) {
  await client.registerApiAuthRegisterPost({
    email,
    password,
  });

  return login({ email, password });
}

export async function logout() {
  const token = localStorage.getItem("token");

  await client.logoutApiAuthLogoutPost({
    headers: token ? { authorization: `Bearer ${token}` } : {},
  });
}

export async function me() {
  const token = localStorage.getItem("token");

  if (!token) {
    return { authenticated: false };
  }

  try {
    const response = await client.meApiAuthMeGet(`Bearer ${token}`);
    return {
      authenticated: true,
      ...response.data,
    };
  } catch {
    localStorage.removeItem("token");
    return { authenticated: false };
  }
}
