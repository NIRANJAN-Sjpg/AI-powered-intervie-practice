import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'
import ScoreCard from '../components/ScoreCard'

const ROLE_COLORS = {
  software: 'bg-blue-100 text-blue-700',
  hr:       'bg-purple-100 text-purple-700',
  bpo:      'bg-green-100 text-green-700',
  data:     'bg-orange-100 text-orange-700',
}

export default function History() {
  const [attempts, setAttempts] = useState([])
  const [loading, setLoading]   = useState(true)
  const [selected, setSelected] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    api.get('/attempts/')
      .then(res => setAttempts(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600" />
    </div>
  )

  if (selected) {
    return (
      <main className="max-w-3xl mx-auto px-4 py-8">
        <button
          onClick={() => setSelected(null)}
          className="flex items-center gap-1 text-blue-600 hover:underline mb-6 text-sm font-medium"
        >
          ← Back to History
        </button>
        <div className="card mb-6 border-l-4 border-blue-500">
          <p className="text-xs text-gray-400 mb-1">Question</p>
          <p className="font-semibold text-gray-900">{selected.question?.text}</p>
        </div>
        <ScoreCard
          feedback={selected.feedback}
          question={selected.question}
          transcript={selected.transcript}
        />
      </main>
    )
  }

  return (
    <main className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-black text-gray-900">📋 Attempt History</h1>
          <p className="text-gray-500 mt-1">{attempts.length} total attempts</p>
        </div>
        <button onClick={() => navigate('/practice')} className="btn-primary">
          + New Attempt
        </button>
      </div>

      {attempts.length === 0 ? (
        <div className="card text-center py-16">
          <p className="text-5xl mb-4">🎤</p>
          <p className="text-xl font-semibold text-gray-700">No attempts yet</p>
          <p className="text-gray-400 mt-2 mb-6">Start practicing to see your history here</p>
          <button onClick={() => navigate('/practice')} className="btn-primary">
            Start Practicing
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          {attempts.map(a => (
            <div
              key={a.id}
              onClick={() => setSelected(a)}
              className="card cursor-pointer hover:shadow-md transition-shadow hover:border-blue-200 border"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-gray-900 truncate">{a.question?.text}</p>
                  <div className="flex items-center gap-2 mt-1.5">
                    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full capitalize ${ROLE_COLORS[a.question?.role] || 'bg-gray-100 text-gray-600'}`}>
                      {a.question?.role}
                    </span>
                    <span className="text-xs text-gray-400">
                      {new Date(a.created_at).toLocaleDateString('en-IN', {
                        day: 'numeric', month: 'short', year: 'numeric'
                      })}
                    </span>
                  </div>
                </div>

                {a.feedback && (
                  <div className="text-right flex-shrink-0">
                    <p className={`text-2xl font-black ${
                      a.feedback.overall_score >= 7 ? 'text-green-600' :
                      a.feedback.overall_score >= 5 ? 'text-yellow-600' : 'text-red-500'
                    }`}>
                      {a.feedback.overall_score}/10
                    </p>
                    <div className="flex gap-2 text-xs text-gray-400 mt-0.5 justify-end">
                      <span>C:{a.feedback.clarity_score}</span>
                      <span>K:{a.feedback.content_score}</span>
                      <span>F:{a.feedback.confidence_score}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  )
}
