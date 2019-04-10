import React from "react";
import axios from "axios";

class GoogleAuth extends React.Component {
  state = { activeUser: {}, isSignedIn: false };

  componentDidMount = async () => {
    const response = await axios.get("/check_user");
    if (response.data) {
      this.setState({ activeUser: response, isSignedIn: true });
    }
  };

  onSignInClick = async () => {
    const response = await axios.get("/login");
    // console.log(response);

    // this.setState({ activeUser: response, isSignedIn: true });

    // console.log(this.state.activeUser.data);
  };
  onSignOutClick = async () => {
    await axios.get("/logout");
    this.setState({ activeUser: {}, isSignedIn: false });
    // console.log(this.state.activeUser.data);
  };

  renderAuthButton() {
    if (this.state.isSignedIn === null) {
      return null;
    } else if (this.state.isSignedIn) {
      return (
        <button onClick={this.onSignOutClick} className="ui red google button">
          <i className="google icon" />
          Sign Out
        </button>
      );
    }
    return (
      <button onClick={this.onSignInClick} className="ui red google button">
        <i className="google icon" />
        Sign in with Google
      </button>
    );
  }

  render() {
    return <div>{this.renderAuthButton()}</div>;
  }
}

export default GoogleAuth;
