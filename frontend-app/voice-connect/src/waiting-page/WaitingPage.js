import React, { Component } from "react";

import Card from "@material-ui/core/Card";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/styles";
import Grid from "@material-ui/core/Grid";
import { Typography } from "@material-ui/core";
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
  loader: {
      position: "relative"
  }
});

class WaitingPage extends Component {
  state = {
    selectedFile: null,
    errors: null,
  };

  render() {
    const { classes } = this.props;
    return (
      <Grid container
            className={classes.root}
            spacing={0}
            alignItems="center"
            justify="center"
            style={{
            backgroundImage: `url(${process.env.PUBLIC_URL + "/spectrogram.png"})`,}}>
        <Card className={classes.card} variant="outlined">
            <BoxLoading className={classes.loader}/>
        </Card>
      </Grid>
    );
  }
}

WaitingPage.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(useStyles)(WaitingPage);
