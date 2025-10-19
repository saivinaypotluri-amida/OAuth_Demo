import React, { useState, useEffect } from 'react'
import api from '../services/api'
import { MessageSquare, Send, Loader2 } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

const Messages = () => {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [newMessage, setNewMessage] = useState('')
  const [error, setError] = useState(null)

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
          <div className="flex items-center">
            <MessageSquare className="h-6 w-6 text-primary-600 mr-2" />
            <h1 className="text-2xl font-bold text-gray-900">Messages</h1>
          </div>
          <p className="mt-1 text-sm text-gray-600">
            Chat with your AI agent and view conversation history
          </p>
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
    </div>
  )
}

export default Messages
