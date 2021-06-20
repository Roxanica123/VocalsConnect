import React, { Component } from "react";

import Card from "@material-ui/core/Card";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/styles";
import Grid from "@material-ui/core/Grid";
import { Typography } from "@material-ui/core";
import { SemipolarLoading } from 'react-loadingg';


const useStyles = (theme) => ({
  root: {
    backgroundColor: theme.palette.primary.dark,
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyItems: "center"
  },
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
            justify="center">
            <SemipolarLoading color="#4dbf14" size="large" style={{position: "relative", margin:"10px", minHeight:"100px"}}/>
            <Typography variant="h5" style={{color:"#4dbf14"}}> Hang on, we're working on it 😄</Typography>
      </Grid>
    );
  }
}

WaitingPage.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(useStyles)(WaitingPage);
