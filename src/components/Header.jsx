import React, { useState } from 'react';
import { Sun, Moon, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
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
    <header className="flex items-center justify-between border-b border-slate-100 dark:border-slate-700 px-6 py-4">
      <h1 className="text-xl font-semibold text-slate-900 dark:text-white">Dashboard</h1>
      <div className="flex items-center gap-4">
        <button onClick={toggleDark} className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
          {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <button onClick={handleLogout} className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
          <LogOut size={18} />
        </button>
      </div>
    </header>
  );
};

export default Header;