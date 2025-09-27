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
      setInput("");
      try {
        const response = await fetch(`http://localhost:5050/output?query=${encodeURIComponent(input)}`);
        console.log(response);
        const data = await response.json();
        setMessages(msgs => [...msgs, { role: 'assistant', content: data.response }]);
        setEvents(data.docs);
      } catch (error) {
        setMessages(msgs => [...msgs, { role: 'assistant', content: 'Error fetching response.' }]);
      }
    }
  };

  return (
    <div className="flex flex-1 h-full w-full">
      {/* Chat interface - takes full width */}
      <div className="flex flex-col flex-1 min-w-0 w-full">
        <div className="flex-1 overflow-y-auto p-6 w-full">
          <div className="max-w-4xl mx-auto space-y-4 w-full">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex w-full ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-2xl p-3 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Input section - fixed at bottom, full width */}
        <div className="flex-shrink-0 p-6 border-t border-border w-full">
          <div className="max-w-4xl mx-auto w-full">
            <div className="flex gap-2 w-full">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question..."
                className="flex-1 px-3 py-2 rounded-md bg-muted border border-border focus:outline-none focus:ring-2 focus:ring-primary min-w-0"
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              />
              <button
                onClick={handleSend}
                className="px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90 flex-shrink-0"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Right: timeline (render only when we have events) */}
      {events?.length > 0 && (
        <div className="flex-shrink-0 w-[400px] border-l border-border overflow-y-auto">
          <div className="p-6">
            <VerticalTimeline events={events} />
          </div>
        </div>
      )}
    </div>
  );
};

export default AskPage;