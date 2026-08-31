import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  async function search() {
    const response = await fetch("https://ai-notes-search-2.onrender.com/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();
    setAnswer(data.answer);
  }

  return (
    <div>
      <h1>AI Notes Search</h1>

      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question"
      />

      <button onClick={search}>Search</button>

      <h3>Answer:</h3>
      <p>{answer}</p>
    </div>
  );
}

export default App;