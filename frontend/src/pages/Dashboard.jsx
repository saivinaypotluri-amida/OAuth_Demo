import React, { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { MessageSquare, FileText, Settings, TrendingUp, AlertCircle, CheckCircle, XCircle } from 'lucide-react'

const Dashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState({
    messages: 0,
    summaries: 0,
    tokens: 0,
  })
  const [credentials, setCredentials] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [messagesRes, summariesRes, credentialsRes] = await Promise.all([
        api.get('/agent/messages?limit=1'),
        api.get('/agent/summaries?limit=1'),
        api.get('/credentials'),
      ])

      // Get counts from headers or calculate
      setStats({
        messages: messagesRes.data.length,
        summaries: summariesRes.data.length,
        tokens: 0, // Calculate from usage if needed
      })

      setCredentials(credentialsRes.data)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getCredentialStatus = (service) => {
    const cred = credentials.find(c => c.service_type === service)
    if (!cred) return { status: 'not_configured', color: 'gray', icon: AlertCircle }
    if (cred.test_status === 'success') return { status: 'connected', color: 'green', icon: CheckCircle }
    if (cred.test_status === 'failed') return { status: 'failed', color: 'red', icon: XCircle }
    return { status: 'pending', color: 'yellow', icon: AlertCircle }
  }

  const services = [
    { name: 'Slack', type: 'slack' },
    { name: 'Azure OpenAI', type: 'azure_openai' },
    { name: 'Google Workspace', type: 'google_workspace' },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-xl shadow-lg p-6 text-white">
        <h1 className="text-3xl font-bold">Welcome back, {user?.full_name || user?.username}!</h1>
        <p className="mt-2 text-primary-100">
          Manage your AI agent, track conversations, and generate summaries seamlessly.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Messages</p>
              <p className="mt-2 text-3xl font-semibold text-gray-900">{stats.messages}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <MessageSquare className="h-8 w-8 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Summaries Created</p>
              <p className="mt-2 text-3xl font-semibold text-gray-900">{stats.summaries}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <FileText className="h-8 w-8 text-green-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Tokens</p>
              <p className="mt-2 text-3xl font-semibold text-gray-900">{stats.tokens.toLocaleString()}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Integration Status */}
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Integration Status</h2>
        <div className="space-y-4">
          {services.map((service) => {
            const status = getCredentialStatus(service.type)
            const StatusIcon = status.icon
            return (
              <div key={service.type} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <div className={`p-2 bg-${status.color}-100 rounded-lg mr-3`}>
                    <StatusIcon className={`h-5 w-5 text-${status.color}-600`} />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{service.name}</p>
                    <p className="text-sm text-gray-500 capitalize">{status.status.replace('_', ' ')}</p>
                  </div>
                </div>
                <a
                  href="/settings"
                  className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                >
                  Configure
                </a>
              </div>
            )
          })}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <a
            href="/messages"
            className="flex items-center p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
          >
            <MessageSquare className="h-6 w-6 text-primary-600 mr-3" />
            <div>
              <p className="font-medium text-gray-900">View Messages</p>
              <p className="text-sm text-gray-600">See your conversation history</p>
            </div>
          </a>
          <a
            href="/summaries"
            className="flex items-center p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
          >
            <FileText className="h-6 w-6 text-green-600 mr-3" />
            <div>
              <p className="font-medium text-gray-900">View Summaries</p>
              <p className="text-sm text-gray-600">Access generated summaries</p>
            </div>
          </a>
          <a
            href="/settings"
            className="flex items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors"
          >
            <Settings className="h-6 w-6 text-purple-600 mr-3" />
            <div>
              <p className="font-medium text-gray-900">Settings</p>
              <p className="text-sm text-gray-600">Configure integrations</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
