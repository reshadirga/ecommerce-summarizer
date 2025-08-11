// import React from "react";


// export default function DownloadTable(){
//     // Your Parse initialization configuration goes here
//     const PARSE_APPLICATION_ID = 'RuZmICQMeGu5bWLko09YyzJNQ481ILUatFrNC2HI';
//     const PARSE_HOST_URL = 'https://parseapi.back4app.com/';
//     const PARSE_JAVASCRIPT_KEY = 'C1PFzXvctEIjXA33a1rYy68fxdfh3bBlXzLBNEaC';
//     Parse.initialize(PARSE_APPLICATION_ID, PARSE_JAVASCRIPT_KEY);
//     Parse.serverURL = PARSE_HOST_URL;

//     // Save user input
//     async function addQuery(userContext) {
//         try {
//             // create a new Parse Object instance
//             const QueryGet = new Parse.Query('ScrapResMin');
//             QueryGet.contains('queryId', 'A5PrVBIGKF');
//             const queryResults = await QueryGet.find();

//             // const QueryId = await ;
//             return queryResults;
        
//         } catch (error) {
//             console.log('Error saving new query: ', error);
//         }
//     }

//     return(
//         <>
//         </>
//     )

// }