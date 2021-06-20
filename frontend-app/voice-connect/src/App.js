import React, { Component } from "react";
import UploadFileForm from "./upload-page/UploadFileForm";
import ResultsContainer from "./results-page/ResultsContainer";
import WaitingPage from "./waiting-page/WaitingPage";
import Card from "@material-ui/core/Card";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { withStyles } from "@material-ui/styles";
import { BoxLoading } from 'react-loadingg';

const useStyles = (theme) => ({
  root: {
    background: theme.palette.primary.baby,
    minWidth: "100%",
    minHeight: "100vh",
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    flexDirection: "column",
    alignItems: "center",
  },
  card: {
    margin: "0px 30px",
    minWidth: "40vw",
    minHeight: "60vh",
    display: "flex",
    alignItems: "center",
    alignSelf: "center",
    backgroundColor: theme.palette.primary.dark,
    boxShadow: "10px 10px 5px 0px rgba(77,191,20,0.29)",
    gridColumn: "1",
  },
  resultsGrid: {
    display: "flex",
    flexWrap: "wrap",
  },
  description: {
    gridColumn: "2",
    minHeight: "90vh",
    maxWidth: "100%",
    padding: "0px 30px 0px 0px"
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
          style={{
            backgroundImage: `url(${process.env.PUBLIC_URL + "/spectrogram.png"})`,
          }}
        >
          <Card className={classes.card} variant="outlined">
            <UploadFileForm handler={this.handler}> </UploadFileForm>{" "}
          </Card>
          <Grid
            container
            className={classes.description}
          >
            <Typography></Typography>
          </Grid>
        </Grid>
      );
    }
    if (this.state.status === "waiting") {
      return <WaitingPage></WaitingPage>;
    }
    if (this.state.status === "done" && this.state.failed === true) {
      return <div>{this.state.data}</div>;
    }
    return <ResultsContainer handler={this.handler} data={this.state.data}></ResultsContainer>;
  }
}

export default withStyles(useStyles)(App);
