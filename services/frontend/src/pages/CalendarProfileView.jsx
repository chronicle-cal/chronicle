import React, { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useFlash } from "../context/FlashContext.jsx";
import TaskComposer from "../components/TaskComposer.jsx";
import TaskList from "../components/TaskList.jsx";
import { profileApi, taskApi } from "../lib/apiClient.js";

export default function CalendarProfileView() {
  const { profileId } = useParams();
  const { addFlash } = useFlash();

  const [profile, setProfile] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loadingProfile, setLoadingProfile] = useState(true);
  const [loadingTasks, setLoadingTasks] = useState(true);
  const [isCreatingTask, setIsCreatingTask] = useState(false);
  const [updatingTaskId, setUpdatingTaskId] = useState(null);
  const [deletingTaskId, setDeletingTaskId] = useState(null);

  const profileTasks = useMemo(() => {
    const filtered = tasks.filter((task) => task.profile?.id === profileId);
    return filtered.sort((first, second) => {
      if (first.completed !== second.completed) {
        return Number(first.completed) - Number(second.completed);
      }
      return first.title.localeCompare(second.title);
    });
  }, [tasks, profileId]);

  useEffect(() => {
    let isActive = true;

    const loadData = async () => {
      setLoadingProfile(true);
      setLoadingTasks(true);

      try {
        const [profileResponse, tasksResponse] = await Promise.all([
          profileApi.getProfile(profileId),
          taskApi.listTasks(),
        ]);

        if (!isActive) return;

        setProfile(profileResponse.data);
        setTasks(tasksResponse.data);
      } catch (error) {
        const message =
          error.response?.data?.detail ||
          error.message ||
          "Failed to load profile data.";
        addFlash("error", message);
      } finally {
        if (isActive) {
          setLoadingProfile(false);
          setLoadingTasks(false);
        }
      }
    };

    loadData();

    return () => {
      isActive = false;
    };
  }, [profileId, addFlash]);

  async function handleCreateTask(payload) {
    try {
      setIsCreatingTask(true);
      const response = await taskApi.createTask({
        ...payload,
        profile_id: profileId,
      });
      setTasks((current) => [response.data, ...current]);
      addFlash("success", "Task created");
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to create task.";
      addFlash("error", message);
    } finally {
      setIsCreatingTask(false);
    }
  }

  async function handleToggleComplete(task) {
    try {
      setUpdatingTaskId(task.id);
      const response = await taskApi.updateTask(task.id, {
        completed: !task.completed,
      });

      setTasks((current) =>
        current.map((item) => (item.id === task.id ? response.data : item))
      );
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to update task.";
      addFlash("error", message);
    } finally {
      setUpdatingTaskId(null);
    }
  }

  async function handleUpdateTaskDetails(taskId, payload) {
    try {
      setUpdatingTaskId(taskId);
      const response = await taskApi.updateTask(taskId, payload);

      setTasks((current) =>
        current.map((item) => (item.id === taskId ? response.data : item))
      );
      addFlash("success", "Task updated");
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to update task.";
      addFlash("error", message);
      throw error;
    } finally {
      setUpdatingTaskId(null);
    }
  }

  async function handleDeleteTask(taskId) {
    const confirmed = window.confirm("Delete this task?");
    if (!confirmed) return;

    try {
      setDeletingTaskId(taskId);
      await taskApi.deleteTask(taskId);
      setTasks((current) => current.filter((task) => task.id !== taskId));
      addFlash("success", "Task deleted");
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to delete task.";
      addFlash("error", message);
    } finally {
      setDeletingTaskId(null);
    }
  }

  async function handleTriggerSync(profileId) {
    try {
      await profileApi.triggerProfileSync(profileId);
      addFlash("success", "Profile sync triggered");
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Failed to trigger sync.";
      addFlash("error", message);
    }
  }

  return (
    <div className="container calendar-profile-view">
      <div className="page-header">
        <div>
          <h1>
            {loadingProfile
              ? "Loading..."
              : profile?.name || "Calendar Profile"}
          </h1>
          <p className="subtle">
            Profile ID: <strong>{profileId}</strong>
          </p>
        </div>

        <div className="btn-group">
          <Link to="/calendar-profiles" className="btn">
            Manage
          </Link>
          <button
            className="btn btn-small"
            onClick={() => handleTriggerSync(profileId)}
          >
            Synchroize Now
          </button>
        </div>
      </div>

      <section className="card tasks-card">
        <h2>Tasks</h2>
        <TaskComposer
          onCreate={handleCreateTask}
          isSubmitting={isCreatingTask}
        />

        {loadingTasks ? (
          <p className="subtle">Loading tasks...</p>
        ) : (
          <TaskList
            tasks={profileTasks}
            onToggleComplete={handleToggleComplete}
            onDelete={handleDeleteTask}
            onUpdateDetails={handleUpdateTaskDetails}
            updatingTaskId={updatingTaskId}
            deletingTaskId={deletingTaskId}
          />
        )}
      </section>

      <section className="card calendar-placeholder-card">
        <h2>Calendar</h2>
        <p className="subtle">Calendar component will appear here.</p>

        <div className="calendar-placeholder" aria-label="calendar placeholder">
          <span>Calendar Placeholder</span>
        </div>
      </section>
    </div>
  );
}
