import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

const POLICY_DOCS = [
  {
    label: 'Emergency Benefits',
    href: 'https://www.opm.gov/policy-data-oversight/pay-leave/pay-administration/#url=Emergency',
  },
  {
    label: 'Elder Care Handbook',
    href: 'https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/#url=Elder-Care',
  },
  {
    label: 'Dismissal & Closure Procedures',
    href: 'https://www.opm.gov/policy-data-oversight/pay-leave/work-schedules/#url=Closure',
  },
]

function CitationBadge({ source, page }) {
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
      <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      {source}{page ? ` · p${page}` : ''}
    </span>
  )
}

function ScoreBadge({ score }) {
  if (score == null) return null
  const pct = Math.round(score * 100)
  const color = pct >= 80 ? 'text-emerald-400' : pct >= 60 ? 'text-yellow-400' : 'text-red-400'
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-white/5 border border-white/10 ${color}`}>
      <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      Quality {pct}%
    </span>
  )
}

function HitlBanner() {
  return (
    <div className="flex items-center gap-2 mt-2 px-3 py-2 rounded-lg bg-yellow-400/10 border border-yellow-400/30 text-yellow-300 text-xs font-medium">
      <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      Under human review — a compliance officer will follow up shortly.
    </div>
  )
}

function Spinner() {
  return (
    <div className="flex items-center gap-3 px-1 py-1">
      <div className="w-8 h-8 rounded-full bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0">
        <svg className="w-4 h-4 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      </div>
      <div className="flex gap-1.5 items-center">
        <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce [animation-delay:0ms]" />
        <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce [animation-delay:150ms]" />
        <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce [animation-delay:300ms]" />
      </div>
    </div>
  )
}

function AgentMessage({ msg }) {
  return (
    <div className="flex items-start gap-3 max-w-[80%]">
      <div className="w-8 h-8 rounded-full bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0 mt-0.5">
        <svg className="w-4 h-4 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      </div>
      <div className="flex-1 min-w-0">
        <div className="px-4 py-3 rounded-2xl rounded-tl-sm bg-[#1e2433] border border-white/[0.08] text-slate-200 text-sm leading-relaxed">
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              strong: ({ children }) => <strong className="font-semibold text-slate-100">{children}</strong>,
              em: ({ children }) => <em className="italic text-slate-300">{children}</em>,
              h1: ({ children }) => <h1 className="text-base font-semibold text-slate-100 mt-3 mb-1 first:mt-0">{children}</h1>,
              h2: ({ children }) => <h2 className="text-sm font-semibold text-slate-100 mt-3 mb-1 first:mt-0">{children}</h2>,
              h3: ({ children }) => <h3 className="text-sm font-medium text-slate-200 mt-2 mb-1 first:mt-0">{children}</h3>,
              ul: ({ children }) => <ul className="list-disc list-outside pl-4 mb-2 space-y-0.5">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal list-outside pl-4 mb-2 space-y-0.5">{children}</ol>,
              li: ({ children }) => <li className="text-slate-300">{children}</li>,
              code: ({ inline, children }) =>
                inline ? (
                  <code className="px-1.5 py-0.5 rounded bg-white/[0.08] text-indigo-300 font-mono text-xs">{children}</code>
                ) : (
                  <code className="block px-3 py-2 my-2 rounded-lg bg-black/30 text-slate-300 font-mono text-xs overflow-x-auto whitespace-pre">{children}</code>
                ),
              pre: ({ children }) => <>{children}</>,
              blockquote: ({ children }) => (
                <blockquote className="border-l-2 border-indigo-500/50 pl-3 my-2 text-slate-400 italic">{children}</blockquote>
              ),
              a: ({ href, children }) => (
                <a href={href} target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 underline underline-offset-2 transition-colors">{children}</a>
              ),
              hr: () => <hr className="my-3 border-white/[0.08]" />,
            }}
          >
            {msg.answer}
          </ReactMarkdown>
        </div>
        {msg.needs_hitl && <HitlBanner />}
        {(msg.citations?.length > 0 || msg.critique_score != null) && (
          <div className="flex flex-wrap items-center gap-2 mt-2 px-1">
            {msg.citations?.map((c, i) => (
              <CitationBadge key={i} source={c.source} page={c.page} />
            ))}
            <ScoreBadge score={msg.critique_score} />
          </div>
        )}
      </div>
    </div>
  )
}

function UserMessage({ text }) {
  return (
    <div className="flex justify-end">
      <div className="max-w-[75%] px-4 py-3 rounded-2xl rounded-tr-sm bg-indigo-600 text-white text-sm leading-relaxed shadow-lg shadow-indigo-900/30 whitespace-pre-wrap">
        {text}
      </div>
    </div>
  )
}

function WelcomePrompt({ onSuggest }) {
  const suggestions = [
    'What are my emergency leave benefits?',
    'How does elder care leave work?',
    'What happens during office closures?',
  ]
  return (
    <div className="flex flex-col items-center justify-center h-full gap-6 px-6 text-center select-none">
      <div className="w-16 h-16 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center">
        <svg className="w-8 h-8 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      </div>
      <div>
        <h2 className="text-xl font-semibold text-slate-100 mb-2">Compliance Assistant</h2>
        <p className="text-slate-400 text-sm max-w-xs leading-relaxed">
          Ask me anything about company policies, benefits, leave procedures, or workplace guidelines.
        </p>
      </div>
      <div className="grid grid-cols-1 gap-2 w-full max-w-sm">
        {suggestions.map((q) => (
          <button
            key={q}
            onClick={() => onSuggest(q)}
            className="px-3 py-2 rounded-lg bg-white/[0.04] border border-white/[0.08] text-slate-400 text-xs text-left cursor-pointer hover:bg-white/[0.07] hover:text-slate-300 hover:border-white/[0.14] transition-all"
          >
            "{q}"
          </button>
        ))}
      </div>
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  function resetTextarea() {
    if (textareaRef.current) {
      textareaRef.current.style.height = '1.5rem'
    }
  }

  async function sendMessage(overrideQuery) {
    const query = (overrideQuery ?? input).trim()
    if (!query || loading) return

    setMessages((prev) => [...prev, { role: 'user', text: query }])
    setInput('')
    resetTextarea()
    setLoading(true)

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setMessages((prev) => [...prev, { role: 'agent', ...data }])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'agent',
          answer: `Sorry, something went wrong: ${err.message}. Please try again.`,
          citations: [],
          needs_hitl: false,
          critique_score: null,
        },
      ])
    } finally {
      setLoading(false)
      setTimeout(() => inputRef.current?.focus(), 50)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  function handleTextareaChange(e) {
    setInput(e.target.value)
    e.target.style.height = 'auto'
    e.target.style.height = Math.min(e.target.scrollHeight, 160) + 'px'
  }

  return (
    <div className="flex h-screen bg-[#0f1117] text-slate-100 overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="w-64 shrink-0 flex flex-col bg-[#13161f] border-r border-white/[0.06]">
        {/* Logo */}
        <div className="px-5 py-5 border-b border-white/[0.06]">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-900/50">
              <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div>
              <p className="text-sm font-semibold leading-tight text-slate-100">Compliance</p>
              <p className="text-xs text-slate-500 leading-tight">Policy Agent</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-5 overflow-y-auto">
          <p className="px-2 mb-3 text-[10px] font-semibold uppercase tracking-widest text-slate-600">
            Policy Documents
          </p>
          <ul className="space-y-0.5">
            {POLICY_DOCS.map((doc) => (
              <li key={doc.label}>
                <a
                  href={doc.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-slate-400 text-sm hover:bg-white/[0.06] hover:text-slate-200 transition-all group"
                >
                  <svg className="w-4 h-4 shrink-0 text-slate-600 group-hover:text-indigo-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="leading-snug flex-1">{doc.label}</span>
                  <svg className="w-3 h-3 opacity-0 group-hover:opacity-50 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* Status footer */}
        <div className="px-5 py-4 border-t border-white/[0.06]">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-50" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
            </span>
            <span className="text-xs text-slate-500">Agent online</span>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="px-6 py-4 border-b border-white/[0.06] bg-[#0f1117]/80 backdrop-blur-sm flex items-center justify-between shrink-0">
          <div>
            <h1 className="text-base font-semibold text-slate-100">Compliance Chat</h1>
            <p className="text-xs text-slate-500 mt-0.5">Ask questions about your workplace policies</p>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/[0.04] border border-white/[0.08]">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            <span className="text-xs text-slate-400 font-medium">LangGraph · GPT-4o</span>
          </div>
        </header>

        {/* Messages area */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-5">
          {messages.length === 0 && !loading ? (
            <WelcomePrompt onSuggest={(q) => sendMessage(q)} />
          ) : (
            <>
              {messages.map((msg, i) =>
                msg.role === 'user' ? (
                  <UserMessage key={i} text={msg.text} />
                ) : (
                  <AgentMessage key={i} msg={msg} />
                )
              )}
              {loading && <Spinner />}
            </>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input bar */}
        <div className="px-6 py-4 border-t border-white/[0.06] bg-[#0f1117]/80 backdrop-blur-sm shrink-0">
          <div className="flex items-end gap-3 bg-[#1e2433] border border-white/[0.10] rounded-2xl px-4 py-3 focus-within:border-indigo-500/50 focus-within:ring-1 focus-within:ring-indigo-500/20 transition-all">
            <textarea
              ref={(el) => {
                inputRef.current = el
                textareaRef.current = el
              }}
              value={input}
              onChange={handleTextareaChange}
              onKeyDown={handleKeyDown}
              placeholder="Ask about policies, benefits, or procedures…"
              rows={1}
              disabled={loading}
              className="flex-1 bg-transparent text-sm text-slate-200 placeholder-slate-500 resize-none outline-none leading-relaxed disabled:opacity-50 min-h-[1.5rem] max-h-40"
              style={{ height: '1.5rem' }}
            />
            <button
              onClick={() => sendMessage()}
              disabled={!input.trim() || loading}
              className="shrink-0 w-8 h-8 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center transition-all active:scale-95 shadow-md shadow-indigo-900/40"
              aria-label="Send message"
            >
              {loading ? (
                <svg className="w-4 h-4 text-white animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
              ) : (
                <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.269 20.876L5.999 12zm0 0h7.5" />
                </svg>
              )}
            </button>
          </div>
          <p className="mt-2 text-center text-xs text-slate-600">
            <kbd className="px-1 py-0.5 rounded bg-white/[0.06] text-slate-500 font-mono text-[10px]">Enter</kbd>
            {' '}to send ·{' '}
            <kbd className="px-1 py-0.5 rounded bg-white/[0.06] text-slate-500 font-mono text-[10px]">Shift+Enter</kbd>
            {' '}for new line
          </p>
        </div>
      </div>
    </div>
  )
}
