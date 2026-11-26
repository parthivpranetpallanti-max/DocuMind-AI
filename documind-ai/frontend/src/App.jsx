import { useState } from 'react'

import Sidebar from './components/Sidebar'
import UploadDocument from './components/UploadDocument'
import ChatWindow from './components/ChatWindow'

export default function App() {

  const [documents, setDocuments] = useState([])

  const [messages, setMessages] = useState([])

  const [loading, setLoading] = useState(false)

  const [uploaded, setUploaded] = useState(false)

  const API = "http://127.0.0.1:8000"

  async function uploadDocument(file) {

    setLoading(true)

    try {

      const formData = new FormData()

      formData.append("file", file)

      const response = await fetch(`${API}/upload`, {
        method: "POST",
        body: formData
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed")
      }

      setDocuments(prev => [...new Set([...prev, file.name])])

      setUploaded(true)

      setMessages(prev => [...prev, {
        role: "assistant",
        content: `Successfully processed ${file.name}. Created ${data.total_chunks} text chunks. You can now ask questions!`
      }])

    } catch (error) {

      alert(error.message)

    }

    setLoading(false)
  }

  async function sendQuestion(question) {

    setMessages(prev => [
      ...prev,
      { role: "user", content: question }
    ])

    setLoading(true)

    try {

      const response = await fetch(`${API}/ask`, {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({ question })

      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Question failed")
      }

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources
        }
      ])

    } catch (error) {

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: `Error: ${error.message}`
        }
      ])

    }

    setLoading(false)
  }

  function newChat() {

    setMessages([])

  }

  return (

    <div className="flex h-screen overflow-hidden">

      <Sidebar
        documents={documents}
        onNewChat={newChat}
      />

      <main className="flex-1 flex flex-col">

        <header className="p-5 border-b border-slate-800">

          <h1 className="text-xl font-bold">
            Your Documents. Your Answers.
          </h1>

          <p className="text-gray-400 text-sm">
            AI-powered document intelligence using RAG and FAISS
          </p>

        </header>

        {!uploaded ? (

          <div className="flex-1 flex items-center justify-center p-10">

            <div className="w-full max-w-2xl">

              <h2 className="text-3xl font-bold text-center mb-8">
                Welcome to DocuMind AI
              </h2>

              <UploadDocument
                onUpload={uploadDocument}
                loading={loading}
              />

            </div>

          </div>

        ) : (

          <ChatWindow
            messages={messages}
            onSend={sendQuestion}
            loading={loading}
          />

        )}

      </main>

    </div>
  )
}