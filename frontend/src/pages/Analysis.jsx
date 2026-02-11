import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import Plot from 'react-plotly.js';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { datasetAPI } from '../services/api';

const Analysis = () => {
  const { datasetId } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [suggestedQuestions] = useState([
    "What are the main columns in this dataset?",
    "How is the data quality?",
    "What insights can you provide?",
    "Are there any outliers?",
    "What should I focus on?"
  ]);
  const chatEndRef = useRef(null);

  useEffect(() => {
    loadAnalysis();
    const interval = setInterval(() => {
      if (analysis?.status === 'processing') {
        loadAnalysis();
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [datasetId]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const loadAnalysis = async () => {
    try {
      const response = await datasetAPI.getAnalysis(datasetId);
      setAnalysis(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load analysis');
      setLoading(false);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userMessage = { role: 'user', content: chatInput };
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setChatLoading(true);

    try {
      const response = await datasetAPI.chat(datasetId, chatInput);
      const aiMessage = { role: 'assistant', content: response.data.response };
      setChatMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      const errorMessage = { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleSuggestedQuestion = (question) => {
    setChatInput(question);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mb-4"></div>
          <p className="text-xl text-gray-600">Loading analysis...</p>
        </div>
      </div>
    );
  }

  if (error || analysis?.status === 'processing') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mb-4"></div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis in Progress</h2>
          <p className="text-gray-600">Please wait while we analyze your data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex overflow-hidden bg-gray-50">
      {/* Left Side - AI Chatbot */}
      <div className="w-1/2 h-screen flex flex-col border-r border-gray-200 bg-white">
        {/* Chat Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6 shadow-lg flex-shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
              <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div>
              <h2 className="text-2xl font-bold">AI Assistant</h2>
              <p className="text-sm text-white/80">Ask me anything about your dataset</p>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {chatMessages.length === 0 && (
            <div className="text-center text-gray-500 mt-8">
              <svg className="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <p className="text-lg font-medium mb-2">Start a conversation</p>
              <p className="text-sm mb-6">Ask questions about your dataset analysis</p>
              
              {/* Suggested Questions */}
              <div className="space-y-2 max-w-md mx-auto">
                <p className="text-xs font-semibold text-gray-600 mb-3">Suggested questions:</p>
                {suggestedQuestions.map((question, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSuggestedQuestion(question)}
                    className="w-full text-left px-4 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-lg text-sm transition border border-indigo-200"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}
          {chatMessages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[75%] rounded-2xl px-5 py-3 ${
                msg.role === 'user' 
                  ? 'bg-indigo-600 text-white' 
                  : 'bg-gray-100 text-gray-900'
              }`}>
                {msg.role === 'assistant' ? (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    className="text-sm leading-relaxed prose prose-sm max-w-none"
                    components={{
                      p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                      strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />,
                      ul: ({node, ...props}) => <ul className="list-none space-y-1 my-2" {...props} />,
                      ol: ({node, ...props}) => <ol className="list-none space-y-1 my-2" {...props} />,
                      li: ({node, ...props}) => (
                        <li className="flex items-start gap-2" {...props}>
                          <span className="text-indigo-600 mt-1">•</span>
                          <span className="flex-1">{props.children}</span>
                        </li>
                      ),
                      h1: ({node, ...props}) => <h1 className="text-lg font-bold mb-2" {...props} />,
                      h2: ({node, ...props}) => <h2 className="text-base font-bold mb-2" {...props} />,
                      h3: ({node, ...props}) => <h3 className="text-sm font-bold mb-1" {...props} />,
                      code: ({node, inline, ...props}) => 
                        inline ? (
                          <code className="bg-gray-200 px-1.5 py-0.5 rounded text-xs font-mono" {...props} />
                        ) : (
                          <code className="block bg-gray-200 p-2 rounded text-xs font-mono my-2" {...props} />
                        ),
                      blockquote: ({node, ...props}) => (
                        <blockquote className="border-l-4 border-indigo-500 pl-3 italic my-2" {...props} />
                      ),
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                ) : (
                  <p className="text-sm leading-relaxed">{msg.content}</p>
                )}
              </div>
            </div>
          ))}
          {chatLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-2xl px-5 py-3">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Chat Input */}
        <form onSubmit={handleChatSubmit} className="p-6 border-t border-gray-200 bg-gray-50 flex-shrink-0">
          <div className="flex gap-3">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Type your question here..."
              className="flex-1 px-5 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              disabled={chatLoading}
            />
            <button
              type="submit"
              disabled={chatLoading || !chatInput.trim()}
              className="bg-indigo-600 text-white px-6 py-3 rounded-xl hover:bg-indigo-700 disabled:bg-gray-400 transition flex items-center gap-2 font-medium"
            >
              {chatLoading ? (
                <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              )}
              Send
            </button>
          </div>
        </form>
      </div>

      {/* Right Side - Dashboard/Report */}
      <div className="w-1/2 h-screen overflow-y-auto bg-gray-50">
        <div className="p-6">
          {/* Header */}
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{analysis.filename}</h1>
            <p className="text-gray-600">Analysis Report</p>
          </div>

          {/* Overview Cards */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 font-medium">Rows</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    {analysis.eda_results?.overview?.rows?.toLocaleString()}
                  </p>
                </div>
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 font-medium">Columns</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    {analysis.eda_results?.overview?.columns}
                  </p>
                </div>
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 font-medium">Quality</p>
                  <p className="text-2xl font-bold text-green-600 mt-1">
                    {analysis.eda_results?.data_quality?.completeness?.toFixed(1)}%
                  </p>
                </div>
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 font-medium">Duplicates</p>
                  <p className="text-2xl font-bold text-orange-600 mt-1">
                    {analysis.cleaning_report?.duplicates_removed}
                  </p>
                </div>
                <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Cleaning Report */}
          <div className="bg-white rounded-xl shadow-sm p-5 mb-6 border border-gray-100">
            <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
              <svg className="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Cleaning Actions
            </h3>
            <div className="space-y-2">
              {analysis.cleaning_report?.actions_taken?.map((action, idx) => (
                <div key={idx} className="flex items-start bg-green-50 p-3 rounded-lg text-sm">
                  <svg className="w-4 h-4 text-green-500 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">{action}</span>
                </div>
              ))}
            </div>
          </div>

          {/* AI Insights */}
          <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl shadow-sm p-5 mb-6 border border-indigo-100">
            <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
              <svg className="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              AI Insights
            </h3>
            <div className="text-sm text-gray-700 space-y-2">
              {analysis.ai_insights?.split('\n\n').map((paragraph, idx) => (
                <p key={idx} className="leading-relaxed">{paragraph}</p>
              ))}
            </div>
          </div>

          {/* Visualizations */}
          <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
            <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Visualizations
            </h3>
            <div className="space-y-4">
              {analysis.visualizations?.map((viz, idx) => (
                <div key={idx} className="border border-gray-200 rounded-lg p-3 bg-gray-50">
                  <Plot
                    data={JSON.parse(viz.data).data}
                    layout={{
                      ...JSON.parse(viz.data).layout,
                      autosize: true,
                      height: 300,
                      paper_bgcolor: 'rgba(0,0,0,0)',
                      plot_bgcolor: 'rgba(0,0,0,0)',
                    }}
                    useResizeHandler
                    style={{ width: '100%' }}
                    config={{ responsive: true }}
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analysis;
