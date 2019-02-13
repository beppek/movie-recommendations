# Movie Recommendations

A recommendation system for users to get movie recommendations based on Euclidean distance or Pearson Correlation using either User Based Content Filtering or Item Based Content Filtering.

To run the application open a terminal and navigate to `/api`. Bring up the docker container using

```bash
docker-compose up --build
```

This will build the docker container if it is new and bring it up. This process may take a while if your connection is slow.

Next open a new terminal and navigate to `/client`. Install dependencies.

```bash
npm i
```

Then bring up the frontend with

```bash
npm start
```

A browser window should automatically open up and load the client.

That's it.
