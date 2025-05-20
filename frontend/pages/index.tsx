import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const formData = new FormData();
    formData.append("query", query);

    const res = await fetch("http://localhost:8000/search", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResults(data.results.map((r, i) => ({ url: r, explanation: data.explanations[i] })));
  };

  return (
    <div className="container">
      <h1>Visual Search Engine</h1>
      <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search for images..." />
      <button onClick={handleSearch}>Search</button>
      <div className="results">
        {results.map((r, i) => (
          <div key={i} className="card">
            <img src={r.url} alt="result" />
            <p>{r.explanation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
