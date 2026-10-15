# weather-etl
This project downloads the weather forecast for 3 Colombian cities (Medellin, La Ceja, Bogota) from the free Open-Meteo API and then answers questions with SQL queries.

## Questions it answers
+ Which city will get the most rain this week?
+ Which city will get the highest average temperature in the next week?
+ Which city will get the greatest temperature variation in this week?

## Architecture
``` mermaid
    flowchart LR
      api[Open-Meteo API] --> Extract --> Transform --> Load --> db[(SQL database)] --> Queries
```

+ **Extract:** get the forecast JSON for the 3 cities from Open-Meteo.
+ **Transform:** turn that JSON into a clean table with one row per city per day.
+ **Load**: save the table into a SQL database.
+ **Queries:** SQL that answers your questions

## Status
<span style="color:yellow">work in progress</span>
