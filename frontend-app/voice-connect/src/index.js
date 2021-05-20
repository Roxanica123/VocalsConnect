import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { createMuiTheme } from "@material-ui/core/styles";
import { ThemeProvider } from "@material-ui/styles";
import pink from "@material-ui/core/colors/purple";
import teal from "@material-ui/core/colors/green";

const theme = createMuiTheme({
  palette: {
    primary: {
      main: "#136f63",
      dark: "#22145a",
      baby: "#28af36",
      mint: "#143d39",
      pink: "#149a7d"
    },
    secondary: {
      main: "#4dbf14",
    },
  },
});

ReactDOM.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
