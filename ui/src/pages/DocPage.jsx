import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function DocPage() {
  const [content, setContent] = useState("");

  useEffect(() => {
    const fakeContent = `
# Introduction

This is a sample documentation page.

## Code Block Example

\`\`\`javascript
console.log('Hello, Orion!');
\`\`\`

### List Example
- Item 1
- Item 2
- Item 3
`;
    setContent(fakeContent);
  }, []);

  return (
    <div className="mx-auto max-w-3xl px-6 py-8">
      <article className="prose prose-invert prose-pre:mt-0">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {content}
        </ReactMarkdown>
      </article>
    </div>
  );
}
