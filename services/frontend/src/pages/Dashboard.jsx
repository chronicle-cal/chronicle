import { useState, useEffect } from "react";
import { CalendarProfileApi, Configuration } from "../api-client";

const configuration = new Configuration({
  basePath: "http://localhost:8000",
});

const profileApi = new CalendarProfileApi(configuration);

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState(0);
  const [profiles, setProfiles] = useState([]);

  useEffect(() => {
    async function fetchProfiles() {
      const token = localStorage.getItem("token");
      const authHeader = token ? `Bearer ${token}` : undefined;

      try {
        const response = await profileApi.listProfilesApiProfileGet(
          {},
          authHeader
        );
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
