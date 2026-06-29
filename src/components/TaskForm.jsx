import React, { useState } from 'react';
import { Plus, X } from 'lucide-react';
import API from '../api.js';
import NotificationToast from './NotificationToast.jsx';

const TaskForm = ({ task }) => {
  const isEdit = Boolean(task);
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [dueDate, setDueDate] = useState(task?.due_date?.split('T')[0] || '');
  const [status, setStatus] = useState(task?.status || '');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);

  const handleSubmit = async e => {
    e.preventDefault();
    if (!title) return;
    setLoading(true);
    try {
      const payload = { title, description, due_date: dueDate, status };
      if (isEdit) {
        await API.put(`/tasks/${task.id}`, payload);
        setToast({ msg: 'Task updated', type: 'success' });
      } else {
        await API.post('/tasks', payload);
        setToast({ msg: 'Task created', type: 'success' });
        setTitle('');
        setDescription('');
        setDueDate('');
        setStatus('');
      }
    } catch (err) {
      setToast({ msg: 'Error saving task', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {toast && <NotificationToast toast={toast} setToast={setToast} />}
      <div className="space-y-1">
        <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Title</label>
        <input type="text" value={title} onChange={e => setTitle(e.target.value)} placeholder="e.g. Launch Q3 campaign" className="input" />
      </div>
      <div className="space-y-1">
        <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Description</label>
        <textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="Optional details" className="input" rows={3} />
      </div>
      <div className="flex gap-4">
        <div className="flex-1 space-y-1">
          <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Due Date</label>
          <input type="date" value={dueDate} onChange={e => setDueDate(e.target.value)} className="input" />
        </div>
        <div className="flex-1 space-y-1">
          <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Status</label>
          <input type="text" value={status} onChange={e => setStatus(e.target.value)} placeholder="e.g. In Progress" className="input" />
        </div>
      </div>
      <div className="flex justify-end gap-2">
        {isEdit && (
          <button type="button" className="btn-primary bg-slate-400 hover:bg-slate-500 text-white">
            <X size={16} /> Cancel
          </button>
        )}
        <button type="submit" disabled={loading || !title} className="btn-primary flex items-center gap-1.5">
          <Plus size={16} /> {loading ? 'Saving...' : isEdit ? 'Update' : 'Create'}
        </button>
      </div>
    </form>
  );
};

export default TaskForm;