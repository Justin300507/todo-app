import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import ListViewPage from './pages/ListViewPage.jsx';
import TaskDetailPage from './pages/TaskDetailPage.jsx';
import SettingsPage from './pages/SettingsPage.jsx';
import NotFoundPage from './pages/NotFoundPage.jsx';
import Sidebar from './components/Sidebar.jsx';
import Header from './components/Header.jsx';

const PrivateRoute = ({ children }) => {
  return localStorage.getItem('token') ? children : <Navigate to="/login" replace />;
};

const Layout = () => (
  <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
    <Sidebar />
    <div className="ml-56 flex-1 flex flex-col">
      <Header />
      <main className="flex-1 p-6 overflow-auto">
        <Outlet />
      </main>
    </div>
  </div>
);

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route element={<PrivateRoute><Layout /></PrivateRoute>}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/lists" element={<ListViewPage />} />
          <Route path="/tasks/:id" element={<TaskDetailPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};

export default App;