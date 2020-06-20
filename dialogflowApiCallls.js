// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
const axios = require('axios');
const functions = require('firebase-functions');
const { WebhookClient } = require('dialogflow-fulfillment');
const { Card, Suggestion } = require('dialogflow-fulfillment');

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));

  function welcome(agent) {
    agent.add(`Welcome to my agent!`);
  }

  function fallback(agent) {
    agent.add(`I didn't understand`);
    agent.add(`I'm sorry, can you try again?`);
  }

  function bestmovies(agent) {
    if (isNaN(agent.parameters.numOfMovies)) {
      return agent.add("how many best movies would you like to know?");
    }
    const numOfMovies = agent.parameters.numOfMovies;
    return axios.get(`https://mrshollywoodlivechat.herokuapp.com/bestMovie?numOfMovies=${numOfMovies}`)
      .then((result) => {
        let mvList = [];
        result.data.map((movieList, index) => {
          mvList.push((index + 1) + ". " + movieList.title + " released in the year " + movieList.year + "\n");
        });
        //console.log(mvList);
        let header = `Here are the top ${numOfMovies} best movies since 2013 till 2018.`;
        let response = mvList.toString().replace(/\,/g, "");
        agent.add(header + "\n" + response);
      });
  }

  function bestMovieWithYear(agent) {
    const numOfMovies = agent.parameters.numOfMovies;
    const year = agent.parameters.year;
    if (isNaN(agent.parameters.numOfMovies)) {
      return agent.add("how many best movies would you like to know?");
    }
    if (isNaN(agent.parameters.year)) {
      return agent.add("please provid an year");
    }
    return axios.get(`https://mrshollywoodlivechat.herokuapp.com/bestMovieWithYear?year=${year}&numOfMovies=${numOfMovies}`)
      .then((result) => {
        let mvList = [];
        result.data.map((movieList, index) => {
          mvList.push((index + 1) + ". " + movieList.title + "\n");
        });
        let header = `Here are the top ${numOfMovies} best movies in ${year}.`;
        let response = mvList.toString().replace(/\,/g, "");
        agent.add(header + "\n" + response);
      });
  }

  function bestMovieWithGenres(agent) {
    const numOfMovies = agent.parameters.numOfMovies;
    const genres = agent.parameters.genres.join(" and ");
    if (genres == "") {
      return agent.add("please provide the genres name");
    }
    if (numOfMovies == "") {
      return agent.add("please provide the number Of movies would you like to know");
    }
    if (isNaN(numOfMovies)) {
      return agent.add("how many best movies would you like to know?");
    }
    return axios.get(`https://mrshollywoodlivechat.herokuapp.com:443/bestMovieWithGenres?genres=${genres}&numOfMovies=${numOfMovies}`)
      .then((result) => {
        let mvList = [];
        let response = "";
        result.data.map((movieList, index) => {
          mvList.push((index + 1) + ". " + movieList.title + " released in the year " + movieList.year + "\n");
        });
        if (mvList.length == 0) {
          response = "Sorry, No movies found. Please try again with another search criteria";
        } else {
          response = mvList.toString().replace(/\,/g, "");
        }
        let header = `Here are the top ${numOfMovies} best ${genres} movies since 2013 till 2018.`;
        agent.add(header + "\n" + response);
      });
  }

  function bestMovieWithGenresAndYear(agent) {
    const genres = agent.parameters.genres.join(" and ");
    const year = agent.parameters.year;
    const numOfMovies = agent.parameters.numOfMovies;
    if (genres == "") {
      return agent.add("please provide the genres name");
    }
    if (year == "") {
      return agent.add("please provide the year");
    }
    if (numOfMovies == "") {
      return agent.add("please provide the number Of movies would you like to know");
    }
    if (isNaN(agent.parameters.numOfMovies)) {
      return agent.add("how many best movies would you like to know?");
    }
    return axios.get(`https://mrshollywoodlivechat.herokuapp.com/bestMovieWithGenresAndYear?genres=${genres}&year=${year}&numOfMovies=${numOfMovies}`)
      .then((result) => {
        var mvList = [];
        let response = "";
        result.data.map((movieList, index) => {
          mvList.push((index + 1) + ". " + movieList.title + "\n");
        });
        if (mvList.length == 0) {
          response = "Sorry, No movies found. Please try again with another search criteria";
        } else {
          response = mvList.toString().replace(/\,/g, "");
        }
        let header = `Here are the top ${numOfMovies} best ${genres} movies in the year ${year}.`;
        agent.add(header + "\n" + result);
      });
  }
  function movieDetailsWithTitle(agent) {
    const title = agent.parameters.title;
    if (title == "") {
      return agent.add("please provide the movie name.");
    }
    return axios.get(`https://mrshollywoodlivechat.herokuapp.com/movieDetailsWithTitle?title=${title}`)
      .then((result) => {
        let mvList = [];
        let response = "";
        result.data.map((movieList, index) => {
          mvList.push((index + 1) + ". " + movieList.title +
               " released in the year: " + movieList.year + 
               " genres: " + movieList.genres + 
               " total ratings: " + movieList.total_rating + 
               " avg rating: " + movieList.year +
               " Home page: " + movieList.tmdLink + "\n");
        });
        if (mvList.length == 0) {
          response = `Sorry, No movies found for ${title}. Please try again with another search criteria`;
        } else {
          response = mvList.toString().replace(/\,/g, "");
        }
        let header = `Here are the movie details for ${title}.`;
        agent.add(header + "\n" + response);
      });
  }

  function similarMoviesWithTitle(agent) {
    const numOfMovies = agent.parameters.numOfMovies;
    const title = agent.parameters.title;
    if (title == "") {
      return agent.add("please provide the movie name.");
    }
    if (numOfMovies == "") {
      return agent.add("how many best movies would you like to know?");
    }
    if (isNaN(numOfMovies)) {
      return agent.add("how many best movies would you like to know?");
    }
    return axios.get(`https://mrshollywoodlivechat.herokuapp.com/similarMoviesWithTitle?title=${title}&numOfMovies=${numOfMovies}`)
      .then((result) => {
        let mvList = [];
        let response = "";
        let header = "";
        result.data.map((movieList, index) => {
          if (index == 0) {
            header = `Here are the ${numOfMovies} best similar movies for ${movieList.title}`;
          } else {
            mvList.push((index) + ". " + movieList.title + " released in the year " + movieList.year + "\n");
          }
        });
        if (mvList.length == 0) {
          response = `Sorry, No movies found for ${title}. Please try again with another search criteria`;
        } else {
          response = mvList.toString().replace(/\,/g, "");
        }
        agent.add(header + "\n" + response);
      });
  }
  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('bestmovies', bestmovies);
  intentMap.set('bestMovieWithYear', bestMovieWithYear);
  intentMap.set('bestMovieWithGenres', bestMovieWithGenres);
  intentMap.set('bestMovieWithGenresAndYear', bestMovieWithGenresAndYear);
  intentMap.set('movieDetailsWithTitle', movieDetailsWithTitle);
  intentMap.set('similarMoviesWithTitle', similarMoviesWithTitle);

  agent.handleRequest(intentMap);
});
