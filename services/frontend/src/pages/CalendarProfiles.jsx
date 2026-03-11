import { useState, useEffect, useRef } from "react";
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

export default function CalendarProfiles() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { addFlash } = useFlash();
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingRule, setEditingRule] = useState(null);
  const [viewingRule, setViewingRule] = useState(null);
  const hasLoadedRef = useRef(false);

  const emptyRule = {
    enabled: true,
    name: "",
    conditions: [],
    actions: [],
  };

  const [ruleDraft, setRuleDraft] = useState(emptyRule);

  useEffect(() => {
    if (!isAuthenticated) {
      hasLoadedRef.current = false;
      return;
    }
    if (hasLoadedRef.current) return;
    hasLoadedRef.current = true;
    loadProfiles();
  }, [isAuthenticated]);

  async function loadProfiles() {
    try {
      const data = await request("/profile");
      setProfiles(data);
    } catch (err) {
      addFlash("error", err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeleteProfile(id) {
    const profile = profiles.find(p => p.id === id);
    if (!confirm(`Delete calendar profile "${profile?.name || "this profile"}"?`)) return;

    try {
      await request(`/profile/${id}`, { method: "DELETE" });
      addFlash("success", "Calendar profile deleted");
      loadProfiles();
    } catch (err) {
      addFlash("error", err.message);
    }
  }

  function normalizeConditions(conditions = []) {
    return conditions.map((cond) => ({
      field: cond.field || "title",
      operator: cond.operator || "starts_with",
      value: cond.value || "",
    }));
  }

  function normalizeActions(actions = []) {
    return actions.map((action) => ({
      name: action.name || "set_field",
      arguments: {
        name: action.arguments?.name || "",
        value: action.arguments?.value || "",
      },
    }));
  }

  function startCreateRule(profileId) {
    setEditingRule({ profileId, ruleId: null });
    setRuleDraft({ ...emptyRule });
  }

  function startEditRule(profileId, rule) {
    setEditingRule({ profileId, ruleId: rule.id });
    setRuleDraft({
      enabled: rule.enabled ?? true,
      name: rule.name ?? "",
      source_id: rule.source_id,
      conditions: normalizeConditions(rule.conditions),
      actions: normalizeActions(rule.actions),
    });
  }

  async function handleCreateRule(profileId, e) {
    e.preventDefault();
    try {
      await request(`/profile/${profileId}/rule`, {
        method: "POST",
        body: ruleDraft,
      });
      addFlash("success", "Rule created");
      setEditingRule(null);
      setRuleDraft({ ...emptyRule });
      loadProfiles();
    } catch (err) {
      addFlash("error", err.message);
    }
  }

  async function handleUpdateRule(profileId, ruleId, e) {
    e.preventDefault();
    try {
      await request(`/profile/${profileId}/rule/${ruleId}`, {
        method: "POST",
        body: ruleDraft,
      });
      addFlash("success", "Rule updated");
      setEditingRule(null);
      setRuleDraft({ ...emptyRule });
      loadProfiles();
    } catch (err) {
      addFlash("error", err.message);
    }
  }

  async function handleDeleteRule(profileId, ruleId) {
    if (!confirm("Delete this rule?")) return;
    try {
      await request(`/profile/${profileId}/rule/${ruleId}`, {
        method: "DELETE",
      });
      addFlash("success", "Rule deleted");
      setViewingRule(null);
      loadProfiles();
    } catch (err) {
      addFlash("error", err.message);
    }
  }

  function addCondition() {
    setRuleDraft({
      ...ruleDraft,
      conditions: [
        ...ruleDraft.conditions,
        { field: "title", operator: "starts_with", value: "" },
      ],
    });
  }

  function updateCondition(index, field, value) {
    const updated = [...ruleDraft.conditions];
    updated[index] = { ...updated[index], [field]: value };
    setRuleDraft({ ...ruleDraft, conditions: updated });
  }

  function removeCondition(index) {
    setRuleDraft({
      ...ruleDraft,
      conditions: ruleDraft.conditions.filter((_, i) => i !== index),
    });
  }

  function addAction() {
    setRuleDraft({
      ...ruleDraft,
      actions: [
        ...ruleDraft.actions,
        { name: "set_field", arguments: { name: "", value: "" } },
      ],
    });
  }

  function updateAction(index, field, value) {
    const updated = [...ruleDraft.actions];
    if (field === "name") {
      updated[index] = { ...updated[index], name: value };
    } else {
      updated[index] = {
        ...updated[index],
        arguments: { ...updated[index].arguments, [field]: value },
      };
    }
    setRuleDraft({ ...ruleDraft, actions: updated });
  }

  function removeAction(index) {
    setRuleDraft({
      ...ruleDraft,
      actions: ruleDraft.actions.filter((_, i) => i !== index),
    });
  }

  if (loading) return <div className="loading">Loading calendar profiles...</div>;

  return (
    <div className="container">
      <div className="page-header">
        <div>
          <h1>Calendar Profiles</h1>
          <p className="subtle">Manage your calendar synchronisation profiles</p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate("/calendar-profiles/new")}>
          + Create Profile
        </button>
      </div>

      <div className="spacer" />

      {profiles.length === 0 && (
        <div className="card empty-state">
          <div className="empty-state-content">
            <h3>No Calendar Profiles</h3>
            <p>Create your first calendar profile to get started</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate("/calendar-profiles/new")}
            >
              Create First Profile
            </button>
          </div>
        </div>
      )}

      {profiles.map((profile) => (
        <div key={profile.id} className="card">
          <div className="card-header">
            <div>
              <h2>{profile.name}</h2>
              <p className="subtle">
                Calendar ID: {profile.main_calendar_id?.slice(0, 8)}...
              </p>
            </div>
            <button
              className="btn btn-small btn-danger"
              onClick={() => handleDeleteProfile(profile.id)}
            >
              Delete
            </button>
          </div>

          <div className="card-section">
            <h3>Rules & Filters</h3>
            {editingRule?.profileId === profile.id ? (
              <form
                onSubmit={(e) =>
                  editingRule.ruleId
                    ? handleUpdateRule(profile.id, editingRule.ruleId, e)
                    : handleCreateRule(profile.id, e)
                }
              >
                <div className="form-group">
                  <label>Rule Name</label>
                  <input
                    value={ruleDraft.name}
                    onChange={(e) =>
                      setRuleDraft({ ...ruleDraft, name: e.target.value })
                    }
                    placeholder="Remove unwanted events"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={ruleDraft.enabled}
                      onChange={(e) =>
                        setRuleDraft({ ...ruleDraft, enabled: e.target.checked })
                      }
                    />
                    <span>Enabled</span>
                  </label>
                </div>

                <h4>Conditions (AND - all must match)</h4>
                {ruleDraft.conditions.map((cond, idx) => (
                  <div key={idx} className="rule-item">
                    <select
                      value={cond.field}
                      onChange={(e) =>
                        updateCondition(idx, "field", e.target.value)
                      }
                    >
                      <option value="title">Title</option>
                      <option value="description">Description</option>
                      <option value="location">Location</option>
                    </select>
                    <select
                      value={cond.operator}
                      onChange={(e) =>
                        updateCondition(idx, "operator", e.target.value)
                      }
                    >
                      <option value="starts_with">Starts with</option>
                      <option value="contains">Contains</option>
                      <option value="equals">Equals</option>
                    </select>
                    <input
                      value={cond.value}
                      onChange={(e) =>
                        updateCondition(idx, "value", e.target.value)
                      }
                      placeholder="Value"
                    />
                    <button
                      type="button"
                      className="btn btn-small btn-danger"
                      onClick={() => removeCondition(idx)}
                    >
                      ✕
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  className="btn btn-small"
                  onClick={addCondition}
                >
                  + Add Condition
                </button>

                <h4>Actions</h4>
                {ruleDraft.actions.map((action, idx) => (
                  <div key={idx} className="rule-item">
                    <select
                      value={action.name}
                      onChange={(e) => updateAction(idx, "name", e.target.value)}
                    >
                      <option value="set_field">Set Field</option>
                      <option value="remove_field">Remove Field</option>
                    </select>
                    <input
                      value={action.arguments.name || ""}
                      onChange={(e) =>
                        updateAction(idx, "name", e.target.value)
                      }
                      placeholder="Field name"
                    />
                    <input
                      value={action.arguments.value || ""}
                      onChange={(e) =>
                        updateAction(idx, "value", e.target.value)
                      }
                      placeholder="Field value"
                    />
                    <button
                      type="button"
                      className="btn btn-small btn-danger"
                      onClick={() => removeAction(idx)}
                    >
                      ✕
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  className="btn btn-small"
                  onClick={addAction}
                >
                  + Add Action
                </button>

                <div className="actions">
                  <button type="submit" className="btn btn-primary">
                    {editingRule.ruleId ? "Update Rule" : "Save Rule"}
                  </button>
                  <button
                    type="button"
                    className="btn"
                    onClick={() => {
                      setEditingRule(null);
                      setRuleDraft({ ...emptyRule });
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            ) : (
              <>
                <button
                  className="btn btn-small"
                  onClick={() => startCreateRule(profile.id)}
                >
                  + Add Rule
                </button>
                {profile.rules && profile.rules.length > 0 ? (
                  <ul className="rule-list">
                    {profile.rules.map((rule) => (
                      <li key={rule.id} className="rule-item">
                        <div className="rule-info">
                          <strong>{rule.name}</strong>
                          <span className="rule-status">
                            {rule.enabled ? "✓ Enabled" : "✗ Disabled"}
                          </span>
                          <span className="subtle">
                            {rule.conditions?.length || 0} conditions, {rule.actions?.length || 0} actions
                          </span>
                        </div>
                        <div className="rule-actions">
                          <button
                            className="btn btn-small"
                            onClick={() => setViewingRule(rule)}
                          >
                            View
                          </button>
                          <button
                            className="btn btn-small"
                            onClick={() => startEditRule(profile.id, rule)}
                          >
                            Edit
                          </button>
                          <button
                            className="btn btn-small btn-danger"
                            onClick={() =>
                              handleDeleteRule(profile.id, rule.id)
                            }
                          >
                            Delete
                          </button>
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="subtle">No rules configured yet</p>
                )}
              </>
            )}
          </div>
        </div>
      ))}

      {/* View Rule Modal */}
      {viewingRule && (
        <div className="modal-overlay" onClick={() => setViewingRule(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Rule Details: {viewingRule.name}</h2>
              <button
                className="btn btn-small"
                onClick={() => setViewingRule(null)}
              >
                ✕
              </button>
            </div>
            <div className="rule-details">
              <p className="rule-status">
                {viewingRule.enabled ? "✓ Enabled" : "✗ Disabled"}
              </p>

              <h3>Conditions ({viewingRule.conditions?.length || 0})</h3>
              {viewingRule.conditions && viewingRule.conditions.length > 0 ? (
                <ul className="detail-list">
                  {viewingRule.conditions.map((cond, idx) => (
                    <li key={idx}>
                      <strong>{cond.field}</strong> {cond.operator} "{cond.value}"
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="subtle">No conditions</p>
              )}

              <h3>Actions ({viewingRule.actions?.length || 0})</h3>
              {viewingRule.actions && viewingRule.actions.length > 0 ? (
                <ul className="detail-list">
                  {viewingRule.actions.map((action, idx) => (
                    <li key={idx}>
                      <strong>{action.name}</strong>:{" "}
                      {JSON.stringify(action.arguments)}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="subtle">No actions</p>
              )}
            </div>
            <div className="actions">
              <button
                className="btn btn-danger"
                onClick={() => {
                  const profile = profiles.find(p =>
                    p.rules && p.rules.some(r => r.id === viewingRule.id)
                  );
                  if (profile) {
                    handleDeleteRule(profile.id, viewingRule.id);
                  }
                }}
              >
                Delete Rule
              </button>
              <button
                className="btn"
                onClick={() => setViewingRule(null)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
