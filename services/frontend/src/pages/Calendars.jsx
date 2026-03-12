import { useEffect, useRef, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";
import { CalendarApi, Configuration } from "../api-client";

const configuration = new Configuration({
  basePath: "http://localhost:8000",
});

const calendarApi = new CalendarApi(configuration);

const emptyForm = {
  type: "caldav",
  url: "",
  username: "",
  password: "",
};

export default function Calendars() {
  const { isAuthenticated } = useAuth();
  const { addFlash } = useFlash();

  const [calendars, setCalendars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingCalendarId, setEditingCalendarId] = useState(null);
  const [formData, setFormData] = useState(emptyForm);

  const hasLoadedRef = useRef(false);

  useEffect(() => {
    if (!isAuthenticated) {
      hasLoadedRef.current = false;
      setCalendars([]);
      setLoading(false);
      return;
    }

    if (hasLoadedRef.current) return;
    hasLoadedRef.current = true;
    loadCalendars();
  }, [isAuthenticated]);

  function getAuthHeader() {
    const token = localStorage.getItem("token");
    return token ? `Bearer ${token}` : undefined;
  }

  function resetForm() {
    setFormData(emptyForm);
    setEditingCalendarId(null);
    setShowForm(false);
  }

  async function loadCalendars() {
    try {
      setLoading(true);
      const authHeader = getAuthHeader();
      const response = await calendarApi.listCalendarsApiCalendarGet(authHeader);
      setCalendars(response.data);
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to load calendars.";
      addFlash("error", message);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      const authHeader = getAuthHeader();

      const payload = {
        type: formData.type,
        url: formData.url,
        username: formData.type === "caldav" ? formData.username || null : null,
        password: formData.type === "caldav" ? formData.password || null : null,
      };

      if (editingCalendarId) {
        const response = await calendarApi.updateCalendarApiCalendarCalendarIdPut(
          editingCalendarId,
          payload,
          authHeader
        );

        setCalendars((current) =>
          current.map((calendar) =>
            calendar.id === editingCalendarId ? response.data : calendar
          )
        );

        addFlash("success", "Calendar updated");
      } else {
        const response = await calendarApi.createCalendarApiCalendarPost(
          payload,
          authHeader
        );

        setCalendars((current) => [...current, response.data]);
        addFlash("success", "Calendar created");
      }

      resetForm();
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        (editingCalendarId
          ? "Failed to update calendar."
          : "Failed to create calendar.");
      addFlash("error", message);
    }
  }

  async function handleDelete(calendarId) {
    const calendar = calendars.find((item) => item.id === calendarId);
    const confirmed = window.confirm(
      `Delete calendar "${calendar?.url || calendarId}"?`
    );

    if (!confirmed) return;

    try {
      const authHeader = getAuthHeader();

      await calendarApi.deleteCalendarApiCalendarCalendarIdDelete(
        calendarId,
        authHeader
      );

      setCalendars((current) =>
        current.filter((item) => item.id !== calendarId)
      );

      if (editingCalendarId === calendarId) {
        resetForm();
      }

      addFlash("success", "Calendar deleted");
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to delete calendar.";
      addFlash("error", message);
    }
  }

  async function handleEdit(calendarId) {
    try {
      const authHeader = getAuthHeader();

      const response = await calendarApi.getCalendarApiCalendarCalendarIdGet(
        calendarId,
        authHeader
      );

      const calendar = response.data;

      setFormData({
        type: calendar.type,
        url: calendar.url,
        username: calendar.username || "",
        password: calendar.password || "",
      });

      setEditingCalendarId(calendar.id);
      setShowForm(true);
    } catch (error) {
      const message =
        error.response?.data?.detail || error.message || "Failed to load calendar.";
      addFlash("error", message);
    }
  }

  if (loading) {
    return <div className="loading">Loading calendars...</div>;
  }

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h1>Calendars</h1>
          <p className="subtle">Manage your calendars</p>
        </div>

        <button
          className="btn btn-primary"
          onClick={() => {
            if (showForm && !editingCalendarId) {
              resetForm();
            } else {
              setEditingCalendarId(null);
              setFormData(emptyForm);
              setShowForm(true);
            }
          }}
        >
          {showForm && !editingCalendarId ? "Cancel" : "+ Create Calendar"}
        </button>
      </div>

      <div className="spacer" />

      {showForm && (
        <div className="card">
          <form onSubmit={handleSubmit}>
            <h2>{editingCalendarId ? "Edit Calendar" : "Create Calendar"}</h2>

            <div className="form-group">
              <label>Calendar Type</label>
              <select
                value={formData.type}
                onChange={(event) =>
                  setFormData((current) => ({
                    ...current,
                    type: event.target.value,
                  }))
                }
              >
                <option value="caldav">CalDAV</option>
                <option value="ical">iCal</option>
              </select>
            </div>

            <div className="form-group">
              <label>Calendar URL</label>
              <input
                value={formData.url}
                onChange={(event) =>
                  setFormData((current) => ({
                    ...current,
                    url: event.target.value,
                  }))
                }
                placeholder="https://calendar.example.com/calendar"
                required
              />
            </div>

            {formData.type === "caldav" && (
              <div className="form-row">
                <div className="form-group">
                  <label>Username</label>
                  <input
                    value={formData.username}
                    onChange={(event) =>
                      setFormData((current) => ({
                        ...current,
                        username: event.target.value,
                      }))
                    }
                    placeholder="username"
                  />
                </div>

                <div className="form-group">
                  <label>Password</label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(event) =>
                      setFormData((current) => ({
                        ...current,
                        password: event.target.value,
                      }))
                    }
                    placeholder="password"
                  />
                </div>
              </div>
            )}

            <div className="actions">
              <button type="submit" className="btn btn-primary">
                {editingCalendarId ? "Save Changes" : "Save Calendar"}
              </button>

              <button
                type="button"
                className="btn"
                onClick={resetForm}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {calendars.length === 0 ? (
        <div className="card empty-state">
          <div className="empty-state-content">
            <h3>No Calendars</h3>
            <p>Create your first calendar to get started</p>
          </div>
        </div>
      ) : (
        calendars.map((calendar) => (
          <div key={calendar.id} className="card">
            <div className="card-header">
              <div>
                <h2>{calendar.type}</h2>
                <p className="subtle">URL: {calendar.url}</p>
                <p className="subtle">
                  Calendar ID: {calendar.id.slice(0, 8)}...
                </p>
                <p className="subtle">
                  Username: {calendar.username || "-"}
                </p>
              </div>

              <div className="actions">
                <button
                  className="btn btn-small"
                  onClick={() => handleEdit(calendar.id)}
                >
                  Edit
                </button>
                <button
                  className="btn btn-small btn-danger"
                  onClick={() => handleDelete(calendar.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
