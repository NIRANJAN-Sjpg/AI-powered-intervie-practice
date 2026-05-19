import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navLink = (to, label) => (
    <Link
      to={to}
      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
        location.pathname === to
          ? 'bg-blue-600 text-white'
          : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
      }`}
    >
      {label}
    </Link>
  )

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center gap-2">
          <span className="text-2xl">🎤</span>
          <span className="font-bold text-gray-900 text-lg">InterviewAI</span>
        </Link>

        <div className="flex items-center gap-2">
          {navLink('/dashboard', 'Dashboard')}
          {navLink('/practice', 'Practice')}
          {navLink('/history', 'History')}
        </div>

        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-500 hidden sm:block">
            Hi, <strong>{user?.first_name || user?.username}</strong>
          </span>
          <button onClick={handleLogout} className="btn-secondary text-sm py-1.5 px-4">
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}
