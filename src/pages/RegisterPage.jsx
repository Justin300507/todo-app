import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import API from '../api.js';

const parseError = err => {
  if (!err.response) return null;
  const detail = err.response?.data?.detail;
  if (!detail) return 'Something went wrong. Please try again.';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) return detail.map(d => d.msg).join(', ');
  return 'Something went wrong. Please try again.';
};

const RegisterPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);

  const handleSubmit = async e => {
    e.preventDefault();
    if (password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await API.post('/auth/signup', { email, password, display_name: displayName });
      const loginRes = await API.post('/auth/login', { email, password });
      localStorage.setItem('token', loginRes.data.access_token);
      if (loginRes.data.display_name) localStorage.setItem('display_name', loginRes.data.display_name);
      if (loginRes.data.user_id) localStorage.setItem('user_id', String(loginRes.data.user_id));
      if (loginRes.data.email) localStorage.setItem('user_email', loginRes.data.email);
      navigate('/dashboard');
    } catch (err) {
      const msg = parseError(err);
      setError(msg || 'Failed to register.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600 mx-auto mb-3 flex items-center justify-center">
            <span className="text-white font-bold text-xl">A</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Create account</h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">Start your journey</p>
        </div>
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 p-6 space-y-4">
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Full Name</label>
            <input type="text" value={displayName} onChange={e => setDisplayName(e.target.value)} placeholder="e.g. Alex Chen" className="input" />
          </div>
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" className="input" />
          </div>
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Enter password" className="input" />
            <p className="text-xs text-slate-400">Must be at least 8 characters</p>
          </div>
          <button type="submit" onClick={handleSubmit} disabled={loading || !email || !password || !displayName} className="btn-primary w-full justify-center">
            {loading ? 'Creating...' : 'Sign Up'}
          </button>
        </div>
        <p className="text-center text-sm text-slate-500 mt-4">
          Already have an account? <Link to="/login" className="text-indigo-600 font-medium hover:underline">Sign in</Link>
        </p>
      </div>
      {toast && (
        <div className={`fixed bottom-4 right-4 px-4 py-3 rounded-xl shadow-lg text-sm font-medium text-white z-50 ${toast.type === 'success' ? 'bg-emerald-600' : 'bg-red-600'}`}>
          {toast.msg}
        </div>
      )}
    </div>
  );
};

export default RegisterPage;