import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";
import { calendarApi, profileApi } from "../lib/apiClient.js";

export default function CreateCalendarProfile() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { addFlash } = useFlash();

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

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h1>Create Profile</h1>
          <p className="subtle">Set up a new calendar synchronisation profile</p>
        </div>
      </div>

      <div className="card">
        <form onSubmit={handleCreateProfile}>
          <div className="form-group">
            <label>Profile Name</label>
            <input
              value={newProfile.name}
              onChange={(e) =>
                setNewProfile({ ...newProfile, name: e.target.value })
              }
              placeholder="My Work Calendar"
              required
              autoFocus
            />
          </div>

          <h2>Main Calendar Configuration</h2>

          <div className="form-group">
            <label>Calendar Type</label>
            <select
              value={newProfile.main_calendar.type}
              onChange={(e) =>
                setNewProfile({
                  ...newProfile,
                  main_calendar: {
                    ...newProfile.main_calendar,
                    type: e.target.value,
                  },
                })
              }
            >
              <option value="caldav">CalDAV</option>
              <option value="ical">iCal</option>
            </select>
          </div>

          <div className="form-group">
            <label>Calendar URL</label>
            <input
              value={newProfile.main_calendar.url}
              onChange={(e) =>
                setNewProfile({
                  ...newProfile,
                  main_calendar: {
                    ...newProfile.main_calendar,
                    url: e.target.value,
                  },
                })
              }
              placeholder="https://calendar.example.com/calendar"
              required
            />
          </div>

          {newProfile.main_calendar.type === "caldav" && (
            <div className="form-row">
              <div className="form-group">
                <label>Username</label>
                <input
                  value={newProfile.main_calendar.username || ""}
                  onChange={(e) =>
                    setNewProfile({
                      ...newProfile,
                      main_calendar: {
                        ...newProfile.main_calendar,
                        username: e.target.value,
                      },
                    })
                  }
                  placeholder="username"
                />
              </div>

              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  value={newProfile.main_calendar.password || ""}
                  onChange={(e) =>
                    setNewProfile({
                      ...newProfile,
                      main_calendar: {
                        ...newProfile.main_calendar,
                        password: e.target.value,
                      },
                    })
                  }
                  placeholder="password"
                />
              </div>
            </div>
          )}

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
    </div>
  );
}
