import { useState } from "react";
import "./App.css";

function App() {
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState<string>("");

  async function pingBridge() {
    try {
      const r = await fetch("http://127.0.0.1:8765/health");
      const txt = await r.text();
      setStatus(txt); // should be "ok"
      alert(txt);
    } catch {
      setStatus("bridge offline");
      alert("bridge offline");
    }
  }

  return (
    <>
      {/* collapsed pill */}
      <div
        onClick={() => setOpen((v) => !v)}
        style={{
          position: "fixed", right: 16, bottom: 16, padding: "10px 14px",
          borderRadius: 999, background: "#111", color: "#fff", cursor: "pointer",
          userSelect: "none", zIndex: 9999
        }}
      >
        Copilot
      </div>

      {/* expanded card */}
      {open && (
        <div
          style={{
            position: "fixed", right: 16, bottom: 64, width: 360,
            background: "#fff", color: "#111", borderRadius: 12, padding: 14,
            boxShadow: "0 10px 30px rgba(0,0,0,.35)", zIndex: 9998
          }}
        >
          <div style={{ fontWeight: 600 }}>Productivity Copilot</div>
          <div style={{ opacity: 0.8, fontSize: 12 }}>Phase 0: overlay & wiring</div>
          <div style={{ marginTop: 8 }}>
            <button onClick={pingBridge}>Ping Bridge</button>
            <span style={{ marginLeft: 8, fontSize: 12, opacity: 0.7 }}>
              {status ? `status: ${status}` : ""}
            </span>
          </div>
        </div>
      )}
    </>
  );
}

export default App;
