import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { X } from "react-feather";

const emptyForm = {
  type: "caldav",
  url: "",
  username: "",
  password: "",
};

/**
 * CalendarModal
 *
 * Props:
 *   isOpen      – boolean, controls visibility
 *   onClose     – () => void, called when the modal should be dismissed
 *   onSave      – (payload) => void, called with the form payload on submit
 *   initialData – object | null, existing calendar data for edit mode (null = create mode)
 */
export default function CalendarModal({
  isOpen,
  onClose,
  onSave,
  initialData = null,
  allowedTypes = ["caldav", "ical"],
  helperText = "",
}) {
  const [formData, setFormData] = useState(emptyForm);
  const isEditing = !!initialData;

  // Sync form state when the modal opens or initialData changes
  useEffect(() => {
    if (!isOpen) return;
    if (initialData) {
      setFormData({
        type: initialData.type,
        url: initialData.url,
        username: initialData.username || "",
        password: initialData.password || "",
      });
    } else {
      setFormData(emptyForm);
    }
  }, [isOpen, initialData]);

  useEffect(() => {
    if (!isOpen) return;
    if (allowedTypes.includes(formData.type)) return;
    setFormData((current) => ({
      ...current,
      type: allowedTypes[0] || "caldav",
    }));
  }, [allowedTypes, formData.type, isOpen]);

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

  function handleSubmit(e) {
    e.preventDefault();
    onSave({
      type: formData.type,
      url: formData.url,
      username: formData.type === "caldav" ? formData.username || null : null,
      password: formData.type === "caldav" ? formData.password || null : null,
    });
  }

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
          <h2>{isEditing ? "Edit Calendar" : "Create Calendar"}</h2>

          <div className="form-group">
            <label>Calendar Type</label>
            <select value={formData.type} onChange={handleChange("type")}>
              {allowedTypes.includes("caldav") && (
                <option value="caldav">CalDAV</option>
              )}
              {allowedTypes.includes("ical") && (
                <option value="ical">iCal</option>
              )}
            </select>
            {helperText ? <p className="subtle">{helperText}</p> : null}
          </div>

          <div className="form-group">
            <label>Calendar URL</label>
            <input
              value={formData.url}
              onChange={handleChange("url")}
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
                  onChange={handleChange("username")}
                  placeholder="username"
                />
              </div>

              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={handleChange("password")}
                  placeholder="password"
                />
              </div>
            </div>
          )}

          <div className="actions">
            <button type="submit" className="btn btn-primary">
              {isEditing ? "Save Changes" : "Save Calendar"}
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

CalendarModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSave: PropTypes.func.isRequired,
  initialData: PropTypes.shape({
    type: PropTypes.string,
    url: PropTypes.string,
    username: PropTypes.string,
    password: PropTypes.string,
  }),
  allowedTypes: PropTypes.arrayOf(PropTypes.string),
  helperText: PropTypes.string,
};
