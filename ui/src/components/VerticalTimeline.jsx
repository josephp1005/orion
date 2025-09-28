// verticalTimeline.jsx
import React from "react";

/**
 * Usage:
 * <VerticalTimeline
 *   events={[
 *     { source: "GitHub", time: "2 hours ago", description: "PR #123 merged" },
 *     { source: "Slack", time: "Yesterday", description: "Release planning" },
 *   ]}
 * />
 */

const KIND_COLORS = {
  slack:   "#10b981", // emerald
  github:  "#6366f1", // indigo
  terminal:"#06b6d4", // cyan
  pdf:     "#f59e0b", // amber
  default: "#7c3aed", // purple (fallback)
};

const VerticalTimeline = ({ events = [] }) => {
  // const knownKinds = ["slack", "github", "terminal", "pdf"];
  // const kind = String(events.source || "").toLowerCase();
  // const isKnown = knownKinds.includes(kind);
  return (
    <div className="vtl">
      {/* Gradient spine */}
      <div className="vtl__spine" />

      <ol className="vtl__list" role="list">
        {events.map((event, idx) => (
          <li key={idx} className="vtl__item">
            {/* Node */}
            <span className="vtl__dot" aria-hidden />

            {/* Card */}
            <div className="vtl__card">
              {event.source && event.source.toLowerCase() === 'github' ? (
                <a 
                  href="https://github.com/josephp1005/orion/pull/10" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="vtl__source vtl__source--link"
                  data-source={event.source.toLowerCase()}
                >
                  {event.source}
                </a>
              ) : (
                <div 
                  className="vtl__source"
                  data-source={event.source ? event.source.toLowerCase() : undefined}
                >
                  {event.source}
                </div>
              )}
              <div className="vtl__time">{event.time}</div>
              {event.description ? (
                <div className="vtl__desc">{event.description}</div>
              ) : null}
            </div>
          </li>
        ))}
      </ol>

      {/* Styles (scoped) */}
      <style>{`
        :root {
          /* Use your app’s theme colors */
          --vtl-accent-1: #10b981; /* emerald/teal (matches sidebar "Ask a question") */
          --vtl-accent-2: #6366f1; /* indigo/purple (pairs with your glowing dots) */
          --vtl-bg: #0f1117;       /* slightly lighter than background for contrast */
          --vtl-card: rgba(255, 255, 255, 0.05);
          --vtl-card-border: rgba(255, 255, 255, 0.1);
          --vtl-text: #e5e7eb;     /* light gray text */
          --vtl-subtle: #9ca3af;   /* muted gray */
          --vtl-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
        }

        @media (prefers-color-scheme: light) {
          :root {
            --vtl-bg: #f7f8fb;
            --vtl-card: rgba(255,255,255,0.8);
            --vtl-card-border: rgba(12, 20, 33, 0.08);
            --vtl-text: #0c1421;
            --vtl-subtle: #4b5b76;
            --vtl-shadow: 0 8px 28px rgba(12,20,33,0.10);
          }
        }

        .vtl {
          position: relative;
          padding: 32px 0 8px 64px;
          margin: 32px 0;
          background: transparent;
          isolation: isolate; /* keep glow contained */
          font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial;
        }

        /* Spine */
        .vtl__spine {
          position: absolute;
          left: 28px;
          top: 0;
          bottom: 0;
          width: 3px;
          background: linear-gradient(180deg, var(--vtl-accent-1), var(--vtl-accent-2));
          border-radius: 2px;
          filter: drop-shadow(0 0 10px rgba(124,58,237,0.35)) drop-shadow(0 0 16px rgba(6,182,212,0.25));
          opacity: 0.9;
        }

        .vtl__list {
          list-style: none;
          margin: 0;
          padding: 0;
        }

        .vtl__item {
          position: relative;
          margin: 0 0 28px 0;
          animation: vtl-fade-in 400ms ease both;
          transform: translateY(6px);
        }

        .vtl__item:nth-child(1) { animation-delay: 20ms; }
        .vtl__item:nth-child(2) { animation-delay: 60ms; }
        .vtl__item:nth-child(3) { animation-delay: 100ms; }
        .vtl__item:nth-child(4) { animation-delay: 140ms; }

        @keyframes vtl-fade-in {
          from { opacity: 0; transform: translateY(8px); }
          to   { opacity: 1; transform: translateY(0); }
        }

        /* Dot */
        .vtl__dot {
          position: absolute;
          left: -5px;
          top: 52px;
          display: inline-block;
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: radial-gradient(circle at 35% 35%, #ffffff 0%, #e6faff 30%, #c8f3ff 60%, #a0ecff 100%);
          border: 3px solid transparent;
          box-shadow:
            0 0 0 2px rgba(255,255,255,0.6) inset,
            0 0 14px rgba(6,182,212,0.45),
            0 0 26px rgba(124,58,237,0.35);
        }

        /* Card */
        .vtl__card {
          margin-left: 35px;
          min-width: 90px;
          max-width: 120px;
          background: var(--vtl-card);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          border: 1px solid var(--vtl-card-border);
          border-radius: 14px;
          padding: 14px 16px 14px 16px;
          color: var(--vtl-text);
          box-shadow: var(--vtl-shadow);
          transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
        }

        .vtl__card:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 34px rgba(0,0,0,0.28);
          border-color: rgba(124,58,237,0.35);
        }

        .vtl__source {
          font-weight: 700;
          letter-spacing: 0.2px;
          display: block;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          text-decoration: none;
        }

        .vtl__source--link {
          cursor: pointer;
          transition: opacity 180ms ease;
        }

        .vtl__source--link:hover {
          opacity: 0.8;
          text-decoration: underline;
        }

        /* Default gradient for sources without specific colors */
        .vtl__source:not([data-source="slack"])
                    :not([data-source="github"])
                    :not([data-source="terminal"])
                    :not([data-source="pdf"]) {
          background: linear-gradient(90deg, var(--vtl-accent-1), var(--vtl-accent-2));
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
        }

        /* Specific colors for known sources */
        .vtl__source[data-source="slack"] { color: #10b981; }
        .vtl__source[data-source="github"] { color: #6366f1; }
        .vtl__source[data-source="terminal"] { color: #06b6d4; }
        .vtl__source[data-source="pdf"] { color: #f59e0b; }

        .vtl__time {
          font-size: 0.9rem;
          color: var(--vtl-subtle);
          margin-top: 2px;
        }

        .vtl__desc {
          font-size: 0.95rem;
          color: var(--vtl-text);
          margin-top: 10px;
          line-height: 1.35;
          opacity: 0.92;
        }

        /* Compact spacing for last item */
        .vtl__item:last-child { margin-bottom: 8px; }
      `}</style>
    </div>
  );
};

export default VerticalTimeline;