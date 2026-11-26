import { FileText, Plus, MessageSquare } from 'lucide-react'

export default function Sidebar({ documents, onNewChat }) {

  return (

    <aside className="w-64 bg-slate-900 h-screen p-5 border-r border-slate-800">

      <h1 className="text-2xl font-bold text-blue-400 mb-10">
        DocuMind AI
      </h1>

      <button
        onClick={onNewChat}
        className="w-full flex items-center gap-2 bg-blue-600 p-3 rounded-xl mb-8"
      >
        <Plus size={18} />
        New Chat
      </button>

      <h2 className="text-gray-400 text-sm mb-4">
        DOCUMENTS
      </h2>

      {documents.map((doc, index) => (

        <div key={index} className="flex items-center gap-2 mb-4 text-sm">

          <FileText size={18} className="text-blue-400" />

          <span className="truncate">{doc}</span>

        </div>

      ))}

      <div className="mt-10 text-gray-400 flex items-center gap-2">

        <MessageSquare size={18} />

        Conversations

      </div>

    </aside>
  )
}