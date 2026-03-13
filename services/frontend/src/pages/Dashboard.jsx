import { useState, useEffect } from "react";
import { profileApi } from "../lib/apiClient.js";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState(0);
  const [profiles, setProfiles] = useState([]);

  useEffect(() => {
    async function fetchProfiles() {
      try {
        const response = await profileApi.listProfilesApiProfileGet();
        setProfiles(response.data);
      } catch (error) {
        console.error("Failed to fetch profiles:", error);
      }
    }

    fetchProfiles();
  }, []);

  return (
    <>
      <div className="hero">
        <section className="card">
          <h1>Dashboard</h1>
          <p className="subtle">Welcome to your dashboard</p>
        </section>
      </div>

      <section className="card">
        <div className="tabs">
          {profiles.map((profile, index) => (
            <button
              key={index}
              className={`tab ${activeTab === index ? "active" : ""}`}
              onClick={() => setActiveTab(index)}
            >
              {profile.name}
            </button>
          ))}
        </div>
        <div className="tab-content">
          {profiles[activeTab] && <p>{profiles[activeTab].content}</p>}
        </div>
      </section>
    </>
  );
}
