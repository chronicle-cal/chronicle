import React, { useState } from "react";
import PropTypes from "prop-types";
import {
  CalendarDaysIcon,
  CheckIcon,
  ClockIcon,
  FlagIcon,
  PencilSquareIcon,
  TrashIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";

function toDateTimeLocal(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}

function toIsoDateTime(value) {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  return date.toISOString();
}

export default function TaskList({
  tasks,
  onToggleComplete,
  onDelete,
  onUpdateDetails,
  updatingTaskId,
  deletingTaskId,
}) {
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [form, setForm] = useState({
    description: "",
    duration: "",
    priority: "",
    dueDate: "",
  });

  function openEditor(task) {
    setEditingTaskId(task.id);
    setForm({
      description: task.description || "",
      duration: task.duration ?? "",
      priority: task.priority ?? "",
      dueDate: toDateTimeLocal(task.due_date),
    });
  }

  function closeEditor() {
    setEditingTaskId(null);
    setForm({ description: "", duration: "", priority: "", dueDate: "" });
  }

  async function handleSave(taskId) {
    const parsedDuration = form.duration ? Number(form.duration) : null;
    const parsedPriority = form.priority ? Number(form.priority) : null;

    await onUpdateDetails(taskId, {
      description: form.description.trim() || null,
      duration:
        parsedDuration && Number.isFinite(parsedDuration)
          ? parsedDuration
          : null,
      priority:
        parsedPriority && Number.isFinite(parsedPriority)
          ? parsedPriority
          : null,
      due_date: toIsoDateTime(form.dueDate),
    });

    closeEditor();
  }

  if (tasks.length === 0) {
    return (
      <div className="task-empty-state">
        <p className="subtle">No tasks yet for this profile.</p>
      </div>
    );
  }

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <li key={task.id} className="task-item">
          <div className="task-main">
            <button
              type="button"
              className={`task-check ${task.completed ? "is-complete" : ""}`}
              onClick={() => onToggleComplete(task)}
              disabled={updatingTaskId === task.id}
              aria-label={
                task.completed ? "Mark task incomplete" : "Mark task complete"
              }
              aria-pressed={task.completed}
            >
              {task.completed ? "✓" : ""}
            </button>

            <div className="task-content">
              <p
                className={`task-title ${task.completed ? "is-complete" : ""}`}
              >
                {task.title}
              </p>

              <div className="task-meta">
                <span className="pill task-pill">
                  <FlagIcon className="pill-icon" aria-hidden="true" />
                  {task.priority ?? "-"}
                </span>
                <span className="pill task-pill">
                  <ClockIcon className="pill-icon" aria-hidden="true" />
                  {task.duration ?? "-"} min
                </span>
                <span className="pill task-pill">
                  <CalendarDaysIcon className="pill-icon" aria-hidden="true" />
                  {task.due_date
                    ? new Date(task.due_date).toLocaleString()
                    : "-"}
                </span>
              </div>

              {task.description ? (
                <p className="subtle task-description">{task.description}</p>
              ) : null}

              {editingTaskId === task.id ? (
                <div className="task-edit-grid">
                  <input
                    type="text"
                    value={form.description}
                    onChange={(event) =>
                      setForm((current) => ({
                        ...current,
                        description: event.target.value,
                      }))
                    }
                    placeholder="Description"
                  />
                  <input
                    type="number"
                    min="1"
                    step="1"
                    value={form.duration}
                    onChange={(event) =>
                      setForm((current) => ({
                        ...current,
                        duration: event.target.value,
                      }))
                    }
                    placeholder="Duration (minutes)"
                  />
                  <input
                    type="number"
                    min="1"
                    step="1"
                    value={form.priority}
                    onChange={(event) =>
                      setForm((current) => ({
                        ...current,
                        priority: event.target.value,
                      }))
                    }
                    placeholder="Priority"
                  />
                  <input
                    type="datetime-local"
                    value={form.dueDate}
                    onChange={(event) =>
                      setForm((current) => ({
                        ...current,
                        dueDate: event.target.value,
                      }))
                    }
                  />
                </div>
              ) : null}
            </div>
          </div>

          <div className="task-actions">
            {editingTaskId === task.id ? (
              <>
                <button
                  type="button"
                  className="btn btn-small btn-primary"
                  onClick={() => handleSave(task.id)}
                  disabled={updatingTaskId === task.id}
                >
                  <CheckIcon className="btn-icon" aria-hidden="true" />
                  {updatingTaskId === task.id ? "Saving..." : "Save"}
                </button>
                <button
                  type="button"
                  className="btn btn-small"
                  onClick={closeEditor}
                >
                  <XMarkIcon className="btn-icon" aria-hidden="true" />
                  Cancel
                </button>
              </>
            ) : (
              <button
                type="button"
                className="btn btn-small"
                onClick={() => openEditor(task)}
              >
                <PencilSquareIcon className="btn-icon" aria-hidden="true" />
                Edit
              </button>
            )}

            <button
              type="button"
              className="btn btn-small btn-danger"
              onClick={() => onDelete(task.id)}
              disabled={deletingTaskId === task.id}
            >
              <TrashIcon className="btn-icon" aria-hidden="true" />
              {deletingTaskId === task.id ? "Deleting..." : "Delete"}
            </button>
          </div>
        </li>
      ))}
    </ul>
  );
}

TaskList.propTypes = {
  tasks: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      completed: PropTypes.bool.isRequired,
      title: PropTypes.string.isRequired,
      description: PropTypes.string,
      duration: PropTypes.number,
      priority: PropTypes.number,
      due_date: PropTypes.string,
    })
  ).isRequired,
  onToggleComplete: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onUpdateDetails: PropTypes.func.isRequired,
  updatingTaskId: PropTypes.string,
  deletingTaskId: PropTypes.string,
};
