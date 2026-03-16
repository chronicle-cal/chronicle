import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";

async function request(path, options = {}) {
  const token = localStorage.getItem("token");

  let res;
  try {
    res = await fetch(`/api${path}`, {
      method: options.method || "GET",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: options.body ? JSON.stringify(options.body) : undefined,
    });
  } catch (err) {
    throw new Error("Network error");
  }

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    throw new Error(data?.detail ? `${res.status}: ${data.detail}` : `Request failed (${res.status})`);
  }

  return data;
}

export default function CreateCalendarProfile() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { addFlash } = useFlash();
  const [newProfile, setNewProfile] = useState({
    name: "",
    main_calendar: {
      type: "",
      url: "",
      username: "",
      password: "",
    },
  });
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState("");

  const updateProfile = (patch) => {
    setNewProfile((prev) => ({ ...prev, ...patch }));
  };

  const updateMainCalendar = (patch) => {
    setNewProfile((prev) => ({
      ...prev,
      main_calendar: { ...prev.main_calendar, ...patch },
    }));
  };

  const clearError = (key) => {
    setErrors((prev) => {
      if (!prev[key]) return prev;
      const next = { ...prev };
      delete next[key];
      return next;
    });
  };

  const validate = (profile) => {
    const nextErrors = {};
    if (!profile.name.trim()) nextErrors.name = "Please enter a profile name.";
    if (!profile.main_calendar.type) nextErrors.type = "Please choose a calendar type.";
    if (!profile.main_calendar.url.trim()) nextErrors.url = "Please enter a calendar URL.";

    if (profile.main_calendar.type === "caldav") {
      if (!profile.main_calendar.username?.trim()) {
        nextErrors.username = "Please enter a CalDAV username.";
      }
      if (!profile.main_calendar.password?.trim()) {
        nextErrors.password = "Please enter a CalDAV password.";
      }
    }

    return nextErrors;
  };

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, navigate]);

  async function handleCreateProfile(e) {
    e.preventDefault();
    try {
      const nextErrors = validate(newProfile);
      if (Object.keys(nextErrors).length > 0) {
        setErrors(nextErrors);
        setSubmitError("");
        return;
      }

      setErrors({});
      setSubmitError("");
      await request("/profile", {
        method: "POST",
        body: newProfile,
      });
      addFlash("success", "Calendar profile created");
      navigate("/calendar-profiles");
    } catch (err) {
      setSubmitError(err.message || "Create failed.");
    }
  }

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h1>Create Calendar Profile</h1>
          <p className="subtle">Set up a new calendar synchronisation profile</p>
        </div>
      </div>

      <div className="card">
        <form className="form form-detailed" onSubmit={handleCreateProfile} noValidate>
          {submitError && <div className="form-error">{submitError}</div>}
          <div className="form-group">
            <label>Profile Name</label>
            <input
              value={newProfile.name}
              onChange={(e) => {
                updateProfile({ name: e.target.value });
                clearError("name");
              }}
              placeholder="My Work Calendar"
              required
              autoFocus
            />
            {errors.name && <div className="field-error">{errors.name}</div>}
          </div>

          <div className="form-section">
            <h2>Calendar Configuration</h2>
            <p className="subtle">
              Connect a calendar so Chronicle can sync it.
            </p>

            <div className="form-group">
              <label>Calendar Type</label>
              <select
                value={newProfile.main_calendar.type}
                onChange={(e) => {
                  updateMainCalendar({ type: e.target.value });
                  clearError("type");
                }}
                required
              >
                <option value="" disabled>
                  Choose calendar type
                </option>
                <option value="caldav">CalDAV</option>
                <option value="ical">iCal</option>
              </select>
              {errors.type && <div className="field-error">{errors.type}</div>}
            </div>

            {newProfile.main_calendar.type && (
              <>
                <div className="form-group">
                  <label>Calendar URL</label>
                  <input
                    value={newProfile.main_calendar.url}
                    onChange={(e) => {
                      updateMainCalendar({ url: e.target.value });
                      clearError("url");
                    }}
                    placeholder="https://calendar.example.com/calendar"
                    required
                  />
                  {errors.url && <div className="field-error">{errors.url}</div>}
                </div>

                {newProfile.main_calendar.type === "caldav" && (
                  <div className="form-row">
                    <div className="form-group">
                      <label>Username</label>
                      <input
                        value={newProfile.main_calendar.username || ""}
                        onChange={(e) => {
                          updateMainCalendar({ username: e.target.value });
                          clearError("username");
                        }}
                        placeholder="username"
                        required={newProfile.main_calendar.type === "caldav"}
                      />
                      {errors.username && (
                        <div className="field-error">{errors.username}</div>
                      )}
                    </div>

                    <div className="form-group">
                      <label>Password</label>
                      <input
                        type="password"
                        value={newProfile.main_calendar.password || ""}
                        onChange={(e) => {
                          updateMainCalendar({ password: e.target.value });
                          clearError("password");
                        }}
                        placeholder="password"
                        required={newProfile.main_calendar.type === "caldav"}
                      />
                      {errors.password && (
                        <div className="field-error">{errors.password}</div>
                      )}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>

          <div className="actions">
            <button type="submit" className="btn btn-primary">
              Create Calendar Profile
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
    </div>
  );
}
