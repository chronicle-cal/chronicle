import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useFlash } from "../context/FlashContext.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import * as api from "../api.js";

export default function Profile() {
  const { addFlash } = useFlash();
  const { user, refreshUser, logout } = useAuth();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState(user?.email || "");
  const [loading, setLoading] = useState(true);

  const [nameValue, setNameValue] = useState("");
  const [namePassword, setNamePassword] = useState("");

  const [newEmail, setNewEmail] = useState("");
  const [emailPassword, setEmailPassword] = useState("");

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [deleteConfirm, setDeleteConfirm] = useState("");

  useEffect(() => {
    if (!user) {
      refreshUser().finally(() => setLoading(false));
      return;
    }
    setLoading(false);
    setName(user.name || "");
    setEmail(user.email || "");
    setNameValue(user.name || "");
  }, [user, refreshUser]);

  const onUpdateName = async (event) => {
    event.preventDefault();
    try {
      await api.updateName({
        name: nameValue,
        password: namePassword,
      });
      await refreshUser();
      setNamePassword("");
      addFlash("success", "Name updated.");
    } catch (error) {
      addFlash("error", error.message || "Name update failed.");
    }
  };

  const onUpdateEmail = async (event) => {
    event.preventDefault();
    try {
      await api.updateEmail({
        new_email: newEmail,
        password: emailPassword,
      });
      await refreshUser();
      setNewEmail("");
      setEmailPassword("");
      addFlash("success", "Email updated.");
    } catch (error) {
      addFlash("error", error.message || "Email update failed.");
    }
  };

  const onUpdatePassword = async (event) => {
    event.preventDefault();
    try {
      await api.updatePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });
      setCurrentPassword("");
      setNewPassword("");
      addFlash("success", "Password updated.");
    } catch (error) {
      addFlash("error", error.message || "Password update failed.");
    }
  };

  const onDeleteAccount = async (event) => {
    event.preventDefault();
    try {
      await api.deleteAccount({ confirm: deleteConfirm });
      await logout();
      addFlash("success", "Account deleted.");
      navigate("/login");
    } catch (error) {
      addFlash("error", error.message || "Delete failed.");
    }
  };

  return (
    <div className="hero">
      <section className="card">
        <h1>Edit Profile</h1>
        <p className="subtle">
          {loading
            ? "Loading..."
            : `Name: ${user?.name || name || "-"} | Email: ${user?.email || "-"}`}
        </p>

        <div className="settings-grid">
          <form className="card settings-panel" onSubmit={onUpdateName}>
            <h2>Change Name</h2>
            <div className="form">
              <label htmlFor="profileName">New name</label>
              <input
                id="profileName"
                type="text"
                value={nameValue}
                onChange={(e) => setNameValue(e.target.value)}
                required
              />
              <label htmlFor="profileNamePassword">Password</label>
              <input
                id="profileNamePassword"
                type="password"
                value={namePassword}
                onChange={(e) => setNamePassword(e.target.value)}
                required
              />
            </div>
            <div className="actions">
              <button className="btn btn-primary" type="submit">
                Save
              </button>
            </div>
          </form>

          <form className="card settings-panel" onSubmit={onUpdateEmail}>
            <h2>Change Email</h2>
            <div className="form">
              <label htmlFor="profileCurrentEmail">Current email</label>
              <input
                id="profileCurrentEmail"
                type="email"
                value={email}
                readOnly
              />
              <label htmlFor="profileNewEmail">New email</label>
              <input
                id="profileNewEmail"
                type="email"
                value={newEmail}
                onChange={(e) => setNewEmail(e.target.value)}
                required
              />
              <label htmlFor="profileEmailPassword">Password</label>
              <input
                id="profileEmailPassword"
                type="password"
                value={emailPassword}
                onChange={(e) => setEmailPassword(e.target.value)}
                required
              />
            </div>
            <div className="actions">
              <button className="btn btn-primary" type="submit">
                Save
              </button>
            </div>
          </form>

          <form className="card settings-panel" onSubmit={onUpdatePassword}>
            <h2>Change Password</h2>
            <div className="form">
              <label htmlFor="profileCurrentPassword">Current password</label>
              <input
                id="profileCurrentPassword"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                required
              />
              <label htmlFor="profileNewPassword">New password</label>
              <input
                id="profileNewPassword"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
            </div>
            <div className="actions">
              <button className="btn btn-primary" type="submit">
                Save
              </button>
            </div>
          </form>

          <form className="card settings-panel" onSubmit={onDeleteAccount}>
            <h2>Delete Profile</h2>
            <p className="subtle">
              Type <strong>delete</strong> to permanently remove your account.
            </p>
            <div className="form">
              <label htmlFor="deleteConfirm">Confirmation</label>
              <input
                id="deleteConfirm"
                type="text"
                value={deleteConfirm}
                onChange={(e) => setDeleteConfirm(e.target.value)}
                placeholder="delete"
                required
              />
            </div>
            <div className="actions">
              <button className="btn btn-danger" type="submit">
                Delete Account
              </button>
            </div>
          </form>
        </div>
      </section>
    </div>
  );
}
