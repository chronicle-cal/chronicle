import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { profileApi } from "../lib/apiClient.js";

export default function Dashboard() {
  const [profiles, setProfiles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchProfiles() {
      try {
        const response = await profileApi.listProfiles();
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
          <div className="actions">
            <button
              className="btn"
              type="button"
              onClick={() => navigate("/calendar-profiles")}
            >
              Manage Profiles
            </button>
            <button
              className="btn btn-primary"
              type="button"
              onClick={() => navigate("/calendar-profiles?new=1")}
            >
              New Profile
            </button>
          </div>
        </section>
      </div>

      <div className="page-header">
        <div>
          <h2>Profiles {profiles.length > 0 && "(" + profiles.length + ")"}</h2>
          <p className="subtle">Quick overview of your calendar sync setup</p>
        </div>
      </div>

      {profiles.length === 0 ? (
        <section className="card">
          <h2>No profiles yet</h2>
          <p className="subtle">
            Create your first profile to start syncing calendars.
          </p>
          <div className="actions">
            <button
              className="btn btn-primary"
              type="button"
              onClick={() => navigate("/calendar-profiles?new=1")}
            >
              Create Profile
            </button>
          </div>
        </section>
      ) : (
        <div className="settings-grid">
          {profiles.map((profile) => (
            <section key={profile.id} className="card settings-panel">
              <div className="page-header">
                <div>
                  <h2>{profile.name}</h2>
                  <p className="subtle">Calendar sync profile</p>
                </div>
                <button
                  className="btn"
                  type="button"
                  onClick={() => navigate("/calendar-profiles")}
                >
                  Manage
                </button>
              </div>
              <div className="actions">
                <span className="pill">
                  Main:{" "}
                  {profile.main_calendar_id
                    ? `${profile.main_calendar_id.slice(0, 8)}...`
                    : "Not set"}
                </span>
                <span className="pill">ID: {profile.id.slice(0, 6)}...</span>
              </div>
            </section>
          ))}
        </div>
      )}
    </>
  );
}
