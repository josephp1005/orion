import React from "react";

const VerticalTimeline = ({ events }) => (
  <div style={{ position: "relative", margin: "40px 0", paddingLeft: "40px" }}>
    {/* Vertical line */}
    <div
      style={{
        position: "absolute",
        left: "20px",
        top: 0,
        bottom: 0,
        width: "4px",
        background: "#1976d2",
        borderRadius: "2px",
      }}
    />
    {events.map((event, idx) => (
      <div
        key={idx}
        style={{
          position: "relative",
          marginBottom: "40px",
        }}
      >
        {/* Dot on the timeline */}
        <div
          style={{
            position: "absolute",
            left: "12px",
            top: "8px",
            width: "16px",
            height: "16px",
            background: "#fff",
            border: "4px solid #1976d2",
            borderRadius: "50%",
            zIndex: 1,
          }}
        />
        {/* Box with event info */}
        <div
          style={{
            marginLeft: "40px",
            background: "#f5f5f5",
            borderRadius: "8px",
            padding: "16px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.07)",
            minWidth: "220px",
            maxWidth: "400px",
          }}
        >
          <div style={{ fontWeight: "bold", color: "#1976d2" }}>
            {event.type}
          </div>
          <div style={{ color: "#555", fontSize: "0.95em" }}>
            {event.time}
          </div>
        </div>
      </div>
    ))}
  </div>
);

export default VerticalTimeline;