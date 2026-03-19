import { useState, useEffect, useMemo, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";
import { calendarApi, profileApi } from "../lib/apiClient.js";
import CalendarModal from "../components/CalendarModal.jsx";

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

  // main_calendar_id editing
  const [editingMainCalendarFor, setEditingMainCalendarFor] = useState(null);
  const [mainCalendarDraft, setMainCalendarDraft] = useState({});
  // CalendarModal for creating a new calendar ("main" or "source")
  const [calendarModalContext, setCalendarModalContext] = useState(null); // { purpose: "main"|"source", profileId }

  // Precompute available (not-yet-used) calendars per profile to avoid O(n)
  // work on every render pass.
  const availableCalendarsByProfile = useMemo(() => {
    const result = {};
    for (const profile of profiles) {
      const usedIds = new Set([
        profile.main_calendar_id,
        ...(sourcesByProfile[profile.id] || []).map((s) => s.calendar_id),
      ]);
      result[profile.id] = calendars.filter((c) => !usedIds.has(c.id));
    }
    return result;
  }, [profiles, calendars, sourcesByProfile]);

  // Fast calendar lookup by id for display purposes.
  const calendarById = useMemo(
    () => Object.fromEntries(calendars.map((c) => [c.id, c])),
    [calendars]
  );

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

  async function loadAll() {
    try {
      setLoading(true);

      const [profilesResponse, calendarsResponse] = await Promise.all([
        profileApi.listProfilesApiProfileGet(),
        calendarApi.listCalendarsApiCalendarGet(),
      ]);

      const loadedProfiles = profilesResponse.data;
      const loadedCalendars = calendarsResponse.data;

      setProfiles(loadedProfiles);
      setCalendars(loadedCalendars);

      const sourceEntries = await Promise.all(
        loadedProfiles.map(async (profile) => {
          const response = await profileApi.listProfileSyncApiProfileProfileIdSourceGet(
            profile.id
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
      `Delete profile "${profile?.name || "this profile"}"?`
    );

    if (!confirmed) return;

    try {
      await profileApi.deleteProfileApiProfileProfileIdDelete(id);

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

      addFlash("success", "Profile deleted");
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
      await profileApi.addProfileSourceApiProfileProfileIdSourcePost(
        profileId,
        { calendar_id: calendarId }
      );

      const response = await profileApi.listProfileSyncApiProfileProfileIdSourceGet(
        profileId
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
      await profileApi.deleteProfileSourceApiProfileProfileIdSourceSourceIdDelete(
        profileId,
        sourceId
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

  async function handleUpdateMainCalendar(profileId) {
    const calendarId = mainCalendarDraft[profileId];
    if (!calendarId) {
      addFlash("error", "Please select a calendar.");
      return;
    }

    const profile = profiles.find((p) => p.id === profileId);

    try {
      const response = await profileApi.updateProfileApiProfileProfileIdPut(
        profileId,
        { name: profile.name, main_calendar_id: calendarId }
      );

      setProfiles((current) =>
        current.map((p) => (p.id === profileId ? { ...p, ...response.data } : p))
      );
      setEditingMainCalendarFor(null);
      addFlash("success", "Main calendar updated");
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to update profile.";
      addFlash("error", message);
    }
  }

  async function handleCalendarModalSave(payload) {
    try {
      const response = await calendarApi.createCalendarApiCalendarPost(payload);
      const newCalendar = response.data;

      setCalendars((current) => [...current, newCalendar]);

      if (calendarModalContext?.purpose === "main") {
        const { profileId } = calendarModalContext;
        const profile = profiles.find((p) => p.id === profileId);

        const updateResponse = await profileApi.updateProfileApiProfileProfileIdPut(
          profileId,
          { name: profile.name, main_calendar_id: newCalendar.id }
        );

        setProfiles((current) =>
          current.map((p) =>
            p.id === profileId ? { ...p, ...updateResponse.data } : p
          )
        );
        setEditingMainCalendarFor(null);
        addFlash("success", "Calendar created and set as main calendar");
      } else if (calendarModalContext?.purpose === "source") {
        const { profileId } = calendarModalContext;
        setMainCalendarDraft((current) => ({ ...current, [profileId]: newCalendar.id }));
        addFlash("success", "Calendar created — select it and click Add Source");
      } else {
        addFlash("success", "Calendar created");
      }

      setCalendarModalContext(null);
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to create calendar.";
      addFlash("error", message);
    }
  }

  async function handleTriggerSync(profileId) {
    try {
      await profileApi.triggerProfileSyncApiProfileProfileIdSyncPost(profileId);
      addFlash("success", "Profile sync triggered");
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to trigger sync.";
      addFlash("error", message);
    }
  }

  if (loading) {
    return <div className="loading">Loading profiles...</div>;
  }

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h1>Profiles</h1>
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
            <h3>No Profiles</h3>
            <p>Create your first profile to get started</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate("/calendar-profiles/new")}
            >
              Create First Profile
            </button>
          </div>
        </div>
      ) : (
        profiles.map((profile, index) => {
          const sources = sourcesByProfile[profile.id] || [];
          const availableCalendars = availableCalendarsByProfile[profile.id] || [];
          const mainCal = calendarById[profile.main_calendar_id];

          return (
            <div key={profile.id}>
              <div className="card">
                <div className="card-header">
                  <div>
                    <h2>{profile.name}</h2>
                    <p className="subtle">
                      Profile ID: {profile.id.slice(0, 8)}...
                    </p>
                    <div className="main-calendar-row">
                      <p className="subtle" style={{ margin: 0 }}>
                        Main Calendar:{" "}
                        <span>
                          {mainCal
                            ? `${mainCal.type} — ${mainCal.url}`
                            : profile.main_calendar_id
                            ? `${profile.main_calendar_id.slice(0, 8)}…`
                            : "—"}
                        </span>
                      </p>
                      {editingMainCalendarFor !== profile.id ? (
                        <button
                          className="btn btn-small"
                          type="button"
                          onClick={() => {
                            setMainCalendarDraft((d) => ({
                              ...d,
                              [profile.id]: profile.main_calendar_id || "",
                            }));
                            setEditingMainCalendarFor(profile.id);
                          }}
                        >
                          Change
                        </button>
                      ) : (
                        <button
                          className="btn btn-small"
                          type="button"
                          onClick={() => setEditingMainCalendarFor(null)}
                        >
                          Cancel
                        </button>
                      )}
                    </div>

                    {editingMainCalendarFor === profile.id && (
                      <div className="form-row" style={{ marginTop: "0.75rem" }}>
                        <div className="form-group" style={{ flex: 1 }}>
                          <label>Select calendar</label>
                          <select
                            value={mainCalendarDraft[profile.id] || ""}
                            onChange={(e) =>
                              setMainCalendarDraft((d) => ({
                                ...d,
                                [profile.id]: e.target.value,
                              }))
                            }
                          >
                            <option value="">— choose —</option>
                            {calendars.map((calendar) => (
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
                            onClick={() => handleUpdateMainCalendar(profile.id)}
                            disabled={!mainCalendarDraft[profile.id]}
                          >
                            Apply
                          </button>
                          <button
                            className="btn"
                            type="button"
                            onClick={() =>
                              setCalendarModalContext({ purpose: "main", profileId: profile.id })
                            }
                          >
                            + New Calendar
                          </button>
                        </div>
                      </div>
                    )}
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
              {index < profiles.length - 1 && <div className="spacer" />}
            </div>
          );
        })
      )}
      <CalendarModal
        isOpen={calendarModalContext !== null}
        onClose={() => setCalendarModalContext(null)}
        onSave={handleCalendarModalSave}
        initialData={null}
      />    </div>
  );
}
