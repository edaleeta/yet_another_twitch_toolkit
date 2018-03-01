import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Col, ListGroup, ListGroupItem } from 'react-bootstrap';
import { TweetTemplateContainer } from './TweetTemplateContainer'

export class TweetTemplatesCurrent extends Component {
  constructor(props) {
    super(props);
    
    this.state = {
      templates: "",
      isUpdated: props.isUpdated
    }
  }

  componentWillMount() {
    fetch("/api/current-user-templates.json",
    {credentials: 'same-origin'})
    .then((response)=> response.json())
    .then((data) => {
      console.log("TweetTemplatesCurrent mounted!");
      this.setState({
        templates: data
      });
    })        
  }

  componentWillReceiveProps() {
    fetch("/api/current-user-templates.json",
    {credentials: 'same-origin'})
    .then((response)=> response.json())
    .then((data) => {
      console.log("TweetTemplatesCurrent is receiving props!");
      this.setState({
        templates: data
      });
    })        
  }

  shouldComponentUpdate(nextProps, nextState) {
    if (nextState.templates === this.state.templates) {
      return false;
    }
    return true;
  }

  render() {
    if (this.state.templates) {
      return (this.state.templates.map((template, key) => (
      <Col xs={12}>
        <ListGroup key={key}>
          <ListGroupItem key={key}>
            <TweetTemplateContainer template={template} key={key} onClick={this.props.onClick} />
          </ListGroupItem>
        </ListGroup>
      </Col>
      )));
    } else {
      return <div></div>
    }
  }
}

TweetTemplatesCurrent.propTypes = {
  onClick: PropTypes.func.isRequired,
  isUpdated: PropTypes.bool.isRequired,
}