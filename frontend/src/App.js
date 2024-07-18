import React from "react";
import "./App.css";
import FileUpload from "./components/FileUpload";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="content-wrapper">
          <h1>Data Inference and Conversion</h1>
          <FileUpload />
        </div>
      </header>
    </div>
  );
}

export default App;
