import { useState } from 'react'
import { Send } from 'lucide-react'
import Message from './Message'

export default function ChatWindow({ messages, onSend, loading }) {

  const [question, setQuestion] = useState("")

  const submit = () => {

    if (!question.trim() || loading) return

    onSend(question)

    setQuestion("")
  }

  return (

    <div className="flex flex-col h-full">

      <div className="flex-1 overflow-y-auto p-6">

        {messages.map((message, index) => (

          <Message key={index} message={message} />

        ))}

        {loading && (
          <p className="text-blue-400 animate-pulse">
            DocuMind is thinking...
          </p>
        )}

      </div>

      <div className="p-5 border-t border-slate-700">

        <div className="flex gap-3 bg-slate-800 p-3 rounded-xl">

          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') submit()
            }}
            placeholder="Ask anything about your document..."
            className="flex-1 bg-transparent outline-none"
          />

          <button
            onClick={submit}
            disabled={loading}
            className="bg-blue-600 p-3 rounded-lg"
          >
            <Send size={18} />
          </button>

        </div>

      </div>

    </div>
  )
}