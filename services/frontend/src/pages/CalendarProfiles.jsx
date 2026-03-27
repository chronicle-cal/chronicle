import { useState, useEffect, useMemo, useRef } from "react";
import { useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";
import { calendarApi, profileApi } from "../lib/apiClient.js";
import CalendarModal from "../components/CalendarModal.jsx";
import ProfileModal from "../components/ProfileModal.jsx";

export default function CalendarProfiles() {
  const { isAuthenticated } = useAuth();
  const { addFlash } = useFlash();
  const [searchParams, setSearchParams] = useSearchParams();

  const [profiles, setProfiles] = useState([]);
  const [calendars, setCalendars] = useState([]);
  const [sourcesByProfile, setSourcesByProfile] = useState({});
  const [selectedCalendarByProfile, setSelectedCalendarByProfile] = useState(
    {}
  );
  const [loading, setLoading] = useState(true);
  const hasLoadedRef = useRef(false);
  const [profileModalOpen, setProfileModalOpen] = useState(false);
  const [editingProfile, setEditingProfile] = useState(null);
  const [profileModalCalendarId, setProfileModalCalendarId] = useState("");

  // CalendarModal for creating a new calendar ("profile")
  const [calendarModalContext, setCalendarModalContext] = useState(null); // { purpose: "profile" }

  function openCreateProfileModal() {
    setEditingProfile(null);
    setProfileModalCalendarId("");
    setProfileModalOpen(true);
  }

  function closeProfileModal() {
    setProfileModalOpen(false);
    setEditingProfile(null);
    setProfileModalCalendarId("");
  }

  function openEditProfileModal(profile) {
    setEditingProfile(profile);
    setProfileModalCalendarId(profile.main_calendar_id || "");
    setProfileModalOpen(true);
  }

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

  useEffect(() => {
    if (!isAuthenticated) return;
    if (profileModalOpen) return;
    if (searchParams.get("new") !== "1") return;

    openCreateProfileModal();
    const nextParams = new URLSearchParams(searchParams);
    nextParams.delete("new");
    setSearchParams(nextParams, { replace: true });
  }, [isAuthenticated, profileModalOpen, searchParams, setSearchParams]);

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
          const response =
            await profileApi.listProfileSyncApiProfileProfileIdSourceGet(
              profile.id
            );
          return [profile.id, response.data];
        })
      );

      setSourcesByProfile(Object.fromEntries(sourceEntries));
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to load profiles.";
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
        error.response?.data?.detail ||
        error.message ||
        "Failed to delete profile.";
      addFlash("error", message);
    }
  }

  async function handleSaveProfile(payload) {
    if (!payload.name.trim() || !payload.main_calendar_id) {
      addFlash("error", "Please enter a name and choose a main calendar.");
      return;
    }

    const mainCalendar = calendars.find(
      (calendar) => calendar.id === payload.main_calendar_id
    );
    if (!mainCalendar || mainCalendar.type !== "caldav") {
      addFlash(
        "error",
        "Profiles can only use CalDAV calendars as the main calendar."
      );
      return;
    }

    try {
      if (editingProfile) {
        const response = await profileApi.updateProfileApiProfileProfileIdPut(
          editingProfile.id,
          {
            name: payload.name.trim(),
            main_calendar_id: payload.main_calendar_id,
          }
        );

        setProfiles((current) =>
          current.map((p) =>
            p.id === editingProfile.id ? { ...p, ...response.data } : p
          )
        );
        addFlash("success", "Profile updated");
      } else {
        const response = await profileApi.createProfileApiProfilePost({
          name: payload.name.trim(),
          main_calendar_id: payload.main_calendar_id,
        });

        const created = response.data;
        setProfiles((current) => [...current, created]);
        setSourcesByProfile((current) => ({ ...current, [created.id]: [] }));
        setSelectedCalendarByProfile((current) => ({
          ...current,
          [created.id]: "",
        }));
        addFlash("success", "Profile created");
      }

      closeProfileModal();
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to save profile.";
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

      const response =
        await profileApi.listProfileSyncApiProfileProfileIdSourceGet(profileId);

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
        error.response?.data?.detail ||
        error.message ||
        "Failed to add source.";
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
        error.response?.data?.detail ||
        error.message ||
        "Failed to delete source.";
      addFlash("error", message);
    }
  }

  async function handleCalendarModalSave(payload) {
    try {
      const response = await calendarApi.createCalendarApiCalendarPost(payload);
      const newCalendar = response.data;

      setCalendars((current) => [...current, newCalendar]);

      if (calendarModalContext?.purpose === "profile") {
        setProfileModalCalendarId(newCalendar.id);
        addFlash("success", "Calendar created");
      } else {
        addFlash("success", "Calendar created");
      }

      setCalendarModalContext(null);
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to create calendar.";
      addFlash("error", message);
    }
  }

  async function handleTriggerSync(profileId) {
    try {
      await profileApi.triggerProfileSyncApiProfileProfileIdSyncPost(profileId);
      addFlash("success", "Profile sync triggered");
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to trigger sync.";
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
          <h1>Profiles {profiles.length > 0 && "(" + profiles.length + ")"}</h1>
          <p className="subtle">
            Manage your calendar synchronisation profiles
          </p>
        </div>
        <button className="btn btn-primary" onClick={openCreateProfileModal}>
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
              onClick={openCreateProfileModal}
            >
              Create First Profile
            </button>
          </div>
        </div>
      ) : (
        profiles.map((profile, index) => {
          const sources = sourcesByProfile[profile.id] || [];
          const availableCalendars =
            availableCalendarsByProfile[profile.id] || [];
          const mainCal = calendarById[profile.main_calendar_id];

          return (
            <div key={profile.id}>
              <div className="card">
                <div className="card-header">
                  <div>
                    <h2>{profile.name}</h2>
                    <p className="subtle">Profile ID: {profile.id}</p>
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
                    </div>
                  </div>

                  <div className="actions">
                    <button
                      className="btn btn-small"
                      onClick={() => openEditProfileModal(profile)}
                    >
                      Edit
                    </button>
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

                <div className="spacer" />
                <hr></hr>

                <div className="card-section">
                  <h3>Sources ({sources.length})</h3>

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
      <ProfileModal
        isOpen={profileModalOpen}
        onClose={closeProfileModal}
        onSave={handleSaveProfile}
        initialData={editingProfile}
        calendars={calendars}
        onRequestCalendarCreate={() =>
          setCalendarModalContext({ purpose: "profile" })
        }
        externalCalendarId={profileModalCalendarId}
      />
      <CalendarModal
        isOpen={calendarModalContext !== null}
        onClose={() => setCalendarModalContext(null)}
        onSave={handleCalendarModalSave}
        initialData={null}
        allowedTypes={
          calendarModalContext?.purpose === "profile"
            ? ["caldav"]
            : ["caldav", "ical"]
        }
        helperText={
          calendarModalContext?.purpose === "profile"
            ? "Profiles can only use CalDAV calendars as their main calendar."
            : ""
        }
      />
    </div>
  );
}
