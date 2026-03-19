import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";
import { calendarApi, profileApi } from "../lib/apiClient.js";
import CalendarModal from "../components/CalendarModal.jsx";

export default function CreateCalendarProfile() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { addFlash } = useFlash();

  const [calendarModalContext, setCalendarModalContext] = useState(null); // { purpose: "main"|"source", profileId }

  const [newProfile, setNewProfile] = useState({
    name: "",
    main_calendar: {
      type: "caldav",
      url: "",
      username: "",
      password: "",
    },
  });

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, navigate]);

  async function handleCreateProfile(e) {
    e.preventDefault();

    try {
      const calendarResponse = await calendarApi.createCalendarApiCalendarPost({
        type: newProfile.main_calendar.type,
        url: newProfile.main_calendar.url,
        username: newProfile.main_calendar.username || null,
        password: newProfile.main_calendar.password || null,
      });

      const calendarId = calendarResponse.data.id;

      await profileApi.createProfileApiProfilePost({
        name: newProfile.name,
        main_calendar_id: calendarId,
      });

      addFlash("success", "Profile created");
      navigate("/calendar-profiles");
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Request failed.";
      addFlash("error", message);
    }
  }

  function handleCalendarModalSave(payload) {
    // Persist the modal payload back into the page form so submit still works.
    if (payload.type != "caldav") {
      addFlash(
        "warning",
        "Only CalDAV calendars are currently supported. Please choose a different calendar!"
      );
      setCalendarModalContext(null);
      return;
    }

    setNewProfile((current) => ({
      ...current,
      main_calendar: {
        type: payload.type,
        url: payload.url,
        username: payload.username || "",
        password: payload.password || "",
      },
    }));

    addFlash("success", "Calendar details updated");
    setCalendarModalContext(null);
  }

  function openCalendarModal() {
    setCalendarModalContext({ purpose: "main" });
  }

  const [existingCalendars, setExistingCalendars] = useState([]);
  const [loadingCalendars, setLoadingCalendars] = useState(false);

  useEffect(() => {
    async function fetchCalendars() {
      try {
        setLoadingCalendars(true);
        const response = await calendarApi.listCalendarsApiCalendarGet();
        const caldavCalendars =
          response.data.filter((cal) => cal.type === "caldav") || [];
        setExistingCalendars(caldavCalendars || []);
      } catch (error) {
        console.error("Failed to load calendars:", error);
      } finally {
        setLoadingCalendars(false);
      }
    }
    if (isAuthenticated) {
      fetchCalendars();
    }
  }, [isAuthenticated]);

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h1>Create Profile</h1>
          <p className="subtle">
            Set up a new calendar synchronisation profile
          </p>
        </div>
      </div>

      <div className="card">
        <form onSubmit={handleCreateProfile}>
          <div className="form-group">
            <label>Profile Name</label>
            <input
              value={newProfile.name}
              onChange={(e) =>
                setNewProfile({
                  ...newProfile,
                  name: e.target.value,
                })
              }
              placeholder="Work"
              required
              autoFocus
            />
          </div>

          <div className="form-group">
            <label>Main Calendar</label>
            <select
              value={newProfile.main_calendar.id || ""}
              onChange={(e) => {
                if (e.target.value === "new") {
                  openCalendarModal();
                } else {
                  const calendar = existingCalendars.find(
                    (c) => c.id === e.target.value
                  );
                  if (calendar) {
                    setNewProfile({
                      ...newProfile,
                      main_calendar: calendar,
                    });
                  }
                }
              }}
              disabled={loadingCalendars}
            >
              <option value="">-- Select or create --</option>
              {existingCalendars.map((cal) => (
                <option key={cal.id} value={cal.id}>
                  {cal.url}
                </option>
              ))}
              <option value="new">+ Create New Calendar</option>
            </select>
            <p>The calendar you choose must be a CalDAV calendar.</p>
          </div>

          <div className="actions">
            <button type="submit" className="btn btn-primary">
              Create Profile
            </button>
            <button
              type="button"
              className="btn"
              onClick={() => navigate("/calendar-profiles")}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      <CalendarModal
        isOpen={!!calendarModalContext}
        onClose={() => setCalendarModalContext(null)}
        onSave={handleCalendarModalSave}
        initialData={
          newProfile.main_calendar?.url ? newProfile.main_calendar : null
        }
      />
    </div>
  );
}
