import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";
import {
  CalendarApi,
  CalendarProfileApi,
  Configuration,
} from "../api-client";

const configuration = new Configuration({
  basePath: "http://localhost:8000",
});

const profileApi = new CalendarProfileApi(configuration);
const calendarApi = new CalendarApi(configuration);

export default function CalendarProfiles() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { addFlash } = useFlash();

  const [profiles, setProfiles] = useState([]);
  const [calendars, setCalendars] = useState([]);
  const [sourcesByProfile, setSourcesByProfile] = useState({});
  const [selectedCalendarByProfile, setSelectedCalendarByProfile] = useState({});
  const [loading, setLoading] = useState(true);
  const hasLoadedRef = useRef(false);

  useEffect(() => {
    if (!isAuthenticated) {
      hasLoadedRef.current = false;
      setProfiles([]);
      setCalendars([]);
      setSourcesByProfile({});
      setLoading(false);
      return;
    }

    if (hasLoadedRef.current) return;
    hasLoadedRef.current = true;
    loadAll();
  }, [isAuthenticated]);

  function getAuthHeader() {
    const token = localStorage.getItem("token");
    return token ? `Bearer ${token}` : undefined;
  }

  async function loadAll() {
    try {
      setLoading(true);
      const authHeader = getAuthHeader();

      const [profilesResponse, calendarsResponse] = await Promise.all([
        profileApi.listProfilesApiProfileGet(authHeader),
        calendarApi.listCalendarsApiCalendarGet(authHeader),
      ]);

      const loadedProfiles = profilesResponse.data;
      const loadedCalendars = calendarsResponse.data;

      setProfiles(loadedProfiles);
      setCalendars(loadedCalendars);

      const sourceEntries = await Promise.all(
        loadedProfiles.map(async (profile) => {
          const response = await profileApi.listProfileSyncApiProfileProfileIdSourceGet(
            profile.id,
            authHeader
          );
          return [profile.id, response.data];
        })
      );

      setSourcesByProfile(Object.fromEntries(sourceEntries));
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to load profiles.";
      addFlash("error", message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeleteProfile(id) {
    const profile = profiles.find((item) => item.id === id);
    const confirmed = window.confirm(
      `Delete calendar profile "${profile?.name || "this profile"}"?`
    );

    if (!confirmed) return;

    try {
      const authHeader = getAuthHeader();
      await profileApi.deleteProfileApiProfileProfileIdDelete(id, authHeader);

      setProfiles((current) => current.filter((item) => item.id !== id));

      setSourcesByProfile((current) => {
        const updated = { ...current };
        delete updated[id];
        return updated;
      });

      setSelectedCalendarByProfile((current) => {
        const updated = { ...current };
        delete updated[id];
        return updated;
      });

      addFlash("success", "Calendar profile deleted");
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to delete profile.";
      addFlash("error", message);
    }
  }

  async function handleAddSource(profileId) {
    const calendarId = selectedCalendarByProfile[profileId];
    if (!calendarId) {
      addFlash("error", "Please select a calendar first.");
      return;
    }

    try {
      const authHeader = getAuthHeader();

      await profileApi.addProfileSourceApiProfileProfileIdSourcePost(
        profileId,
        { calendar_id: calendarId },
        authHeader
      );

      const response = await profileApi.listProfileSyncApiProfileProfileIdSourceGet(
        profileId,
        authHeader
      );

      setSourcesByProfile((current) => ({
        ...current,
        [profileId]: response.data,
      }));

      setSelectedCalendarByProfile((current) => ({
        ...current,
        [profileId]: "",
      }));

      addFlash("success", "Source added");
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to add source.";
      addFlash("error", message);
    }
  }

  async function handleDeleteSource(profileId, sourceId) {
    const confirmed = window.confirm("Delete this source?");
    if (!confirmed) return;

    try {
      const authHeader = getAuthHeader();

      await profileApi.deleteProfileSourceApiProfileProfileIdSourceSourceIdDelete(
        profileId,
        sourceId,
        authHeader
      );

      setSourcesByProfile((current) => ({
        ...current,
        [profileId]: (current[profileId] || []).filter(
          (source) => source.id !== sourceId
        ),
      }));

      addFlash("success", "Source deleted");
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to delete source.";
      addFlash("error", message);
    }
  }

  async function handleTriggerSync(profileId) {
    try {
      const authHeader = getAuthHeader();
      await profileApi.triggerProfileSyncApiProfileProfileIdSyncPost(
        profileId,
        authHeader
      );
      addFlash("success", "Profile sync triggered");
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to trigger sync.";
      addFlash("error", message);
    }
  }

  function getAvailableCalendarsForProfile(profile) {
    const currentSources = sourcesByProfile[profile.id] || [];
    const usedCalendarIds = new Set([
      profile.main_calendar_id,
      ...currentSources.map((source) => source.calendar_id),
    ]);

    return calendars.filter((calendar) => !usedCalendarIds.has(calendar.id));
  }

  if (loading) {
    return <div className="loading">Loading calendar profiles...</div>;
  }

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h1>Calendar Profiles</h1>
          <p className="subtle">Manage your calendar synchronisation profiles</p>
        </div>
        <button
          className="btn btn-primary"
          onClick={() => navigate("/calendar-profiles/new")}
        >
          + Create Profile
        </button>
      </div>

      <div className="spacer" />

      {profiles.length === 0 ? (
        <div className="card empty-state">
          <div className="empty-state-content">
            <h3>No Calendar Profiles</h3>
            <p>Create your first calendar profile to get started</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate("/calendar-profiles/new")}
            >
              Create First Profile
            </button>
          </div>
        </div>
      ) : (
        profiles.map((profile) => {
          const sources = sourcesByProfile[profile.id] || [];
          const availableCalendars = getAvailableCalendarsForProfile(profile);

          return (
            <div key={profile.id} className="card">
              <div className="card-header">
                <div>
                  <h2>{profile.name}</h2>
                  <p className="subtle">
                    Profile ID: {profile.id.slice(0, 8)}...
                  </p>
                  <p className="subtle">
                    Main Calendar ID: {profile.main_calendar_id?.slice(0, 8) || "-"}...
                  </p>
                </div>

                <div className="actions">
                  <button
                    className="btn btn-small"
                    onClick={() => handleTriggerSync(profile.id)}
                  >
                    Sync Now
                  </button>
                  <button
                    className="btn btn-small btn-danger"
                    onClick={() => handleDeleteProfile(profile.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>

              <div className="card-section">
                <h3>Sources</h3>

                {sources.length === 0 ? (
                  <p className="subtle">No sources added yet.</p>
                ) : (
                  <ul className="rule-list">
                    {sources.map((source) => (
                      <li key={source.id} className="rule-item">
                        <div className="rule-info">
                          <strong>
                            {source.calendar?.url || source.calendar_id}
                          </strong>
                          <span className="subtle">
                            Calendar ID: {source.calendar_id.slice(0, 8)}...
                          </span>
                          <span className="subtle">
                            Type: {source.calendar?.type || "-"}
                          </span>
                        </div>
                        <div className="rule-actions">
                          <button
                            className="btn btn-small btn-danger"
                            onClick={() =>
                              handleDeleteSource(profile.id, source.id)
                            }
                          >
                            Delete Source
                          </button>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}

                <div className="form-row" style={{ marginTop: "1rem" }}>
                  <div className="form-group" style={{ flex: 1 }}>
                    <label>Add existing calendar as source</label>
                    <select
                      value={selectedCalendarByProfile[profile.id] || ""}
                      onChange={(e) =>
                        setSelectedCalendarByProfile((current) => ({
                          ...current,
                          [profile.id]: e.target.value,
                        }))
                      }
                    >
                      <option value="">Select a calendar</option>
                      {availableCalendars.map((calendar) => (
                        <option key={calendar.id} value={calendar.id}>
                          {calendar.type} — {calendar.url}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="actions" style={{ alignItems: "end" }}>
                    <button
                      className="btn btn-primary"
                      type="button"
                      onClick={() => handleAddSource(profile.id)}
                      disabled={availableCalendars.length === 0}
                    >
                      Add Source
                    </button>
                  </div>
                </div>

                {availableCalendars.length === 0 && (
                  <p className="subtle">
                    No additional calendars available to add as sources.
                  </p>
                )}
              </div>
            </div>
          );
        })
      )}
    </div>
  );
}
