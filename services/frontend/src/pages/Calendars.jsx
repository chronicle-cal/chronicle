import React, { useEffect, useRef, useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";
import { calendarApi } from "../lib/apiClient.js";
import CalendarModal from "../components/CalendarModal.jsx";

export default function Calendars() {
  const { isAuthenticated } = useAuth();
  const { addFlash } = useFlash();

  const [calendars, setCalendars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingCalendar, setEditingCalendar] = useState(null);

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

  function openCreateModal() {
    setEditingCalendar(null);
    setShowModal(true);
  }

  function closeModal() {
    setShowModal(false);
    setEditingCalendar(null);
  }

  async function loadCalendars() {
    try {
      setLoading(true);
      const response = await calendarApi.listCalendarsApiCalendarGet();
      setCalendars(response.data);
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to load calendars.";
      addFlash("error", message);
    } finally {
      setLoading(false);
    }
  }

  async function handleSave(payload) {
    try {
      if (editingCalendar) {
        const response =
          await calendarApi.updateCalendarApiCalendarCalendarIdPut(
            editingCalendar.id,
            payload
          );

        setCalendars((current) =>
          current.map((calendar) =>
            calendar.id === editingCalendar.id ? response.data : calendar
          )
        );

        addFlash("success", "Calendar updated");
      } else {
        const response =
          await calendarApi.createCalendarApiCalendarPost(payload);

        setCalendars((current) => [...current, response.data]);
        addFlash("success", "Calendar created");
      }

      closeModal();
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        (editingCalendar
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
      await calendarApi.deleteCalendarApiCalendarCalendarIdDelete(calendarId);

      setCalendars((current) =>
        current.filter((item) => item.id !== calendarId)
      );

      if (editingCalendar?.id === calendarId) {
        closeModal();
      }

      addFlash("success", "Calendar deleted");
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to delete calendar.";
      addFlash("error", message);
    }
  }

  async function handleEdit(calendarId) {
    try {
      const response =
        await calendarApi.getCalendarApiCalendarCalendarIdGet(calendarId);

      setEditingCalendar(response.data);
      setShowModal(true);
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to load calendar.";
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

        <button className="btn btn-primary" onClick={openCreateModal}>
          + Create Calendar
        </button>
      </div>

      <div className="spacer" />

      <CalendarModal
        isOpen={showModal}
        onClose={closeModal}
        onSave={handleSave}
        initialData={editingCalendar}
      />

      {calendars.length === 0 ? (
        <div className="card empty-state">
          <div className="empty-state-content">
            <h3>No Calendars</h3>
            <p>Create your first calendar to get started</p>
          </div>
        </div>
      ) : (
        calendars.map((calendar, index) => (
          <div key={calendar.id}>
            <div className="card">
              <div className="card-header">
                <div>
                  <h2>{calendar.type}</h2>
                  <p className="subtle">URL: {calendar.url}</p>
                  <p className="subtle">
                    Calendar ID: {calendar.id.slice(0, 8)}
                    ...
                  </p>
                  <p className="subtle">Username: {calendar.username || "-"}</p>
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
            {index < calendars.length - 1 && <div className="spacer" />}
          </div>
        ))
      )}
    </div>
  );
}
