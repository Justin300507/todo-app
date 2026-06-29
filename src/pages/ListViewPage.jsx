import React, { useState, useEffect } from 'react';
import { Plus, Search } from 'lucide-react';
import ListItemCard from '../components/ListItemCard.jsx';
import SearchBar from '../components/SearchBar.jsx';
import NotificationToast from '../components/NotificationToast.jsx';

const ListViewPage = () => {
  const [lists, setLists] = useState([
    { id:1, name:'Product Roadmap', owner:'Team Alpha', updated:'Jun 20' },
    { id:2, name:'Marketing Campaigns', owner:'Team Beta', updated:'Jun 18' },
    { id:3, name:'Personal To‑Do', owner:'You', updated:'Jun 22' },
    { id:4, name:'Bug Triage', owner:'Team Gamma', updated:'Jun 19' },
    { id:5, name:'Design Sprint', owner:'Team Delta', updated:'Jun 21' },
  ]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1000);
    return () => clearTimeout(timer);
  }, []);

  const filtered = lists.filter(l => l.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div>
      <header className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Lists</h2>
        <button className="btn-primary flex items-center gap-1.5">
          <Plus size={16} /> Add List
        </button>
      </header>
      <SearchBar value={search} onChange={e => setSearch(e.target.value)} placeholder="Search lists..." />
      {loading ? (
        <div className="animate-pulse space-y-3 mt-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-16 bg-slate-200 dark:bg-slate-700 rounded-xl" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-10 text-slate-500 dark:text-slate-400">
          <Search size={48} className="mx-auto mb-4 text-slate-400" />
          <p>No results found</p>
        </div>
      ) : (
        <div className="mt-4 space-y-3">
          {filtered.map(list => (
            <ListItemCard key={list.id} title={list.name} subtitle={`${list.owner} · ${list.updated}`} />
          ))}
        </div>
      )}
      <NotificationToast toast={toast} setToast={setToast} />
    </div>
  );
};

export default ListViewPage;