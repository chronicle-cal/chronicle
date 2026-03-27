import React, { useState, useEffect } from "react";

function SyncConfigs() {
  const [configs, setConfigs] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    destination: "",
    username: "",
    password: "",
  });

  useEffect(() => {
    fetchConfigs();
  }, []);

  async function fetchConfigs() {
    const token = localStorage.getItem("token");
    const res = await fetch("/api/sync-configs", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      const data = await res.json();
      setConfigs(data);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const res = await fetch("/api/sync-configs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    });
    if (res.ok) {
      setShowForm(false);
      setFormData({ destination: "", username: "", password: "" });
      fetchConfigs();
    }
  }

  async function handleDelete(id) {
    const token = localStorage.getItem("token");
    const res = await fetch(`/api/sync-configs/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      fetchConfigs();
    }
  }

  return (
    <div className="hero">
      <section className="card">
        <div className="flex justify-between items-center mb-6">
          <h1>Sync Configurations</h1>
          <button onClick={() => setShowForm(!showForm)} className="pill">
            {showForm ? "Cancel" : "Add Config"}
          </button>
        </div>

        {showForm && (
          <form
            className="card"
            style={{ padding: "20px" }}
            onSubmit={handleSubmit}
          >
            <h2>Create Sync Configuration</h2>
            <div className="form">
              <label htmlFor="destination">Destination</label>
              <input
                id="destination"
                type="text"
                value={formData.destination}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    destination: e.target.value,
                  })
                }
                required
              />
              <label htmlFor="username">Username</label>
              <input
                id="username"
                type="text"
                value={formData.username}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    username: e.target.value,
                  })
                }
                required
              />
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    password: e.target.value,
                  })
                }
                required
              />
            </div>
            <div className="actions">
              <button className="btn btn-primary" type="submit">
                Save
              </button>
            </div>
          </form>
        )}

        {configs.length === 0 ? (
          <p className="subtle">
            No sync configurations yet. Create one to get started.
          </p>
        ) : (
          <div className="settings-grid">
            {configs.map((config) => (
              <div key={config.id} className="card settings-panel">
                <div className="flex justify-between items-start">
                  <div>
                    <h3>{config.destination}</h3>
                    <p className="subtle">ID: {config.id.substring(0, 8)}...</p>
                  </div>
                  <button
                    onClick={() => handleDelete(config.id)}
                    className="pill btn-danger"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default SyncConfigs;
