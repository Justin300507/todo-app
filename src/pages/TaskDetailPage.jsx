import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import API from '../api.js';
import TaskForm from '../components/TaskForm.jsx';
import NotificationToast from '../components/NotificationToast.jsx';

const TaskDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        const res = await API.get(`/tasks/${id}`);
        setTask(res.data);
      } catch (err) {
        setToast({ msg: 'Failed to load task', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchTask();
  }, [id]);

  const handleDelete = async () => {
    if (!window.confirm('Delete this task?')) return;
    try {
      await API.delete(`/tasks/${id}`);
      setToast({ msg: 'Task deleted', type: 'success' });
      setTimeout(() => navigate('/dashboard'), 1500);
    } catch (err) {
      setToast({ msg: 'Delete failed', type: 'error' });
    }
  };

  return (
    <div>
      <header className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Task Detail</h2>
        <button onClick={handleDelete} className="btn-primary bg-red-600 hover:bg-red-700">
          Delete
        </button>
      </header>
      {loading ? (
        <div className="animate-pulse space-y-3">
          <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded-xl" />
          <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded-xl" />
          <div className="h-64 bg-slate-200 dark:bg-slate-700 rounded-xl" />
        </div>
      ) : task ? (
        <TaskForm task={task} />
      ) : (
        <p className="text-slate-500 dark:text-slate-400">Task not found.</p>
      )}
      <NotificationToast toast={toast} setToast={setToast} />
    </div>
  );
};

export default TaskDetailPage;