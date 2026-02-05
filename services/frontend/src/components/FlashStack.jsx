import React from "react";
import { useFlash } from "../context/FlashContext.jsx";

export default function FlashStack() {
  const { messages } = useFlash();

  if (messages.length === 0) return <div className="flash" />;

  return (
    <div className="flash">
      {messages.map((m) => (
        <div
          key={m.id}
          className={`alert ${m.type === "success" ? "alert-success" : ""} ${
            m.type === "error" ? "alert-error" : ""
          }`}
        >
          {m.text}
        </div>
      ))}
    </div>
  );
}
