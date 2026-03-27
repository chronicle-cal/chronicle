import React, { useState } from "react";
import PropTypes from "prop-types";
import { Calendar, Clock, FileText, Flag, Plus } from "react-feather";

function toIsoDateTime(value) {
  if (!value) return null;
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return null;
  return parsed.toISOString();
}

export default function TaskComposer({ onCreate, isSubmitting }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [duration, setDuration] = useState("");
  const [priority, setPriority] = useState("");
  const [dueDate, setDueDate] = useState("");

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
    };

    await onCreate(payload);
    setTitle("");
    setDescription("");
    setDuration("");
    setPriority("");
    setDueDate("");
  }

  return (
    <form className="tasks-create-form" onSubmit={handleSubmit}>
      <div className="tasks-create-row">
        <div className="input-with-icon">
          <FileText className="field-icon" aria-hidden="true" />
          <input
            type="text"
            placeholder="Add a task"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            disabled={isSubmitting}
            aria-label="Task title"
          />
        </div>
        <button
          type="submit"
          className="btn btn-primary task-add-btn"
          disabled={isSubmitting || !title.trim()}
        >
          <Plus className="btn-icon" aria-hidden="true" />
          {isSubmitting ? "Adding..." : "Add"}
        </button>
      </div>

      <div className="tasks-fields-grid">
        <div className="input-with-icon">
          <FileText className="field-icon" aria-hidden="true" />
          <input
            type="text"
            placeholder="Description"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            disabled={isSubmitting}
            aria-label="Task description"
          />
        </div>
        <div className="input-with-icon">
          <Clock className="field-icon" aria-hidden="true" />
          <input
            type="number"
            min="1"
            step="1"
            placeholder="Duration (min)"
            value={duration}
            onChange={(event) => setDuration(event.target.value)}
            disabled={isSubmitting}
            aria-label="Task duration"
          />
        </div>
        <div className="input-with-icon">
          <Flag className="field-icon" aria-hidden="true" />
          <input
            type="number"
            min="1"
            step="1"
            placeholder="Priority"
            value={priority}
            onChange={(event) => setPriority(event.target.value)}
            disabled={isSubmitting}
            aria-label="Task priority"
          />
        </div>
        <div className="input-with-icon">
          <Calendar className="field-icon" aria-hidden="true" />
          <input
            type="datetime-local"
            value={dueDate}
            onChange={(event) => setDueDate(event.target.value)}
            disabled={isSubmitting}
            aria-label="Task due date"
          />
        </div>
      </div>
    </form>
  );
}

TaskComposer.propTypes = {
  onCreate: PropTypes.func.isRequired,
  isSubmitting: PropTypes.bool.isRequired,
};
