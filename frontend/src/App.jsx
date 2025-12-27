import { useState } from "react";
import { enhanceImage } from "./api";
import "./App.css";

function App() {
  const [original, setOriginal] = useState(null);
  const [enhanced, setEnhanced] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    setOriginal(URL.createObjectURL(file));
    setLoading(true);
    const result = await enhanceImage(file);
    setEnhanced(result);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>AI Image Enhancer</h1>
      <input type="file" onChange={handleUpload} />

      {loading && <p className="loader">Enhancing your image...</p>}

      <div className="images">
        {original && <img src={original} />}
        {enhanced && <img src={enhanced} />}
      </div>

      {enhanced && (
        <a href={enhanced} download="enhanced.jpg">Download Image</a>
      )}
    </div>
  );
}

export default App;
