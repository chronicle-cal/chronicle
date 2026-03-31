import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { X } from "react-feather";

/**
 * ProfileModal
 *
 * Props:
 *   isOpen               – boolean, controls visibility
 *   onClose              – () => void, called when the modal should be dismissed
 *   onSave               – (payload) => void, called with the form payload on submit
 *   initialData          – object | null, existing profile data for edit mode (null = create mode)
 *   calendars            – array, available calendars for selection
 *   onRequestCalendarCreate – () => void, called when the user wants to create a new calendar
 *   externalCalendarId   – string | null, optional calendar id to preselect (e.g. after creating a calendar)
 */
export default function ProfileModal({
  isOpen,
  onClose,
  onSave,
  initialData = null,
  calendars,
  onRequestCalendarCreate,
  externalCalendarId = null,
}) {
  const workdayStartOptions = Array.from({ length: 24 }, (_, hour) => ({
    value: String(hour),
    label: `${String(hour).padStart(2, "0")}:00`,
  }));
  const workdayEndOptions = Array.from({ length: 24 }, (_, index) => {
    const hour = index + 1;
    return {
      value: String(hour),
      label: `${String(hour).padStart(2, "0")}:00`,
    };
  });

  function createEmptyForm() {
    // profil default vals
    return {
      name: "",
      main_calendar_id: "",
      workday_start_hour: "9",
      workday_end_hour: "17",
    };
  }

  const [formData, setFormData] = useState(createEmptyForm);
  const isEditing = !!initialData;
  const mainCalendarOptions = calendars.filter(
    (calendar) => calendar.type === "caldav"
  );

  // Sync form state when the modal opens or initialData changes
  useEffect(() => {
    if (!isOpen) return;
    if (initialData) {
      setFormData({
        name: initialData.name || "",
        main_calendar_id: initialData.main_calendar_id || "",
        workday_start_hour: String(initialData.workday_start_hour ?? 9),
        workday_end_hour: String(initialData.workday_end_hour ?? 17),
      });
    } else {
      setFormData(createEmptyForm());
    }
  }, [isOpen, initialData]);

  // Allow external calendar selection (e.g. after creating a calendar)
  useEffect(() => {
    if (!isOpen) return;
    if (!externalCalendarId) return;
    setFormData((current) => ({
      ...current,
      main_calendar_id: externalCalendarId,
    }));
  }, [isOpen, externalCalendarId]);

  // Close on Escape key
  useEffect(() => {
    if (!isOpen) return;
    function handleKey(e) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  function handleChange(field) {
    return (e) =>
      setFormData((current) => ({ ...current, [field]: e.target.value }));
  }

  function handleCalendarChange(e) {
    const value = e.target.value;
    if (value === "new") {
      onRequestCalendarCreate();
      return;
    }
    setFormData((current) => ({ ...current, main_calendar_id: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSave({
      name: formData.name.trim(),
      main_calendar_id: formData.main_calendar_id,
      workday_start_hour: Number(formData.workday_start_hour),
      workday_end_hour: Number(formData.workday_end_hour),
    });
  }

  const workdayStartHour = Number(formData.workday_start_hour);
  const workdayEndHour = Number(formData.workday_end_hour);
  const hasValidWorkday = workdayEndHour > workdayStartHour;
  const canSubmit =
    formData.name.trim() && formData.main_calendar_id && hasValidWorkday;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card card" onClick={(e) => e.stopPropagation()}>
        <button
          className="modal-close"
          type="button"
          onClick={onClose}
          aria-label="Close"
        >
          <X className="modal-close-icon" aria-hidden="true" />
        </button>

        <form onSubmit={handleSubmit}>
          <h2>{isEditing ? "Edit Profile" : "Create Profile"}</h2>

          <div className="form-group">
            <label>Profile Name</label>
            <input
              value={formData.name}
              onChange={handleChange("name")}
              placeholder="Work"
              required
              autoFocus
            />
          </div>

          <div className="form-group">
            <label>Main Calendar</label>
            <select
              value={formData.main_calendar_id || ""}
              onChange={handleCalendarChange}
            >
              <option value="">-- Select or create --</option>
              {mainCalendarOptions.map((calendar) => (
                <option key={calendar.id} value={calendar.id}>
                  {calendar.type} — {calendar.url}
                </option>
              ))}
              <option value="new">Create New Calendar</option>
            </select>
            <p className="subtle">
              Only CalDAV calendars can be used as a profile&apos;s main
              calendar, because scheduled events cannot be written back to
              linked calendars otherwise.
            </p>
            {mainCalendarOptions.length === 0 && (
              <p className="subtle">
                No calendars yet. Create one to continue.
              </p>
            )}
          </div>

          <div>
            <label>Scheduling Window</label>
            <p className="subtle" style={{ marginTop: "0.35rem" }}>
              The scheduler places tasks within this time window for the
              profile.
            </p>
          </div>

          <div className="form-row">
            <div className="form-group" style={{ flex: 1 }}>
              <label>Start Time</label>
              <select
                value={formData.workday_start_hour}
                onChange={handleChange("workday_start_hour")}
              >
                {workdayStartOptions.map((hour) => (
                  <option key={hour.value} value={hour.value}>
                    {hour.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ flex: 1 }}>
              <label>End Time</label>
              <select
                value={formData.workday_end_hour}
                onChange={handleChange("workday_end_hour")}
              >
                {workdayEndOptions.map((hour) => (
                  <option key={hour.value} value={hour.value}>
                    {hour.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {!hasValidWorkday ? (
            <p className="subtle">
              Workday end must be later than workday start.
            </p>
          ) : null}

          <div className="actions">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={!canSubmit}
            >
              {isEditing ? "Save Changes" : "Create Profile"}
            </button>
            <button type="button" className="btn" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

ProfileModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSave: PropTypes.func.isRequired,
  initialData: PropTypes.shape({
    name: PropTypes.string,
    main_calendar_id: PropTypes.string,
    workday_start_hour: PropTypes.number,
    workday_end_hour: PropTypes.number,
  }),
  calendars: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      type: PropTypes.string.isRequired,
      url: PropTypes.string.isRequired,
    })
  ).isRequired,
  onRequestCalendarCreate: PropTypes.func.isRequired,
  externalCalendarId: PropTypes.string,
};
