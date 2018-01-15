import React, { Component } from 'react';
// import logo from './logo.svg';
import { Dropdown, Header, Table, Rating, Form, Checkbox, Dimmer, Loader, Segment } from 'semantic-ui-react';
import * as API from './Services/API';
import logo from './logo4.png';
import './App.css';

class App extends Component {

  state = {
    userId: null,
    movieId: null,
    users: [],
    movies: [],
    value: null,
    similarity: 'euclidean',
    recommendations: null,
    loading: true,
    filtering: 'users'
  }

  componentDidMount() {
    API.getData('users')
      .then(data => {
        let users = [];
        data.forEach(user => {
          users.push({key: user, text: user, value: user});
        });
        this.setState({users, loading: false});
      })
      .catch(err => {
        console.log(err);
      });
  }

  selectUser = (e, data) => {
    const {similarity, filtering} = this.state;
    let userId = data.value;
    this.setState({loading: true});
    API.getData(`${filtering}/${userId}/recommendations/${similarity}`)
      .then(data => {
        this.setState({recommendations: data.recommendations, userId, loading: false});
      })
      .catch(err => {
        console.log(err);
      });
  }

  selectMovie = (e, data) => {
    const {similarity, filtering} = this.state;
    let movieId = data.value;
    this.setState({loading: true});
    API.getData(`${filtering}/${movieId}/recommendations/${similarity}`)
      .then(data => {
        this.setState({recommendations: data.recommendations, movieId, loading: false});
      })
      .catch(err => {
        console.log(err);
      });
  }

  selectSimilarity = (e, {value}) => {
    const {userId, movieId, filtering} = this.state;
    this.setState({similarity: value});
    if (userId) {
      this.setState({loading: true});
      API.getData(`${filtering}/${userId}/recommendations/${value}`)
        .then(data => {
          this.setState({recommendations: data.recommendations, loading: false});
        })
        .catch(err => {
          console.log(err);
        });
    } else if (movieId) {
      this.setState({loading: true});
      API.getData(`${filtering}/${movieId}/recommendations/${value}`)
        .then(data => {
          this.setState({recommendations: data.recommendations, loading: false});
        })
        .catch(err => {
          console.log(err);
        });
    }
  }

  selectFiltering = (e, {value}) => {
    this.setState({filtering: value});
    if (value === 'users') {
      API.getData('users')
        .then(data => {
          let users = [];
          data.forEach(user => {
            users.push({key: user, text: user, value: user});
          });
          this.setState({users, loading: false});
        })
        .catch(err => {
          console.log(err);
        });
    } else {
      API.getData('movies')
        .then(data => {
          let movies = [];
          for (const movie in data) {
            movies.push({key: movie, text: data[movie].title, value: movie});
          }
          this.setState({movies, loading: false});
        })
        .catch(err => {
          console.log(err);
        });
    }
  }

  render() {
    const {users, movies, recommendations, similarity, loading, filtering} = this.state;
    let rows = [];
    if (recommendations) {
      recommendations.forEach(rec => {
        rows.push(
          <Table.Row key={rec}>
            <Table.Cell>
              <Header as='h2'>{rec[1]}</Header>
            </Table.Cell>
            <Table.Cell>
              <Rating icon='star' defaultRating={rec[0]} maxRating={5} />
              {/* {`${Math.round(rec[0] / 5 * 100)}%`} */}
              {`(${parseFloat(rec[0]).toFixed(2)})`}
            </Table.Cell>
          </Table.Row>
        )
      });
    }
    return (
      <div className="App">
        <header className="App-header">
          <div className="App-title-container">
            <img src={logo} className="App-logo" alt="logo" />
            <h1 className="App-title">MovieMachine</h1>
          </div>
          <div className="App-menu">
            {filtering === 'users' && <Dropdown onChange={this.selectUser} placeholder='User ID' search selection options={users} />}
            {filtering === 'movies' && <Dropdown onChange={this.selectMovie} placeholder='Movie ID' search selection options={movies} />}
            <div className="similarity-selector">
              <Form>
                <Form.Field>
                  <Checkbox
                    radio
                    label='Euclidean Distance'
                    name='checkboxRadioGroup'
                    value='euclidean'
                    checked={similarity === 'euclidean'}
                    onChange={this.selectSimilarity}
                  />
                </Form.Field>
                <Form.Field>
                  <Checkbox
                    radio
                    label='Pearson Correlation'
                    name='checkboxRadioGroup'
                    value='pearson'
                    checked={similarity === 'pearson'}
                    onChange={this.selectSimilarity}
                  />
                </Form.Field>
              </Form>
            </div>
            <div className="similarity-selector">
              <Form>
                <Form.Field>
                  <Checkbox
                    radio
                    label='User Based'
                    name='checkboxRadioGroup'
                    value='users'
                    checked={filtering === 'users'}
                    onChange={this.selectFiltering}
                  />
                </Form.Field>
                <Form.Field>
                  <Checkbox
                    radio
                    label='Item Based'
                    name='checkboxRadioGroup'
                    value='movies'
                    checked={filtering === 'movies'}
                    onChange={this.selectFiltering}
                  />
                </Form.Field>
              </Form>
            </div>
          </div>
        </header>
        <div>
          {loading && <Segment className="loader-background">
            <Dimmer active>
              <Loader size='massive'>Loading</Loader>
            </Dimmer>
          </Segment>}
          {!loading && recommendations && <Table celled padded>
            <Table.Header>
              <Table.Row>
                <Table.HeaderCell singleLine>Movie Title</Table.HeaderCell>
                <Table.HeaderCell>Recommendation</Table.HeaderCell>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {rows}
            </Table.Body>
          </Table>}
        </div>
      </div>
    );
  }
}

export default App;
