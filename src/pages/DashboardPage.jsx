import React, { useState, useEffect } from 'react';
import API from '../api.js';
import StatCard from '../components/StatCard.jsx';
import { CheckSquare, Clock, AlertCircle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import NotificationToast from '../components/NotificationToast.jsx';

const DashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await API.get('/stats/summary');
        setStats(res.data);
      } catch (err) {
        setToast({ msg: 'Failed to load stats', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const chartData = [
    { month: 'Jan', total: 840 },
    { month: 'Feb', total: 720 },
    { month: 'Mar', total: 1100 },
    { month: 'Apr', total: 890 },
    { month: 'May', total: 1240 },
    { month: 'Jun', total: 980 },
  ];

  return (
    <div>
      <header className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Hello, {localStorage.getItem('display_name') || 'User'}</h2>
        <p className="text-slate-500 dark:text-slate-400">{new Date().toLocaleDateString()}</p>
      </header>
      {loading ? (
        <div className="animate-pulse space-y-4">
          <div className="h-24 bg-slate-200 dark:bg-slate-700 rounded-xl" />
          <div className="h-64 bg-slate-200 dark:bg-slate-700 rounded-xl" />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <StatCard label="Total Tasks" value={stats.total_tasks} icon={<CheckSquare size={18} className="text-indigo-600" />} change="+12% this week" />
            <StatCard label="Completed" value={stats.completed_tasks} icon={<CheckSquare size={18} className="text-indigo-600" />} change="+8% this week" />
            <StatCard label="Pending" value={stats.pending_tasks} icon={<Clock size={18} className="text-indigo-600" />} change="+5% this week" />
            <StatCard label="Overdue" value={stats.overdue_tasks} icon={<AlertCircle size={18} className="text-indigo-600" />} change="+2% this week" />
          </div>
          <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-5">
            <h3 className="font-semibold text-slate-900 dark:text-white mb-4">Monthly Overview</h3>
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.15} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#1e293b', border: 'none', borderRadius: '8px', color: '#f1f5f9' }} />
                <Area type="monotone" dataKey="total" stroke="#6366f1" strokeWidth={2} fill="url(#colorTotal)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <section className="mt-6">
            <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-3">Recent Tasks</h3>
            <div className="space-y-3">
              {stats.recent_tasks?.slice(0,5).map(task => (
                <div key={task.id} className="bg-white dark:bg-slate-800 rounded-xl p-4 border border-slate-100 dark:border-slate-700 flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-slate-900 dark:text-white">{task.title}</p>
                    <p className="text-xs text-slate-500 dark:text-slate-400">{task.status}</p>
                  </div>
                  <span className="text-sm font-medium text-indigo-600">{task.due_date?.split('T')[0]}</span>
                </div>
              ))}
            </div>
          </section>
        </>
      )}
      <NotificationToast toast={toast} setToast={setToast} />
    </div>
  );
};

export default DashboardPage;