import React from 'react';
import { Search } from 'lucide-react';

const SearchBar = ({ value, onChange, placeholder }) => (
  <div className="flex items-center gap-2 bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-lg px-3 py-2 mt-4">
    <Search size={16} className="text-slate-500 dark:text-slate-400" />
    <input
      type="text"
      value={value}
      onChange={onChange}
      placeholder={placeholder || 'Search...'}
      className="flex-1 bg-transparent outline-none text-slate-900 dark:text-white placeholder-slate-400"
    />
  </div>
);

export default SearchBar;