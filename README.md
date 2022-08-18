# fortristest

## Set up
**NOTE**: First of all, get a free API KEY from [weatherapi.com](https://weatherapi.com) and copy it to a file called `weather_api_key.txt` in the root directory. You can copy and rename the file `weather_api_key.txt.template` for it. The API will work without this key, but will raise an error at the `/weather` endpoint if it doesn't.

Clone repo:
```
git clone https://github.com/fonsiman/fortristest.git
```

On the repo folder, run the app:
```
docker compose up -d --build
```

## Testing the API

You can test the API in a web browser or on a platform like Postman through the URL `http://localhost/endpoint` or through the interactive documentation at [http://localhost/docs](http://localhost/docs).

## Endpoints

- /life_expectancy/{sex}/{race}/{year}
    
    Returns the average life expectancy based on the gender, race, and year passed as path parameters.
    - sex: Sex whose life expectancy you want to know. Required. Only the values "female", "male" or "both" are valid.
    - race: Race whose life expectancy you want to know. Required. Only the values "black", "white" or "all" are valid.
    - year: Year whose life expectancy you want to know. Required. Only a number between 1900 and 2017 is valid.
    
  > Example: [http://localhost/life_expectancy/male/black/2017](http://localhost/life_expectancy/male/black/2017)
    
    Output example: 
    ```json
    {"interest": [NUMBERS]}
    ```
  
- /unemployment/{STATE}
    
    Returns unemployment passing the name of a US state as a path parameter.
    - path: State of the United States from which to obtain unemployment. Required, lower-case and case insensitive. Only full state names are allowed. For names with more than one word you can use space (" ", "%20") or underscore ("_"). For example: District of Columbia could be district_of_columbia or district of columbia. You can find a complete list of official names [here](https://www.bls.gov/web/laus/lauhsthl.htm).
    
    > Example: [http://localhost/unemployment/district%20of%20columbia](http://localhost/unemployment/district%20of%20columbia)
    
    Output example: 
    ```json
    {"average_life_expectancy": NUMBER}
    ```
  
- /trends?phrase=\[phrase\]&start_date=\[date\]&end_date=\[date\]
  
  Retrieve historical interest for the phrase for the period <start_date,
  end_date> from Google Trends. If the dates are not specified get data for the last 2
  weeks.
  
  Query parameters:
  - phrase: Phrase that you want to know the trend in Google. Required. The data will be returned in days. If the date range is very large, weekly trends will be returned. 
  - start_date: Start date of the interest search. Optional. In ISO 8601 format: YYYY-MM-DD. Data available from 2004-01-01. If you specify a start_date but not an end_date, trends from start_date to the current day will be displayed.
  - end_date: End date of the interest search. Optional. In ISO 8601 format: YYYY-MM-DD. Data available from 2004-01-01. If you specify a end_date but not an start_date, the data available up to the end_date will be displayed.

  > Example: [http://localhost/trends?phrase=bitcoin%20price&start_date=2022-08-10&end_date=2022-08-15](http://localhost/trends?phrase=bitcoin%20price&start_date=2022-08-10&end_date=2022-08-15)
    
  Output example: 
  ```json
  {"interest":[89,100,84,76,82,59,55,52,50]}
  ```
  
- /weather

    Returns the weather history of the last 7 days according to the user's location through the IP. Does not require parameters.
    
    > Example: [http://localhost/weather](http://localhost/weather)
  
    Output example: 
    ```json
      {
        "2022-08-18": {
          "weather": "Sunny",
          "maxtemp_c": "31",
          "maxtemp_f": "87.8",
          "mintemp_c": "17.4",
          "mintemp_f": "63.3",
          "avgtemp_c": "24.9",
          "avgtemp_f": "76.9",
          "maxwind_kph": "24.8",
          "maxwind_mph": "15.4",
          "totalprecip_mm": "0",
          "totalprecip_in": "0",
          "avgvis_km": "10",
          "avgvis_miles": "6",
          "avghumidity": "38",
          "sunrise": "07:29 AM",
          "sunset": "09:08 PM",
          "moonrise": "12:13 AM",
          "moonset": "02:29 PM",
          "moon_phase": "Waning Gibbous",
          "moon_illumination": "60"
        },
        "2022-08-17": {
          [...]
        },
        [...]
      }
  ```

- /trends_weather?phrase=\[phrase\]
  
    Returns the phrase interest on Google and the weather history according to the user's location through the IP of the last 7 days.
    - phrase: Output example: Phrase that you want to know the trend in Google. Required. The data will be returned in days. If the date range is very large, weekly trends will be returned.
    
    > Example: [http://localhost/trends_weather?phrase=bitcoin%20price](http://localhost/trends_weather?phrase=bitcoin%20price)
  
    ```json
    [
      {
        "date": "2022-08-12",
        "interest": 100,
        "weather": {
          "weather": "Sunny",
          "maxtemp_c": "37.3",
          "maxtemp_f": "99.1",
          "mintemp_c": "25.8",
          "mintemp_f": "78.4",
          "avgtemp_c": "33.2",
          "avgtemp_f": "91.7",
          "maxwind_kph": "16.9",
          "maxwind_mph": "10.5",
          "totalprecip_mm": "0",
          "totalprecip_in": "0",
          "avgvis_km": "10",
          "avgvis_miles": "6",
          "avghumidity": "19",
          "sunrise": "07:23 AM",
          "sunset": "09:17 PM",
          "moonrise": "10:05 PM",
          "moonset": "07:27 AM",
          "moon_phase": "Waxing Gibbous",
          "moon_illumination": "100"
        }
      },
      {
        "date": "2022-08-13",
        [...]
      },
      [...]
    ]
    ```

