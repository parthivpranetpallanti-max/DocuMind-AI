import { Upload } from 'lucide-react'

export default function UploadDocument({ onUpload, loading }) {

  return (

    <div className="border-2 border-dashed border-slate-600 rounded-2xl p-10 text-center">

      <Upload size={40} className="mx-auto mb-4 text-blue-400" />

      <h2 className="text-xl font-semibold mb-2">
        Upload Your Document
      </h2>

      <p className="text-gray-400 mb-5">
        Upload PDF, DOCX or TXT files
      </p>

      <label className="bg-blue-600 px-6 py-3 rounded-xl cursor-pointer">

        {loading ? "Processing..." : "Choose File"}

        <input
          type="file"
          accept=".pdf,.docx,.txt"
          className="hidden"
          disabled={loading}
          onChange={(e) => {
            if (e.target.files[0]) {
              onUpload(e.target.files[0])
              e.target.value = ""
            }
          }}
        />

      </label>

    </div>
  )
}