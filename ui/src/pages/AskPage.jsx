// import React, { useState } from 'react';
// import VerticalTimeline from '../components/VerticalTimeline';

// const AskPage = () => {
//   const [messages, setMessages] = useState([
//     { role: 'assistant', content: 'How can I help you today?' }
//   ]);
//   const [input, setInput] = useState('');
//   const [events, setEvents] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);

//   const handleSend = async () => {
//     if (input.trim()) {
//       const userMessage = input;
//       setMessages([...messages, { role: 'user', content: userMessage }]);
//       setInput('');
//       setIsLoading(true);
      
//       try {
//         const response = await fetch(`http://localhost:5050/output?query=${encodeURIComponent(userMessage)}`);
//         console.log(response);
//         const data = await response.json();
//         setMessages(msgs => [...msgs, { role: 'assistant', content: data.response }]);
//         setEvents(data.docs);
//       } catch (error) {
//         setMessages(msgs => [...msgs, { role: 'assistant', content: 'Error fetching response.' }]);
//       } finally {
//         setIsLoading(false);
//       }
//     }
//   };

//   return (
//     <div className="grid grid-cols-4 h-full w-full">
//       {/* Chat interface - spans 3 columns (75%) */}
//       <div className="col-span-3 flex flex-col min-h-0">
//         <div className="flex-1 overflow-y-auto p-6">
//           <div className="max-w-4xl mx-auto w-full space-y-4">
//             {messages.map((message, index) => (
//               <div
//                 key={index}
//                 className={`flex w-full ${
//                   message.role === 'user' ? 'justify-end' : 'justify-start'
//                 }`}
//               >
//                 <div
//                   className={`max-w-2xl p-3 rounded-lg ${
//                     message.role === 'user'
//                       ? 'bg-primary text-primary-foreground'
//                       : 'bg-muted'
//                   }`}
//                 >
//                   <p className="whitespace-pre-wrap">{message.content}</p>
//                 </div>
//               </div>
//             ))}
            
//             {/* Loading bubbles */}
//             {isLoading && (
//               <div className="flex justify-start">
//                 <div className="bg-muted p-3 rounded-lg max-w-2xl">
//                   <div className="flex space-x-1 items-center">
//                     <div className="flex space-x-1">
//                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
//                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
//                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
//                     </div>
//                   </div>
//                 </div>
//               </div>
//             )}
//           </div>
//         </div>
        
//         {/* Input section - fixed at bottom */}
//         <div className="flex-shrink-0 p-6 border-t border-border">
//           <div className="max-w-4xl mx-auto w-full">
//             <div className="flex gap-2 w-full">
//               <input
//                 type="text"
//                 value={input}
//                 onChange={(e) => setInput(e.target.value)}
//                 placeholder="Ask a question..."
//                 className="flex-1 px-3 py-2 rounded-md bg-muted border border-border focus:outline-none focus:ring-2 focus:ring-primary min-w-0"
//                 onKeyPress={(e) => e.key === 'Enter' && handleSend()}
//               />
//               <button
//                 onClick={handleSend}
//                 disabled={isLoading}
//                 className="px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90 flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
//               >
//                 {isLoading ? 'Sending...' : 'Send'}
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>
      
//       {/* Timeline - spans 1 column (25%) */}
//       {/* <div className="col-span-1 border-l border-border bg-panel/50 flex flex-col">
//         <div className="p-6 border-b border-border">
//           <h3 className="font-semibold text-primary mb-2">Reference Timeline</h3>
//           <p className="text-sm text-text-muted">
//             {events.length === 0 
//               ? "Timeline for reference resources will appear here after your first question."
//               : "Resources used to answer your questions"
//             }
//           </p>
//         </div>
//         <div className="flex-1 overflow-y-auto">
//           {events.length > 0 && (
//             <div className="p-4">
//               <VerticalTimeline events={events} />
//             </div>
//           )}
//         </div>
//       </div> */}
//       <div className="col-span-1 border-l border-border bg-panel/50 flex flex-col h-screen overflow-hidden">
//         {/* Header (fixed) */}
//         <div className="p-6 border-b border-border shrink-0">
//           <h3 className="font-semibold text-primary mb-2">Reference Timeline</h3>
//           <p className="text-sm text-text-muted">
//             {events.length === 0
//               ? "Timeline for reference resources will appear here after your first question."
//               : "Resources used to answer your questions"}
//           </p>
//         </div>

//         {/* Scrollable body */}
//         <div id="timeline-scroll" className="min-h-0 flex-1 overflow-y-auto">
//           {events.length > 0 && (
//             <div className="p-4">
//               <VerticalTimeline events={events} />
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default AskPage;



import React, { useState } from 'react';
import VerticalTimeline from '../components/VerticalTimeline';

const AskPage = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // ✅ new state for timeline width toggle
  const [isWideTimeline, setIsWideTimeline] = useState(false);

  const handleSend = async () => {
    if (input.trim()) {
      const userMessage = input;
      setMessages([...messages, { role: 'user', content: userMessage }]);
      setInput('');
      setIsLoading(true);
      
      try {
        const response = await fetch(`http://localhost:5050/output?query=${encodeURIComponent(userMessage)}`);
        const data = await response.json();
        setMessages(msgs => [...msgs, { role: 'assistant', content: data.response }]);
        setEvents(data.docs);
      } catch (error) {
        setMessages(msgs => [...msgs, { role: 'assistant', content: 'Error fetching response.' }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    // ✅ grid adjusts automatically
    <div className="grid grid-cols-4 h-screen w-full overflow-hidden">
      {/* Chat interface */}
      <div className={`${isWideTimeline ? "col-span-2" : "col-span-3"} flex flex-col min-h-0`}>
        {/* Chat body */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto w-full space-y-4">
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

            {/* Loading bubbles */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-muted p-3 rounded-lg max-w-2xl">
                  <div className="flex space-x-1 items-center">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Input */}
        <div className="flex-shrink-0 p-6 border-t border-border">
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
                disabled={isLoading}
                className="px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90 flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Timeline */}
      <div className={`${isWideTimeline ? "col-span-2" : "col-span-1"} border-l border-border bg-panel/50 flex flex-col h-screen overflow-hidden`}>
        {/* Header with toggle */}
        <div className="p-6 border-b border-border shrink-0 flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-primary mb-2">Reference Timeline</h3>
            <p className="text-sm text-text-muted">
              {events.length === 0 
                ? "Timeline for reference resources will appear here after your first question."
                : "Resources used to answer your questions"}
            </p>
          </div>
          <button
            onClick={() => setIsWideTimeline(!isWideTimeline)}
            className="ml-4 px-2 py-1 text-xs rounded bg-primary/20 hover:bg-primary/40 text-primary transition"
          >
            {isWideTimeline ? "⟩ Shrink" : "Expand ⟨"}
          </button>
        </div>

        {/* Scrollable timeline */}
        <div id="timeline-scroll" className="min-h-0 flex-1 overflow-y-auto">
          {events.length > 0 && (
            <div className="p-4">
              <VerticalTimeline events={events} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AskPage;
