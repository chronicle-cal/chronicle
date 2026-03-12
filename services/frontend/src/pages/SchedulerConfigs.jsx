import { useState, useEffect } from "react";

function SchedulerConfigs() {
  const [configs, setConfigs] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    calendar_url: "",
    calendar_username: "",
    calendar_password: "",
  });

  useEffect(() => {
    fetchConfigs();
  }, []);

  async function fetchConfigs() {
    const token = localStorage.getItem("token");
    const res = await fetch("/api/scheduler-configs", {
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
    const res = await fetch("/api/scheduler-configs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    });
    if (res.ok) {
      setShowForm(false);
      setFormData({
        name: "",
        calendar_url: "",
        calendar_username: "",
        calendar_password: "",
      });
      fetchConfigs();
    }
  }

  async function handleDelete(id) {
    const token = localStorage.getItem("token");
    const res = await fetch(`/api/scheduler-configs/${id}`, {
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
          <h1>Scheduler Configurations</h1>
          <button onClick={() => setShowForm(!showForm)} className="pill">
            {showForm ? "Cancel" : "Add Config"}
          </button>
        </div>

        {showForm && (
          <form className="card" style={{"padding": "20px"}} onSubmit={handleSubmit}>
            <h2>Create Scheduler Configuration</h2>
            <div className="form">
              <label htmlFor="name">Name</label>
              <input
                id="name"
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
              <label htmlFor="calendar_url">Calendar URL</label>
              <input
                id="calendar_url"
                type="text"
                value={formData.calendar_url}
                onChange={(e) => setFormData({ ...formData, calendar_url: e.target.value })}
                required
              />
              <label htmlFor="calendar_username">Calendar Username</label>
              <input
                id="calendar_username"
                type="text"
                value={formData.calendar_username}
                onChange={(e) => setFormData({ ...formData, calendar_username: e.target.value })}
                required
              />
              <label htmlFor="calendar_password">Calendar Password</label>
              <input
                id="calendar_password"
                type="password"
                value={formData.calendar_password}
                onChange={(e) => setFormData({ ...formData, calendar_password: e.target.value })}
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
          <p className="subtle">No scheduler configurations yet. Create one to get started.</p>
        ) : (
          <div className="settings-grid">
            {configs.map((config) => (
              <div key={config.id} className="card settings-panel">
                <div className="flex justify-between items-start">
                  <div>
                    <h3>{config.name}</h3>
                    <p className="subtle">ID: {config.id.substring(0, 8)}...</p>
                    <p className="subtle">URL: {config.calendar_url}</p>
                  </div>
                  <button onClick={() => handleDelete(config.id)} className="pill btn-danger">
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

export default SchedulerConfigs;
