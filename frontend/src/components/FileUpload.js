import React, { useState, useRef } from "react";
import axios from "axios";
import "../styles/FileUpload.css";
import uploadIcon from "../assets/upload-icon.png";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [inferredTypes, setInferredTypes] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadStatus(null);
    setErrorMessage("");
    setIsLoading(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    setFile(droppedFile);
    setUploadStatus(null);
    setErrorMessage("");
    setIsLoading(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleBrowseClick = (e) => {
    fileInputRef.current.click(); // Simulate a click event on the file input element
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    setIsLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/uploaded-files/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setInferredTypes(response.data.inferred_types);
      setIsLoading(false);
      setUploadStatus("success");
    } catch (error) {
      console.error("Error uploading file:", error);
      setIsLoading(false);
      setUploadStatus("error");
      if (error.response && error.response.data.error) {
        setErrorMessage(error.response.data.error);
      }
    }
  };

  const dataTypeMapping = {
    object: "Text",
    "datetime64[ns]": "Date",
    datetime64: "Date",
    int64: "Integer",
    int32: "Integer",
    int16: "Integer",
    int8: "Integer",
    uint64: "Integer",
    uint32: "Integer",
    uint16: "Integer",
    uint8: "Integer",
    float64: "Float",
    float32: "Float",
    bool: "Boolean",
    category: "Category",
    "timedelta64[ns]": "Time Delta",
    complex: "Complex",
    complex64: "Complex",
    complex128: "Complex",
  };

  return (
    <div className="file-upload-container">
      <div className="file-upload-box">
        <form onSubmit={handleSubmit} className="upload-form">
          <div
            className="drag-drop-area"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
          >
            <input
              type="file"
              id="file-input"
              onChange={handleFileChange}
              ref={fileInputRef}
              style={{ display: "none" }}
            />
            <label htmlFor="file-input" className="drag-drop-label">
              <img src={uploadIcon} alt="Upload Icon" className="icon-upload" />
              <div>Drag and Drop files to upload</div>
              <div>or</div>
              <button
                type="button"
                className="btn btn-primary browse-button"
                onClick={handleBrowseClick}
              >
                Browse
              </button>
            </label>
          </div>

          {file && (
            <div className="file-details">
              <p>File: {file.name}</p>
              <button className="upload-button" type="submit">
                Upload
              </button>
            </div>
          )}
        </form>

        {isLoading && <div className="spinner"></div>}

        {uploadStatus === "error" && errorMessage && (
          <div className="upload-error">
            <p>{errorMessage}</p>
          </div>
        )}

        {inferredTypes && (
          <div className="inferred-types">
            <h2>Inferred Data Types</h2>
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>Column</th>
                  <th>Data Type</th>
                </tr>
              </thead>
              <tbody>
                {Object.keys(inferredTypes).map((column) => (
                  <tr key={column}>
                    <td>{column}</td>
                    <td>
                      {dataTypeMapping[inferredTypes[column]] ||
                        inferredTypes[column]}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
