import React, { useEffect, useRef, useState } from "react";
import PropTypes from "prop-types";
import { Calendar, Clock, Flag, Plus } from "react-feather";

function toIsoDateTime(value) {
  if (!value) return null;
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return null;
  return parsed.toISOString();
}

export default function TaskComposer({ onCreate, isSubmitting }) {
  const titleInputRef = useRef(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [duration, setDuration] = useState("");
  const [priority, setPriority] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [notBeforeDate, setNotBeforeDate] = useState("");

  useEffect(() => {
    if (!isExpanded) return;
    titleInputRef.current?.focus();
  }, [isExpanded]);

  function resetForm() {
    setTitle("");
    setDescription("");
    setDuration("");
    setPriority("");
    setDueDate("");
  }

  function handleExpand() {
    setIsExpanded(true);
  }

  function handleCancel() {
    resetForm();
    setIsExpanded(false);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) return;

    const parsedDuration = duration ? Number(duration) : null;
    const parsedPriority = priority ? Number(priority) : null;

    const payload = {
      title: trimmedTitle,
      description: description.trim() || null,
      duration:
        parsedDuration && Number.isFinite(parsedDuration)
          ? parsedDuration
          : null,
      priority:
        parsedPriority && Number.isFinite(parsedPriority)
          ? parsedPriority
          : null,
      due_date: toIsoDateTime(dueDate),
      not_before: toIsoDateTime(notBeforeDate),
    };

    await onCreate(payload);
    resetForm();
  }

  return (
    <form className="tasks-create-form" onSubmit={handleSubmit}>
      {!isExpanded ? (
        <button
          type="button"
          className="btn task-compose-expand-btn"
          onClick={handleExpand}
          disabled={isSubmitting}
        >
          <Plus className="btn-icon" aria-hidden="true" />
          Add task
        </button>
      ) : null}

      {isExpanded ? (
        <div className="task-composer-shell">
          <input
            ref={titleInputRef}
            type="text"
            className="task-title-input"
            placeholder="Task name"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            disabled={isSubmitting}
            aria-label="Task title"
          />
          <input
            type="text"
            className="task-description-input"
            placeholder="Description"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            disabled={isSubmitting}
            aria-label="Task description"
          />

          <div className="task-options-row">
            <label className="task-chip-field">
              <Clock className="task-chip-icon" aria-hidden="true" />
              <input
                type="number"
                min="1"
                step="1"
                value={duration}
                onChange={(event) => setDuration(event.target.value)}
                disabled={isSubmitting}
                placeholder="Duration (min)"
                aria-label="Task duration"
              />
            </label>

            <label className="task-chip-field task-chip-select">
              <Flag className="task-chip-icon" aria-hidden="true" />
              <select
                value={priority}
                onChange={(event) => setPriority(event.target.value)}
                disabled={isSubmitting}
                aria-label="Task priority"
              >
                <option value="">Priority</option>
                <option value="1">P1</option>
                <option value="2">P2</option>
                <option value="3">P3</option>
                <option value="4">P4</option>
              </select>
            </label>

            <label className="task-chip-field task-chip-date">
              <Calendar className="task-chip-icon" aria-hidden="true" />
              Due
              <input
                type="datetime-local"
                value={dueDate}
                onChange={(event) => setDueDate(event.target.value)}
                disabled={isSubmitting}
                aria-label="Task due date"
              />
            </label>
            <label className="task-chip-field task-chip-date">
              <Calendar className="task-chip-icon" aria-hidden="true" />
              Not Before
              <input
                type="datetime-local"
                value={notBeforeDate}
                onChange={(event) => setNotBeforeDate(event.target.value)}
                disabled={isSubmitting}
                aria-label="Not before date"
              />
            </label>
          </div>

          <div className="task-footer-row">
            <div className="task-create-actions">
              <button
                type="button"
                className="btn task-create-cancel-btn"
                onClick={handleCancel}
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn btn-primary task-add-btn"
                disabled={isSubmitting || !title.trim()}
              >
                {isSubmitting ? "Adding task..." : "Add task"}
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </form>
  );
}

TaskComposer.propTypes = {
  onCreate: PropTypes.func.isRequired,
  isSubmitting: PropTypes.bool.isRequired,
};
