import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const res = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    setResults(data.results || []);
  };

  return (
    <main className="min-h-screen p-6 bg-gray-100 font-sans">
      <h1 className="text-3xl font-bold mb-6 text-center">Visual Search</h1>

      <div className="flex justify-center mb-6">
        <input
          type="text"
          placeholder="Search images (e.g. dog with hoodie)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="px-4 py-2 border rounded w-1/2 shadow"
        />
        <button
          onClick={handleSearch}
          className="ml-4 px-6 py-2 bg-blue-600 text-white rounded shadow hover:bg-blue-700"
        >
          Search
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {results.map((item: any, index) => (
          <div key={index} className="bg-white rounded shadow p-2">
            <img src={item.image_url} alt="" className="w-full rounded" />
            <p className="text-sm text-gray-700 mt-2">{item.explanation}</p>
          </div>
        ))}
      </div>
    </main>
  );
}