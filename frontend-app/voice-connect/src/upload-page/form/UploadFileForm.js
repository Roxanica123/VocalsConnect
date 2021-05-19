import axios from "axios";
import Files from "react-butterfiles";
import React, { Component } from "react";

class UploadFileForm extends Component {
  state = {
    selectedFile: null,
    errors: null,
  };

  onFileUpload = async () => {
    console.log(this.state.selectedFile)
    const formData = new FormData();
    formData.append(
      "file",
      this.state.selectedFile.src.file,
      this.state.selectedFile.name
    );
    this.props.handler('waiting');
    const result = await axios.post("http://127.0.0.1:5000/upload", formData);
    this.props.handler("done", result.data)
  };

  fileData = () => {
    if (this.state.selectedFile) {
      return (
        <div>
          <h2> Uploaded File Details: </h2>
          <p> File Name: {this.state.selectedFile.name} </p>
          <p> File Type: {this.state.selectedFile.type} </p>
        </div>
      );
    } else {
      return (
        <div>
          <h4> Choose before Pressing the Upload button </h4>
        </div>
      );
    }
  };

  fileInputField = () => {
    return (
      <Files
        multiple={false}
        maxSize="10mb"
        multipleMaxSize="10mb"
        accept={["audio/mpeg", "audio/wav"]}
        onSuccess={(files) => {
          this.setState({ selectedFile: files[0] });
        }}
        onError={(errors) => this.setState({ errors: errors })}
      >
        {({ browseFiles }) => (
          <>
            <button onClick={browseFiles}>Select file</button>
          </>
        )}
      </Files>
    );
  };
  render() {
    return (
      <div>
        {this.fileInputField()}
        <button onClick={this.onFileUpload}> Upload!</button>
        <div> {this.fileData()} </div>
      </div>
    );
  }
}

export default UploadFileForm;
