import React, { Component } from 'react';
import axios from 'axios';
import './App.css';

import { withStyles } from '@material-ui/core/styles';

import Button from '@material-ui/core/Button';
import FilledInput from '@material-ui/core/FilledInput';
import InputLabel from '@material-ui/core/InputLabel';
import InputAdornment from '@material-ui/core/InputAdornment';
import FormControl from '@material-ui/core/FormControl';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormLabel from '@material-ui/core/FormLabel';


const styles = theme => ({

  button: {
    padding: '8px',
    margin: '10px',
  },
  radios: {
    display: 'inline',
    textAlign: 'center',

  },
  radioGroup: {
    display: 'block',
    margin: '30px'
  }

});

class App extends Component {

  state = {
    amount: '',
    dollarCoins: 0,
    halfDollarCoins: 0,
    quarterCoins: 0,
    dimeCoins: 0,
    nickelCoins: 0,
    pennyCoins: 0,
    type: 'US',
    toonies: 0,
  }

  changeAmount = (event) => {
    this.setState({
      ...this.state,
      amount: event.target.value,
    })
  }

  handleCountryChange = (event) => {
    this.setState({
      ...this.state,
      dollarCoins: 0,
      halfDollarCoins: 0,
      quarterCoins: 0,
      dimeCoins: 0,
      nickelCoins: 0,
      pennyCoins: 0,
      toonies: 0,
      type: event.target.value
    })
  }

  sendData = () => {
    const config = {
      headers: { 'Content-Type': 'application/json' },
      withCredentials: true,
    };
    let thingToSendToServer = { amount: this.state.amount, type: this.state.type };
    console.log(thingToSendToServer);

    axios.put('/convert', thingToSendToServer, config)
      .then((response) => {
        console.log('this is response from server:', response.data);
        let coinBundle = response.data;
        this.setState({
          ...this.state,
          dollarCoins: coinBundle.dollarCoins,
          halfDollarCoins: coinBundle.halfDollarCoins,
          quarterCoins: coinBundle.quarterCoins,
          dimeCoins: coinBundle.dimeCoins,
          nickelCoins: coinBundle.nickelCoins,
          pennyCoins: coinBundle.pennyCoins,
          toonies: coinBundle.toonies,
        })

      }).catch((err) => {
        console.log(err);
      })
  }

  render() {

    const { classes } = this.props;

    return (
      <div className="App">

        <h1>GIVE ME YOUR $$, I GIVE YOU COINS</h1>
        <h3>Amount entered: ${this.state.amount}</h3>
        <FormControl className={classes.radioGroup}>
          <FormLabel component="legend">Currency</FormLabel>
          <RadioGroup className={classes.radios} aria-label="currency" name="currency" value={this.state.type} onChange={this.handleCountryChange}>
            <FormControlLabel value="US" control={<Radio />} label="US Dollars" />
            <FormControlLabel value="Canada" control={<Radio />} label="Canadian Dollars" />
          </RadioGroup>
        </FormControl>

        <FormControl >
          <InputLabel htmlFor="standard-adornment-amount">Amount</InputLabel>
          <FilledInput
            id="standard-adornment-amount"
            value={this.state.amount}
            onChange={this.changeAmount}
            startAdornment={<InputAdornment position="start">$</InputAdornment>}
          />
        </FormControl>
        <Button
          className={classes.button}
          variant="contained"
          color="primary"
          onClick={this.sendData}>
          Click me to count the change!
        </Button>
        {this.state.type === 'US' &&
          <div>
            <p>Silver Dollars: {this.state.dollarCoins}</p>
            <p>Half Dollars: {this.state.halfDollarCoins}</p>
            <p>Quarters: {this.state.quarterCoins}</p>
            <p>Dimes: {this.state.dimeCoins}</p>
            <p>Nickels: {this.state.nickelCoins}</p>
            <p>Pennies: {this.state.pennyCoins}</p>
          </div>}
        {this.state.type === 'Canada' &&
          <div>
            <p>Toonies: {this.state.toonies}</p>
            <p>Loonies: {this.state.dollarCoins}</p>
            <p>Half Dollars: {this.state.halfDollarCoins}</p>
            <p>Quarters: {this.state.quarterCoins}</p>
            <p>Dimes: {this.state.dimeCoins}</p>
            <p>Nickels: {this.state.nickelCoins}</p>
            <p>Pennies: {this.state.pennyCoins}</p>
          </div>
        }

        {/* {JSON.stringify(this.state)} */}

      </div>
    );
  }
}

export default (withStyles(styles)(App));
