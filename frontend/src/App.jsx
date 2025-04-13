import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [mode, setMode] = useState("grade");
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [history, setHistory] = useState([]);

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:8000/analyze/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode: mode, user_input: input })
    });
    const data = await res.json();
    setResponse(data.response);
    fetchHistory();
  };

  const fetchHistory = async () => {
    const res = await fetch("http://localhost:8000/history/");
    const data = await res.json();
    setHistory(data.history);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="App">
      <h1>📄 Document Analyzer</h1>

      <div>
        <label>Mode:</label>
        <select value={mode} onChange={e => setMode(e.target.value)}>
          <option value="create">Create</option>
          <option value="feedback">Feedback</option>
          <option value="grade">Grade</option>
        </select>
      </div>

      <textarea
        rows={10}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter your prompt (e.g., assignment + rubric)"
      />
      <button onClick={handleSubmit}>Submit</button>

      {response && (
        <div className="output">
          <h3>LLM Response:</h3>
          <pre>{response}</pre>
        </div>
      )}

      <div className="history">
        <h3>History</h3>
        {history.map((entry) => (
          <div key={entry[0]}>
            <strong>{entry[4]}</strong> — <em>{entry[1]}</em>
            <details>
              <summary>Input</summary>
              <pre>{entry[2]}</pre>
            </details>
            <details>
              <summary>Output</summary>
              <pre>{entry[3]}</pre>
            </details>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
