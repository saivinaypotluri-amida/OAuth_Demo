import React, { useState, useEffect } from 'react'
import api from '../services/api'
import { CheckCircle, XCircle, Loader2, AlertCircle } from 'lucide-react'

const Settings = () => {
  const [credentials, setCredentials] = useState({})
  const [testing, setTesting] = useState({})
  const [saving, setSaving] = useState({})
  const [message, setMessage] = useState(null)

  useEffect(() => {
    fetchCredentials()
  }, [])

  const fetchCredentials = async () => {
    try {
      const response = await api.get('/credentials/')
      const credsMap = {}
      response.data.forEach(cred => {
        credsMap[cred.service_type] = cred
      })
      setCredentials(credsMap)
    } catch (error) {
      console.error('Failed to fetch credentials:', error)
    }
  }

  const handleSaveCredential = async (serviceType, credData) => {
    setSaving({ ...saving, [serviceType]: true })
    setMessage(null)

    try {
      await api.post('/credentials', {
        service_type: serviceType,
        credentials: credData
      })
      setMessage({ type: 'success', text: `${serviceType} credentials saved successfully!` })
      await fetchCredentials()
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to save credentials' })
    } finally {
      setSaving({ ...saving, [serviceType]: false })
    }
  }

  const handleTestCredential = async (serviceType) => {
    setTesting({ ...testing, [serviceType]: true })
    setMessage(null)

    try {
      const response = await api.post(`/credentials/${serviceType}/test`)
      setMessage({
        type: response.data.status === 'success' ? 'success' : 'error',
        text: response.data.message
      })
      await fetchCredentials()
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to test connection' })
    } finally {
      setTesting({ ...testing, [serviceType]: false })
    }
  }

  const handleGoogleOAuth = async () => {
    try {
      const response = await api.get('/oauth/google/authorize')
      window.location.href = response.data.authorization_url
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to initiate Google OAuth' })
    }
  }

  return (
    <div className="max-w-4xl space-y-6">
      {message && (
        <div className={`p-4 rounded-lg ${
          message.type === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
        }`}>
          {message.text}
        </div>
      )}

      {/* Slack Configuration */}
      <div className="bg-white rounded-xl shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Slack Configuration</h2>
          {credentials.slack && (
            <StatusBadge status={credentials.slack.test_status} />
          )}
        </div>

        <form onSubmit={(e) => {
          e.preventDefault()
          const formData = new FormData(e.target)
          handleSaveCredential('slack', {
            bot_token: formData.get('slack_bot_token'),
            app_token: formData.get('slack_app_token'),
            signing_secret: formData.get('slack_signing_secret')
          })
        }}>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Bot Token
              </label>
              <input
                type="text"
                name="slack_bot_token"
                placeholder="xoxb-your-bot-token"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                App Token (Optional)
              </label>
              <input
                type="text"
                name="slack_app_token"
                placeholder="xapp-your-app-token"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Signing Secret
              </label>
              <input
                type="text"
                name="slack_signing_secret"
                placeholder="your-signing-secret"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="mt-4 flex gap-3">
            <button
              type="submit"
              disabled={saving.slack}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center"
            >
              {saving.slack && <Loader2 className="animate-spin mr-2 h-4 w-4" />}
              Save Credentials
            </button>
            {credentials.slack && (
              <button
                type="button"
                onClick={() => handleTestCredential('slack')}
                disabled={testing.slack}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 flex items-center"
              >
                {testing.slack && <Loader2 className="animate-spin mr-2 h-4 w-4" />}
                Test Connection
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Azure OpenAI Configuration */}
      <div className="bg-white rounded-xl shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Azure OpenAI Configuration</h2>
          {credentials.azure_openai && (
            <StatusBadge status={credentials.azure_openai.test_status} />
          )}
        </div>

        <form onSubmit={(e) => {
          e.preventDefault()
          const formData = new FormData(e.target)
          handleSaveCredential('azure_openai', {
            endpoint: formData.get('azure_endpoint'),
            api_key: formData.get('azure_api_key'),
            deployment: formData.get('azure_deployment'),
            api_version: formData.get('azure_api_version') || '2023-05-15'
          })
        }}>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Endpoint
              </label>
              <input
                type="text"
                name="azure_endpoint"
                placeholder="https://your-resource.openai.azure.com/"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                API Key
              </label>
              <input
                type="password"
                name="azure_api_key"
                placeholder="your-api-key"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Deployment Name
              </label>
              <input
                type="text"
                name="azure_deployment"
                placeholder="your-deployment-name"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                API Version
              </label>
              <input
                type="text"
                name="azure_api_version"
                defaultValue="2023-05-15"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="mt-4 flex gap-3">
            <button
              type="submit"
              disabled={saving.azure_openai}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center"
            >
              {saving.azure_openai && <Loader2 className="animate-spin mr-2 h-4 w-4" />}
              Save Credentials
            </button>
            {credentials.azure_openai && (
              <button
                type="button"
                onClick={() => handleTestCredential('azure_openai')}
                disabled={testing.azure_openai}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 flex items-center"
              >
                {testing.azure_openai && <Loader2 className="animate-spin mr-2 h-4 w-4" />}
                Test Connection
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Google Workspace Configuration */}
      <div className="bg-white rounded-xl shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Google Workspace Configuration</h2>
          {credentials.google_workspace && (
            <StatusBadge status={credentials.google_workspace.test_status} />
          )}
        </div>

        <p className="text-sm text-gray-600 mb-4">
          Connect your Google Workspace account to save summaries to Google Drive.
        </p>

        <div className="flex gap-3">
          <button
            onClick={handleGoogleOAuth}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center"
          >
            {credentials.google_workspace ? 'Reconnect' : 'Connect'} Google Workspace
          </button>
          {credentials.google_workspace && (
            <button
              onClick={() => handleTestCredential('google_workspace')}
              disabled={testing.google_workspace}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 flex items-center"
            >
              {testing.google_workspace && <Loader2 className="animate-spin mr-2 h-4 w-4" />}
              Test Connection
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

const StatusBadge = ({ status }) => {
  if (status === 'success') {
    return (
      <span className="flex items-center text-green-600 text-sm">
        <CheckCircle className="h-4 w-4 mr-1" />
        Connected
      </span>
    )
  }
  if (status === 'failed') {
    return (
      <span className="flex items-center text-red-600 text-sm">
        <XCircle className="h-4 w-4 mr-1" />
        Failed
      </span>
    )
  }
  return (
    <span className="flex items-center text-yellow-600 text-sm">
      <AlertCircle className="h-4 w-4 mr-1" />
      Pending
    </span>
  )
}

export default Settings
