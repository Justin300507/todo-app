import React from 'react';
import { CheckSquare } from 'lucide-react';

const ListItemCard = ({ title, subtitle }) => (
  <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-4 flex items-center justify-between hover:shadow-sm transition-shadow">
    <div className="flex items-center gap-3">
      <div className="w-9 h-9 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center">
        <CheckSquare className="text-indigo-600" size={18} />
      </div>
      <div>
        <p className="text-sm font-semibold text-slate-900 dark:text-white">{title}</p>
        <p className="text-xs text-slate-500 dark:text-slate-400">{subtitle}</p>
      </div>
    </div>
  </div>
);

export default ListItemCard;