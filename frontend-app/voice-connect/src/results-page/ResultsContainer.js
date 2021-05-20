import React, { Component } from "react";

import Card from "@material-ui/core/Card";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/styles";
import Grid from "@material-ui/core/Grid";
import { Typography } from "@material-ui/core";

const useStyles = (theme) => ({
  root: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flex: "1 0 21%",
    margin: "5px",
    minWidth: "300px",
    minHeight: "200px",
    backgroundColor: "transparent",
  },
  grid: {
    display: "flex",
    backgroundColor: theme.palette.primary.dark,
    direction: "column",
    alignItems: "center",
    justifyContent: "space-around",
    minHeight: "100vh",
    padding: "0px 10%",
  },
  resultsGrid: {
    display: "flex",
    flexWrap: "wrap",
    minHeight: "80vh",
  },
  text: {
    margin: "20px 0px",
    backgroundColor: theme.palette.secondary.main,
    color: "#fff5ee",
    boxShadow: "6px 6px 15px 0px rgba(255,245,238,0.43)",
    width: "100%",
    height: "20%",
    padding: "20px 0px",
    justifyContent: "center",
  },
  frame: {
    width: "100%",
    height: "100%",
    minHeight: "200px",
  },
});

class ResultsContainer extends Component {
  state = {
    selectedFile: null,
    errors: null,
  };

  render() {
    const { classes } = this.props;
    const genres = this.props.data.genre_predictions
      .toString()
      .replaceAll(",", ", ")
    const urls = this.props.data.similar_songs_ids;
    return (
      <Grid container className={classes.grid}>
        <Card container className={classes.text}>
          <Typography align="center" variant="h5">
            The predicted genres were: {genres}.<br />
            Here are the most similar songs in our dataset:
          </Typography>
        </Card>
        <Grid
          container
          spacing={0}
          alignItems="center"
          justify="center"
          direction="row"
          className={classes.resultsGrid}
        >
          {urls.map((url) => (
            <Card
              container
              className={classes.root}
              key={url.split("/")[5]}
              variant="elevation"
            >
              <iframe
                className={classes.frame}
                title={url.split("/")[5]}
                src={url}
                frameBorder="0"
                allowtransparency="true"
                allow="encrypted-media"
                align="center"
                justify="center"
              ></iframe>
            </Card>
          ))}
        </Grid>
      </Grid>
    );
  }
}

ResultsContainer.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(useStyles)(ResultsContainer);
