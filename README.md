# fortristest

## Set up
**NOTE**: First of all, get a free API KEY from [weatherapi.com](https://weatherapi.com) and copy it to a file called `weather_api_key.txt` in the root directory. You can copy and rename the file `weather_api_key.txt.template` for it. The API will work without this key, but will raise an error at the `/weather` endpoint if it doesn't.

Clone repo:
```
git clone https://github.com/fonsiman/fortristest.git
```

On the repo folder, run the app:
```
docker compose up
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
    
    Output example: {‘interest’: \[NUMBERS\]}

- /unemployment/{STATE}
    
    Returns unemployment passing the name of a US state as a path parameter.
    - path: State of the United States from which to obtain unemployment. Required, lower-case and case insensitive. Only full state names are allowed. For names with more than one word you can use space (" ", "%20") or underscore ("_"). For example: District of Columbia could be district_of_columbia or district of columbia. You can find a complete list of official names [here](https://www.bls.gov/web/laus/lauhsthl.htm).
    
    > Example: [http://localhost/unemployment/district%20of%20columbia](http://localhost/unemployment/district%20of%20columbia)
    
    Output example: {"average_life_expectancy": NUMBER}
  
- /trends?phrase=\[phrase\]&start_date=\[date\]&end_date=\[date\]


- /weather

    Returns the weather history of the last 7 days according to the user's location through the IP. Does not require parameters.
    
    > Example: [http://localhost/weather](http://localhost/weather)

- /trends_weather?phrase=\[phrase\]


