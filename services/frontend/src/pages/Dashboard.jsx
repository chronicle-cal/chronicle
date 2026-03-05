import { useState } from "react";
import SyncConfigs from "./SyncConfigs.jsx";
import SchedulerConfigs from "./SchedulerConfigs.jsx";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("sync");

  return (
    <>
      <div className="hero">
        <section className="card">
          <h1>Dashboard</h1>
          <p className="subtle">Manage your sync and scheduler configurations</p>

          <div style={{ marginTop: "20px" }} className="nav-links">
            <button
              onClick={() => setActiveTab("sync")}
              className="pill"
              style={{
                background: activeTab === "sync"
                  ? "linear-gradient(135deg, var(--accent), var(--accent-2))"
                  : "",
                color: activeTab === "sync" ? "#ffffff" : "",
              }}
            >
              Sync Configurations
            </button>
            <button
              onClick={() => setActiveTab("scheduler")}
              className="pill"
              style={{
                background: activeTab === "scheduler"
                  ? "linear-gradient(135deg, var(--accent), var(--accent-2))"
                  : "",
                color: activeTab === "scheduler" ? "#ffffff" : "",
              }}
            >
              Scheduler Configurations
            </button>
          </div>
        </section>
      </div>

      {activeTab === "sync" && <SyncConfigs />}
      {activeTab === "scheduler" && <SchedulerConfigs />}
    </>
  );
}
