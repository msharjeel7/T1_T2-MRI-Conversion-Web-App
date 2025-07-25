// Import React and useState hook to manage component state (like variables)
import React, { useState } from "react";

// Axios is used to make HTTP requests (like POST to backend)
import axios from "axios";

// Toast is used to show popup messages (like success or error alerts)
import { ToastContainer, toast } from "react-toastify";

// CSS for toast notifications (pre-designed styles)
import "react-toastify/dist/ReactToastify.css";

//*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
//

// Define your main functional component named App
function App() {
  // State to store uploaded files (before sending to backend)
  const [images, setImages] = useState([]);

  // State to store preview URLs of uploaded files
  const [previews, setPreviews] = useState([]);

  // State to store the selected conversion direction ("T1_T2" or "T2_T1")
  const [direction, setDirection] = useState("T1_T2");

  // State to store preview URLs of converted images from backend
  const [results, setResults] = useState([]);

  //*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
  //
  // Function triggered when user uploads files
  const handleUpload = (e) => {
    const files = Array.from(e.target.files);   // Convert FileList to array
    setImages(files);   // Store images in state
    setPreviews(files.map((f) => URL.createObjectURL(f)));   // Create preview URLs for images
  };

  //*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
  //
  // Function triggered when user clicks the "Convert" button
  const handleConvert = async () => {
    // Show error if user tries to convert without uploading any image
    if (images.length === 0) {
      toast.error("⚠️ Upload at least one image before converting.", { position: "top-center" });
      return;
    }

    try {
      // Create form data to send to Flask backend (like a virtual form)
      const formData = new FormData();

      images.forEach((img) => formData.append("images", img));   // Append each image

      // Append selected direction (T1->T2 or T2->T1)
      formData.append("direction", direction);

      // Send POST request to `/convert` route of Flask server
      const res = await axios.post("/convert", formData);

      // Debug: log returned filenames
      console.log("Backend filenames:", res.data);

      // Initialize an array to store fetched converted image URLs
      const urls = [];

      // Loop through each returned filename from backend
      for (let r of res.data) {
        // Fetch the image file from backend (public URL)
        const resp = await fetch(`/static/results/${r.filename}`);

        // Log fetch status
        console.log(`Fetch ${r.filename}: status ${resp.status}`);

        // If image is missing or broken, skip it
        if (!resp.ok) {
          console.error(`Failed to fetch converted image: ${r.filename}`);
          continue;
        }

        // Convert fetched file (blob) to a previewable URL and store it
        const blob = await resp.blob();
        urls.push(URL.createObjectURL(blob));
      }


      // If no converted images successfully fetched, show error toast
      if (urls.length === 0) {
        toast.error("Conversion succeeded but previews failed to load.", { position: "top-center" });
      } else {
        setResults(urls);   // Show converted previews
        toast.success("Conversion complete — images previewed below.", { position: "top-center" });
      }
    } catch (err) {
      // If something fails (server down, image too large, etc.)
      console.error("Conversion process failed:", err);
      toast.error("Conversion failed — check console logs.", { position: "top-center" });
    }
  };

  //*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=**=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
  //

  // JSX that defines what is shown on screen (HTML-like syntax)
  return (
    <div className="min-h-screen p-8 text-white" style={{ backgroundColor: "#1f2937" }}>

      {/* This shows popup toasts at top center of page */}
      <ToastContainer autoClose={2000} />

       {/* Page heading */}
      <h1 className="text-4xl font-bold mb-6 text-[orange] text-center">T1 ↔ T2 Image Conversion</h1>

      {/* Main layout: responsive grid with 1 column on mobile, 2 on tablet, 3 on desktop */}
      <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        {/* Uploaded Preview Section */}
        <div className="bg-white p-4 rounded shadow text-black">
          <h2 className="text-xl font-semibold mb-4 text-center">Uploaded Images</h2>
          {previews.length ? (
            <div className="grid grid-cols-1 gap-4 place-items-center">
              {previews.map((src, i) => <img key={i} src={src} alt={`uploaded-${i}`} className="w-full mb-2 rounded" />)}
            </div>
          ) : <p className="text-center">No uploads yet.</p>}
        </div>

        {/* Conversion Controls Section (upload + select + button) */}
        <div className="flex flex-col justify-center items-center space-y-6">
          {/* File input (accepts multiple image files) */}
          <input type="file" multiple accept="image/*" onChange={handleUpload} className="text-white" />
          {/* Dropdown to select direction */}
          <select value={direction} onChange={(e) => setDirection(e.target.value)} className="p-2 rounded text-black">
            <option value="T1_T2">T1 → T2</option>
            <option value="T2_T1">T2 → T1</option>
          </select>
          {/* Button to trigger conversion */}
          <button onClick={handleConvert} className="bg-orange-500 hover:bg--600 text-white px-6 py-2 rounded">
            Convert
          </button>
        </div>

        {/* Converted Image Preview Section */}
        <div className="bg-white p-4 rounded shadow text-black">
          <h2 className="text-xl font-semibold mb-4 text-center">Converted Images</h2>
          {results.length ? (
            <div className="grid grid-cols-1 gap-4 place-items-center">
              {results.map((url, i) => <img key={i} src={url} alt={`converted-${i}`} className="w-full mb-2 rounded" />)}
            </div>
          ) : <p className="text-center">No conversions yet.</p>}
        </div>
      </div>
    </div>
  );
}

export default App;
