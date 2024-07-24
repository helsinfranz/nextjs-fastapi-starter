import { useState } from 'react';

interface Result {
  video?: string;
  audio?: string;
}

export default function Home() {
  const [videoUrl, setVideoUrl] = useState<string>('');
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/getVideoAudioUrls', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: videoUrl }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data: Result = await response.json();
      setResult(data);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <div>
      <h1>Video URL Fetcher</h1>
      <input
        type="text"
        value={videoUrl}
        onChange={(e) => setVideoUrl(e.target.value)}
        placeholder="Enter video URL"
      />
      <button onClick={handleSubmit}>Fetch Video & Audio URLs</button>

      {error && <p>Error: {error}</p>}
      {result && (
        <div>
          {result.video && <p><strong>Video URL:</strong> {result.video}</p>}
          {result.audio && <p><strong>Audio URL:</strong> {result.audio}</p>}
        </div>
      )}
    </div>
  );
}
