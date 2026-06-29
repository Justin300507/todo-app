import React, { useState } from 'react';
import { Sun, Moon, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const SettingsPage = () => {
  const [dark, setDark] = useState(document.documentElement.classList.contains('dark'));
  const navigate = useNavigate();

  const toggleDark = () => {
    setDark(d => {
      const next = !d;
      document.documentElement.classList.toggle('dark', next);
      return next;
    });
  };

  const handleLogout = () => {
    ['token','display_name','user_id','user_email'].forEach(k => localStorage.removeItem(k));
    navigate('/login');
  };

  return (
    <div>
      <header className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Settings</h2>
        <button onClick={toggleDark} className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
          {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </header>
      <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-100 dark:border-slate-700">
        <p className="text-slate-900 dark:text-white mb-4">Logged in as {localStorage.getItem('display_name') || 'User'}</p>
        <button onClick={handleLogout} className="btn-primary flex items-center gap-1.5 bg-red-600 hover:bg-red-700">
          <LogOut size={16} /> Log Out
        </button>
      </div>
    </div>
  );
};

export default SettingsPage;