import React from 'react';
import { useAuthStore } from '../store/authStore';
import { LogOut, Menu } from 'lucide-react';

export const Header: React.FC = () => {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const [menuOpen, setMenuOpen] = React.useState(false);

  return (
    <header className="bg-primary-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
              <span className="text-primary-600 font-bold">SC</span>
            </div>
            <h1 className="text-xl font-bold">SME Compliance</h1>
          </div>

          <nav className="hidden md:flex gap-6">
            <a href="/dashboard" className="hover:text-primary-100">Dashboard</a>
            <a href="/uploads" className="hover:text-primary-100">Uploads</a>
            <a href="/reports" className="hover:text-primary-100">Reports</a>
          </nav>

          <div className="flex items-center gap-4">
            {user && <span className="text-sm">{user.email}</span>}
            <button
              onClick={logout}
              className="flex items-center gap-2 bg-primary-700 hover:bg-primary-800 px-4 py-2 rounded-lg transition"
            >
              <LogOut size={18} />
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
