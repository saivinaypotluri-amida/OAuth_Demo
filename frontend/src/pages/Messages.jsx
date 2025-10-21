import React, { useState, useEffect } from 'react'
import api from '../services/api'
import { MessageSquare, Send, Loader2, FileText, ExternalLink } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

const Messages = () => {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [newMessage, setNewMessage] = useState('')
  const [error, setError] = useState(null)
  const [showSummaryModal, setShowSummaryModal] = useState(false)
  const [summaryContent, setSummaryContent] = useState('')
  const [summaryTitle, setSummaryTitle] = useState('')
  const [generatingSummary, setGeneratingSummary] = useState(false)
  const [summaryResult, setSummaryResult] = useState(null)

  useEffect(() => {
    fetchMessages()
  }, [])

  const fetchMessages = async () => {
    try {
      const response = await api.get('/agent/messages?limit=50')
      setMessages(response.data)
    } catch (error) {
      console.error('Failed to fetch messages:', error)
      setError('Failed to load messages')
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!newMessage.trim()) return

    setSending(true)
    setError(null)

    try {
      await api.post('/agent/message', {
        message: newMessage,
        channel_id: 'web_portal'
      })
      setNewMessage('')
      await fetchMessages()
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to send message')
    } finally {
      setSending(false)
    }
  }

  const handleGenerateSummary = async (e) => {
    e.preventDefault()
    if (!summaryContent.trim()) return

    setGeneratingSummary(true)
    setError(null)

    try {
      const response = await api.post('/agent/summary', {
        title: summaryTitle || 'Untitled Summary',
        content: summaryContent
      }, {
        params: { save_to_drive: true }
      })
      
      setSummaryResult(response.data)
      setSummaryContent('')
      setSummaryTitle('')
      
      // Show success message
      setTimeout(() => {
        setShowSummaryModal(false)
        setSummaryResult(null)
      }, 5000)
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to generate summary')
    } finally {
      setGeneratingSummary(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow">
        {/* Header */}
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center">
                <MessageSquare className="h-6 w-6 text-primary-600 mr-2" />
                <h1 className="text-2xl font-bold text-gray-900">Messages</h1>
              </div>
              <p className="mt-1 text-sm text-gray-600">
                Chat with your AI agent and view conversation history
              </p>
            </div>
            <button
              onClick={() => setShowSummaryModal(true)}
              className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
            >
              <FileText className="h-5 w-5 mr-2" />
              Generate Summary
            </button>
          </div>
        </div>

        {/* New Message Form */}
        <div className="p-6 border-b bg-gray-50">
          <form onSubmit={handleSendMessage}>
            <div className="flex gap-3">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                disabled={sending}
              />
              <button
                type="submit"
                disabled={sending || !newMessage.trim()}
                className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {sending ? (
                  <Loader2 className="animate-spin h-5 w-5" />
                ) : (
                  <>
                    <Send className="h-5 w-5 mr-2" />
                    Send
                  </>
                )}
              </button>
            </div>
          </form>
          {error && (
            <p className="mt-2 text-sm text-red-600">{error}</p>
          )}
        </div>

        {/* Messages List */}
        <div className="p-6 space-y-4 max-h-[600px] overflow-y-auto">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-500">No messages yet. Start a conversation!</p>
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className="space-y-3">
                {/* User Message */}
                <div className="flex justify-end">
                  <div className="max-w-[70%] bg-primary-100 rounded-lg p-4">
                    <p className="text-sm text-gray-900">{message.user_message}</p>
                    <p className="mt-1 text-xs text-gray-500">
                      {formatDistanceToNow(new Date(message.created_at), { addSuffix: true })}
                    </p>
                  </div>
                </div>

                {/* Bot Response */}
                <div className="flex justify-start">
                  <div className="max-w-[70%] bg-gray-100 rounded-lg p-4">
                    <p className="text-sm text-gray-900 whitespace-pre-wrap">{message.bot_response}</p>
                    <div className="mt-2 flex items-center gap-3 text-xs text-gray-500">
                      <span>Tokens: {message.tokens_used}</span>
                      {message.response_time_ms && (
                        <span>Response time: {Math.round(message.response_time_ms)}ms</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Summary Modal */}
      {showSummaryModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <FileText className="h-6 w-6 text-green-600 mr-2" />
                  <h2 className="text-xl font-bold text-gray-900">Generate Summary</h2>
                </div>
                <button
                  onClick={() => {
                    setShowSummaryModal(false)
                    setSummaryResult(null)
                    setError(null)
                  }}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              <p className="mt-2 text-sm text-gray-600">
                AI will generate a summary and save it to Google Drive
              </p>
            </div>

            {summaryResult ? (
              <div className="p-6 space-y-4">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="font-semibold text-green-900 mb-2">✅ Summary Generated!</h3>
                  <div className="bg-white rounded p-3 mb-3">
                    <p className="text-sm text-gray-900 whitespace-pre-wrap">{summaryResult.summary}</p>
                  </div>
                  {summaryResult.google_drive_file_url && (
                    <a
                      href={summaryResult.google_drive_file_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-sm text-green-700 hover:text-green-800"
                    >
                      <ExternalLink className="h-4 w-4 mr-1" />
                      Open in Google Drive
                    </a>
                  )}
                  <div className="mt-2 text-xs text-gray-500">
                    Tokens used: {summaryResult.tokens_used}
                  </div>
                </div>
              </div>
            ) : (
              <form onSubmit={handleGenerateSummary} className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Title (Optional)
                  </label>
                  <input
                    type="text"
                    value={summaryTitle}
                    onChange={(e) => setSummaryTitle(e.target.value)}
                    placeholder="My Summary"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Content to Summarize *
                  </label>
                  <textarea
                    value={summaryContent}
                    onChange={(e) => setSummaryContent(e.target.value)}
                    placeholder="Paste your long text here..."
                    rows={10}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    required
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Minimum 50 characters required
                  </p>
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                )}

                <div className="flex gap-3">
                  <button
                    type="submit"
                    disabled={generatingSummary || summaryContent.length < 50}
                    className="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                  >
                    {generatingSummary ? (
                      <>
                        <Loader2 className="animate-spin h-5 w-5 mr-2" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <FileText className="h-5 w-5 mr-2" />
                        Generate & Save to Drive
                      </>
                    )}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowSummaryModal(false)
                      setSummaryContent('')
                      setSummaryTitle('')
                      setError(null)
                    }}
                    className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default Messages
