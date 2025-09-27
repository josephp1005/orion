import React, { useState } from 'react';
import VerticalTimeline from '../components/VerticalTimeline';




const AskPage = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [events, setEvents] = useState([]);

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, { role: 'user', content: input }]);
      try {
        const response = await fetch(`http://localhost:5050/output?query=${encodeURIComponent(input)}`);
        console.log(response);
        const data = await response.json();
        setMessages(msgs => [...msgs, { role: 'assistant', content: data.response }]);
        setEvents(data.docs);
      } catch (error) {
        setMessages(msgs => [...msgs, { role: 'assistant', content: 'Error fetching response.' }]);
      }
      setInput('');
    }
  };

  return (
    <div style={{ display: 'flex', height: '100%' }}>
      {/* Left: chat and input UI */}
      <div style={{ flex: 1 }}>
        <div className="flex flex-col h-full">
          <div className="flex-1 overflow-y-auto p-6">
            <div className="max-w-3xl mx-auto w-full space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-lg p-3 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                    }`}
                  >
                    <p>{message.content}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="p-4 border-t border-border">
            <div className="max-w-3xl mx-auto flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question..."
                className="flex-1 px-3 py-2 rounded-md bg-muted border border-border focus:outline-none focus:ring-2 focus:ring-primary"
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              />
              <button
                onClick={handleSend}
                className="px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
      {/* Right: timeline */}
      <div style={{ width: '400px', marginLeft: '32px', height: '100%', overflowY: 'auto' }}>
        <VerticalTimeline events={events} />
      </div>
    </div>
  );
};

export default AskPage;
