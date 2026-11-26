export default function Message({ message }) {

  return (

    <div className={`flex mb-6 ${
      message.role === "user"
        ? "justify-end"
        : "justify-start"
    }`}>

      <div className={`max-w-[80%] p-4 rounded-2xl whitespace-pre-wrap ${
        message.role === "user"
          ? "bg-blue-600"
          : "bg-slate-800"
      }`}>

        {message.content}

        {message.sources?.length > 0 && (

          <div className="mt-4 border-t border-slate-600 pt-3 text-sm">

            <p className="font-semibold mb-2">Sources:</p>

            {message.sources.map((source, index) => (

              <p key={index} className="text-blue-300">

                {source.document} — Chunk {source.chunk_id + 1}

              </p>

            ))}

          </div>

        )}

      </div>

    </div>
  )
}