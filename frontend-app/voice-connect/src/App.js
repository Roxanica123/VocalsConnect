import React, { Component } from "react";
import UploadFileForm from "./upload-page/form/UploadFileForm";

class App extends Component {
  constructor(props) {
    super(props);
  }
  state = { status: null, data: null };

  handler = (status, data = null) => {
    this.setState({
      status: status,
      data: data,
    });
  };

  render() {
    if (this.state.status === null) {
      return (
        <div>
          <UploadFileForm handler={this.handler}> </UploadFileForm>{" "}
        </div>
      );
    }
    if (this.state.status === "waiting") {
      return <div>Waiting </div>;
    }
    return <div>{JSON.stringify(this.state.data)}</div>;
  }
}

export default App;
