import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const Block = ({ block }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(block.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  switch (block.kind) {
    case 'heading':
      return <h1 className="text-3xl font-bold text-white mt-1 mb-4">{block.content}</h1>;
    case 'markdown':
      return (
        <div className="prose prose-invert max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{block.content}</ReactMarkdown>
        </div>
      );
    case 'code':
      return (
        <div className="bg-gray-900 rounded-lg my-4">
          <div className="flex justify-between items-center px-4 py-2 bg-gray-800 rounded-t-lg">
            <span className="text-gray-400 text-sm">Code Block</span>
            <button
              onClick={handleCopy}
              className="text-sm text-white bg-gray-700 hover:bg-gray-600 rounded px-2 py-1 transition-colors"
            >
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <pre className="p-4 text-white overflow-x-auto">
            <code>{block.content}</code>
          </pre>
        </div>
      );
    default:
      return null;
  }
};

export default Block;
