import { useState, useRef, useEffect } from 'react'

export default function AudioRecorder({ onTranscriptReady }) {
  const [status, setStatus] = useState('idle')      // idle | recording | done
  const [transcript, setTranscript] = useState('')
  const [seconds, setSeconds] = useState(0)
  const [error, setError] = useState('')
  const recognitionRef = useRef(null)
  const timerRef = useRef(null)
  const transcriptRef = useRef('')

  const isSupported = 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window

  useEffect(() => {
    return () => {
      stopTimer()
      if (recognitionRef.current) recognitionRef.current.stop()
    }
  }, [])

  const stopTimer = () => {
    if (timerRef.current) clearInterval(timerRef.current)
  }

  const startRecording = () => {
    setError('')
    setTranscript('')
    transcriptRef.current = ''

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SR()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = 'en-IN'        // Indian English accent support

    recognition.onresult = (e) => {
      let final = ''
      let interim = ''
      for (let i = 0; i < e.results.length; i++) {
        const text = e.results[i][0].transcript
        if (e.results[i].isFinal) final += text + ' '
        else interim += text
      }
      const full = final + interim
      transcriptRef.current = full
      setTranscript(full)
    }

    recognition.onerror = (e) => {
      setError(`Microphone error: ${e.error}. Please allow mic access and use Chrome.`)
      stopRecording()
    }

    recognition.onend = () => {
      if (status === 'recording') stopRecording()
    }

    recognitionRef.current = recognition
    recognition.start()
    setStatus('recording')
    setSeconds(0)
    timerRef.current = setInterval(() => setSeconds(s => s + 1), 1000)
  }

  const stopRecording = () => {
    stopTimer()
    if (recognitionRef.current) {
      recognitionRef.current.stop()
    }
    setStatus('done')
  }

  const handleSubmit = () => {
    const final = transcriptRef.current.trim()
    if (final.length < 10) {
      setError('Answer is too short. Please record a longer response.')
      return
    }
    onTranscriptReady(final)
  }

  const handleReset = () => {
    setStatus('idle')
    setTranscript('')
    transcriptRef.current = ''
    setSeconds(0)
    setError('')
  }

  const formatTime = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`

  if (!isSupported) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 text-center">
        <p className="text-yellow-800 font-medium">⚠️ Speech recognition is not supported in this browser.</p>
        <p className="text-yellow-700 text-sm mt-1">Please use <strong>Google Chrome</strong> for the best experience.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Mic button */}
      <div className="flex flex-col items-center gap-3">
        <button
          onClick={status === 'recording' ? stopRecording : startRecording}
          disabled={status === 'done'}
          className={`w-24 h-24 rounded-full flex items-center justify-center text-4xl transition-all duration-300 shadow-lg
            ${status === 'recording'
              ? 'bg-red-500 hover:bg-red-600 animate-pulse scale-110'
              : status === 'done'
              ? 'bg-green-500 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 hover:scale-105'
            }`}
        >
          {status === 'recording' ? '⏹' : status === 'done' ? '✅' : '🎤'}
        </button>

        {status === 'idle' && <p className="text-gray-500 text-sm">Click the mic to start recording your answer</p>}
        {status === 'recording' && (
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
            <span className="text-red-600 font-mono font-semibold">{formatTime(seconds)}</span>
            <span className="text-gray-500 text-sm">Recording... Click to stop</span>
          </div>
        )}
        {status === 'done' && <p className="text-green-600 font-medium text-sm">✅ Recording complete</p>}
      </div>

      {/* Live transcript */}
      {transcript && (
        <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Your Answer (Transcript)</p>
          <p className="text-gray-800 text-sm leading-relaxed">{transcript}</p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-3">
          <p className="text-red-700 text-sm">{error}</p>
        </div>
      )}

      {/* Action buttons */}
      {status === 'done' && (
        <div className="flex gap-3">
          <button onClick={handleReset} className="btn-secondary flex-1">
            🔄 Re-record
          </button>
          <button onClick={handleSubmit} className="btn-primary flex-1">
            🚀 Submit for Evaluation
          </button>
        </div>
      )}
    </div>
  )
}
