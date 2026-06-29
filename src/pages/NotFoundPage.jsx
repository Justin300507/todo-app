import React from 'react';
import { Link } from 'react-router-dom';
import { AlertCircle } from 'lucide-react';

const NotFoundPage = () => (
  <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
    <div className="text-center">
      <AlertCircle size={64} className="mx-auto text-slate-400 mb-4" />
      <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Page Not Found</h1>
      <p className="text-slate-500 dark:text-slate-400 mt-2">The page you are looking for does not exist.</p>
      <Link to="/" className="mt-4 inline-block text-indigo-600 hover:underline">Go Home</Link>
    </div>
  </div>
);

export default NotFoundPage;