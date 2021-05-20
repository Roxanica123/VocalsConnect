import axios from "axios";
import Files from "react-butterfiles";
import React, { Component } from "react";

import Button from "@material-ui/core/Button";
import CloudUploadIcon from "@material-ui/icons/CloudUpload";
import AttachFileIcon from "@material-ui/icons/AttachFile";
import Grid from "@material-ui/core/Grid";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/styles";
import { Typography } from "@material-ui/core";
import "./UploadFileForm.css";

const useStyles = (theme) => ({
  root: {},
  button: {
    margin: "10px 0px",
    width: "30%",
    alignSelf: "center",
  },
  info:{
    color: "#fff5ee",
    padding: "30px",
  }
});

class UploadFileForm extends Component {
  state = {
    selectedFile: null,
    errors: null,
  };

  onFileUpload = async () => {
    if (this.state.selectedFile === null) return;
    const formData = new FormData();
    formData.append(
      "file",
      this.state.selectedFile.src.file,
      this.state.selectedFile.name
    );
    this.props.handler("waiting");
    try {
      const result = await axios.post("http://127.0.0.1:5000/upload", formData);
      this.props.handler("done", result.data);
    } catch (e) {
      this.props.handler("done", e.response.data.error, true);
    }
  };

  fileData = () => {
    const { classes } = this.props;
    if (this.state.selectedFile) {
      return (
        <Typography variant="subtitle1" className={classes.info}>
          {" "}
          You selected {this.state.selectedFile.name}, ready to upload?{" "}
        </Typography>
      );
    }
    if (this.state.errors != null) {
      return <Typography variant="subtitle1" className={classes.info}>{this.state.errors}</Typography>;
    }
    return (
      <Typography variant="subtitle1" className={classes.info}>
        We need an audio file to get to work. Make it have at least 20 seconds
        of vocals.
      </Typography>
    );
  };

  fileInputField = () => {
    const { classes } = this.props;
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
            <Button
              onClick={browseFiles}
              variant="contained"
              color="secondary"
              className={classes.button}
              startIcon={<AttachFileIcon />}
            >
              Select file
            </Button>
          </>
        )}
      </Files>
    );
  };
  render() {
    const { classes } = this.props;
    return (
      <Grid container className="grid">
        {this.fileInputField()}
        <Button
          onClick={this.onFileUpload}
          variant="outlined"
          color="secondary"
          className={classes.button}
          startIcon={<CloudUploadIcon />}
        >
          Upload
        </Button>
        <div> {this.fileData()} </div>
      </Grid>
    );
  }
}

UploadFileForm.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(useStyles)(UploadFileForm);
