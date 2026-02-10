const API_BASE = ""; // proxy handles /api

function getToken() {
  return localStorage.getItem("token");
}

async function request(path, options = {}) {
  const token = getToken();

  const res = await fetch(`${API_BASE}${path}`, {
    method: options.method || "GET",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: options.body,
  });

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    throw new Error(data?.detail || "Request failed");
  }

  return data;
}

export function register(payload) {
  return request("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function login(payload) {
  const data = await request("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  localStorage.setItem("token", data.access_token);
  return data;
}

export async function registerAndLogin(payload) {
  const data = await register(payload);
  localStorage.setItem("token", data.access_token);
  return data;
}

export function logout() {
  return request("/api/auth/logout", { method: "POST" });
}

export function me() {
  return request("/api/auth/me");
}

export function updateEmail(payload) {
  return request("/api/auth/update-email", {
    method: "POST",
    body: JSON.stringify(payload),
  }).then((data) => {
    if (data?.access_token) {
      localStorage.setItem("token", data.access_token);
    }
    return data;
  });
}

export function updatePassword(payload) {
  return request("/api/auth/update-password", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateName(payload) {
  return request("/api/auth/update-name", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function deleteAccount(payload) {
  return request("/api/auth/delete-account", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
