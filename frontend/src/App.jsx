import { useState } from "react";
import { enhanceImage } from "./api";
import "./App.css";

function App() {
  const [original, setOriginal] = useState(null);
  const [enhanced, setEnhanced] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setOriginal(URL.createObjectURL(file));
    setEnhanced(null);
    setLoading(true);
    try {
      const result = await enhanceImage(file);
      setEnhanced(result);
    } catch (err) {
      console.error(err);
      alert("Enhancement failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="container card">
        <h1 className="title">AI Image Enhancer</h1>
        <p className="subtitle">Simple histogram equalization on luminance for clearer photos</p>

        <div className="controls">
          <label className="upload-btn">
            Upload Image
            <input type="file" accept="image/*" onChange={handleUpload} />
          </label>

          {enhanced && (
            <a className="download-btn" href={enhanced} download="enhanced.jpg">Download Image</a>
          )}
        </div>

        <div className="images">
          <div className="image-box">
            <div className="caption">Original</div>
            {original ? <img src={original} alt="Original" /> : <div className="placeholder">No image uploaded</div>}
          </div>

          <div className="image-box">
            <div className="caption">Enhanced</div>
            {loading ? <div className="loader">Enhancing your image...</div> : (enhanced ? <img src={enhanced} alt="Enhanced" /> : <div className="placeholder">No image yet</div>)}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
