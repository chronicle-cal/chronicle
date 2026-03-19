import { useEffect, useState } from "react";

const emptyForm = {
  name: "",
  main_calendar_id: "",
};

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
  const [formData, setFormData] = useState(emptyForm);
  const isEditing = !!initialData;

  // Sync form state when the modal opens or initialData changes
  useEffect(() => {
    if (!isOpen) return;
    if (initialData) {
      setFormData({
        name: initialData.name || "",
        main_calendar_id: initialData.main_calendar_id || "",
      });
    } else {
      setFormData(emptyForm);
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
    return (e) => setFormData((current) => ({ ...current, [field]: e.target.value }));
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
    });
  }

  const canSubmit = formData.name.trim() && formData.main_calendar_id;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card card" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" type="button" onClick={onClose} aria-label="Close">
          x
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
            <select value={formData.main_calendar_id || ""} onChange={handleCalendarChange}>
              <option value="">-- Select or create --</option>
              {calendars.map((calendar) => (
                <option key={calendar.id} value={calendar.id}>
                  {calendar.type} — {calendar.url}
                </option>
              ))}
              <option value="new">+ Create New Calendar</option>
            </select>
            {calendars.length === 0 && (
              <p className="subtle">No calendars yet. Create one to continue.</p>
            )}
          </div>

          <div className="actions">
            <button type="submit" className="btn btn-primary" disabled={!canSubmit}>
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
