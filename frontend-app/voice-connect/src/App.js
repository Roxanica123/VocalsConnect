import React, { Component } from "react";
import UploadFileForm from "./upload-page/UploadFileForm";
import ResultsContainer from "./results-page/ResultsContainer";
import Card from "@material-ui/core/Card";
import Grid from "@material-ui/core/Grid";
import { withStyles } from "@material-ui/styles";

const useStyles = (theme) => ({
  root: {
    background: theme.palette.primary.baby,
    minWidth: "100%",
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
  },
  card: {
    minWidth: "60vw",
    maxWidth: "100vw",
    minHeight: "50vh",
    display: "flex",
    alignItems: "center",
    backgroundColor: theme.palette.primary.dark,
    boxShadow: "10px 10px 5px 0px rgba(0,0,0,0.25)",
  },
  resultsGrid: {
    display: "flex",
    flexWrap: "wrap",
  },
});

class App extends Component {
  constructor(props) {
    super(props);
  }
  state = { status: null, data: null };

  handler = (status, data = null, failed = false) => {
    this.setState({
      status: status,
      data: data,
      failed: failed,
    });
  };

  render() {
    const { classes } = this.props;
    if (this.state.status === null) {
      return (
        <Grid
          container
          className={classes.root}
          spacing={0}
          alignItems="center"
          justify="center"
        >
          <Card className={classes.card} variant="outlined">
            <UploadFileForm handler={this.handler}> </UploadFileForm>{" "}
          </Card>
        </Grid>
      );
    }
    if (this.state.status === "waiting") {
      return <div>Waiting </div>;
    }
    if (this.state.status === "done" && this.state.failed === true) {
      return <div>{this.state.data}</div>;
    }
    return <ResultsContainer data={this.state.data}></ResultsContainer>;
  }
}

export default withStyles(useStyles)(App);
