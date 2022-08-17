from typing import Union, Optional

from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel

from datetime import datetime, timedelta, date
from urllib.request import urlopen
import json
import os

from lxml.html import parse
from pytrends.request import TrendReq


if "WEATHER_API_KEY" not in os.environ:
    raise ValueError("You need to set up an API KEY from weatherapi.com. Go to the documentation if you have any questions.")

WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]


app = FastAPI()


class LifeExpectancy(BaseModel):
    average_life_expectancy: float


class Unemployment(BaseModel):
    rate: float


class Trends(BaseModel):
    interest: list[int] = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/life_expectancy/{sex}/{race}/{year}", response_model=LifeExpectancy)
def get_life_expectancy(
        sex: str = Path(
            ...,
            title='Sex whose life expectancy you want to know.',
            description='Required. Only the values "female", "male" or '
                        '"both" are valid',
            regex=r'^male$|^female$|^both$'),
        race: str = Path(
            ...,
            title='Race whose life expectancy you want to know.',
            description='Required. Only the values "black", "white" or '
                        '"all" are valid',
            regex=r'^black$|^white$|^all$'),
        year: int = Path(
            ...,
            title='Year whose life expectancy you want to know',
            description='Required. Only a number between 1900 and 2017 '
                        'is valid',
            ge=1900,
            le=2017)):
    life_expectancy_request = urlopen(f'https://data.cdc.gov/resource/w9j2-ggv5.json?year={year}')
    life_expectancy_result = json.load(life_expectancy_request)

    race = 'All Races' if race == 'all' else race.capitalize()
    sex = 'Both Sexes' if sex == 'both' else sex.capitalize()
    result = next((item['average_life_expectancy'] for item in life_expectancy_result if
                   item["race"] == race and item["sex"] == sex), None)
    return {"average_life_expectancy": result}


@app.get("/unemployment/{state}", response_model=Unemployment)
def get_unemployment(state: str = Path(
    ...,
    title='State of the United States from which to obtain unemployment.',
    description='Required, lower-case and case insensitive. '
                'Only full state names are allowed. For names with more than one word you can use space (" ", "%20") or'
                ' underscore ("_"). For example: District of Columbia could be `district_of_columbia` or `district of '
                'columbia`. You can find a complete list of official names [here]('
                'https://www.bls.gov/web/laus/lauhsthl.htm) '
)):
    state = state.replace('_', ' ').title().replace(' Of ', ' of ')

    doc = parse(urlopen('https://www.bls.gov/web/laus/lauhsthl.htm')).getroot()
    list_of_states = [e.text_content() for e in doc.xpath('//p[@class="sub0"]')]

    if state not in list_of_states:
        raise HTTPException(status_code=400,
                            detail='Please, introduce a valid US State. You can find a complete list of official '
                                   'names here: https://www.bls.gov/web/laus/lauhsthl.htm ')

    parent_id = doc.xpath(f'//th[p[contains(text(),"{state}")]]/@id')
    unemployment = doc.xpath(f'//td[@headers="{parent_id[0]} lauhsthl.h.1.2"]')[0].text_content()

    return {'rate': unemployment}


@app.get("/trends", response_model=Trends)
async def get_trends(phrase: str = Query(
    ...,
    title='Phrase you want to know the trend in Google.',
    description='The data will be returned in days. If the date range is very large, weekly trends will be returned. '
),
        start_date: Union[date, None] = None,
        end_date: Union[date, None] = None):
    kw_list = [phrase]

    if start_date is not None and end_date is not None:
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        if start_date > end_date or start_date > datetime.today().strftime('%Y-%m-%d'):
            raise HTTPException(status_code=400,
                                detail='DATE ERROR: Please, introduce a valid date range. start_date must be before '
                                       'end_date. If you specify a start_date but not an end_date, trends from '
                                       'start_date to the current day will be displayed. If instead you specify an '
                                       'end_date and not a start_date, the data available up to the end_date will be '
                                       'displayed. Also, start_date must be before the current date.')
        if end_date < '2004-01-01':
            raise HTTPException(status_code=400,
                                detail='DATE ERROR: Data is available from 2004-01-01. Please check the date range.')
    elif start_date is None and end_date is not None:
        start_date = '2004-01-01'
    elif start_date is not None and end_date is None:
        end_date = datetime.today()
        end_date = end_date.strftime('%Y-%m-%d')
    else:
        start_date = datetime.today() - timedelta(days=13)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = datetime.today()
        end_date = end_date.strftime('%Y-%m-%d')

    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list, cat=0, timeframe=f'{start_date} {end_date}', geo='', gprop='')
    trends = pytrends.interest_over_time()

    pytrends.build_payload(kw_list, cat=0, timeframe=f'now 7-d', geo='', gprop='')
    last_seven_days_trends = pytrends.interest_over_time()
    last_seven_days_trends['days'] = [e.strftime('%Y-%m-%d') for e in last_seven_days_trends.index]
    daily_last_seven_days_trends = last_seven_days_trends.groupby(by=['days']).mean().iloc[1:, :]

    trend_index = trends.index

    for i, row in daily_last_seven_days_trends.iterrows():
        if i not in [e.strftime('%Y-%m-%d') for e in trend_index]:
            trends = trends.append(row)

    list_of_trends = trends.iloc[:, 0].values.tolist()

    return {'interest': list_of_trends}


@app.get("/weather")
async def get_weather(location: str = json.loads(urlopen("https://ip.seeip.org/jsonip?").read())["ip"]):
    # check if error
    weather_dict = {}

    date = datetime.today().strftime('%Y-%m-%d')

    while date > (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d'):
        doc = parse(urlopen(f'http://api.weatherapi.com/v1/history.xml?key={WEATHERAPI_KEY}&q={location}&dt={date}')).getroot()
        weather_dict[date] = {
            'weather': doc.xpath('//forecastday/day/condition/text')[0].text_content(),
            'maxtemp_c': doc.xpath('//forecastday/day/maxtemp_c')[0].text_content(),
            'maxtemp_f': doc.xpath('//forecastday/day/maxtemp_f')[0].text_content(),
            'mintemp_c': doc.xpath('//forecastday/day/mintemp_c')[0].text_content(),
            'mintemp_f': doc.xpath('//forecastday/day/mintemp_f')[0].text_content(),
            'avgtemp_c': doc.xpath('//forecastday/day/avgtemp_c')[0].text_content(),
            'avgtemp_f': doc.xpath('//forecastday/day/avgtemp_f')[0].text_content(),
            'maxwind_kph': doc.xpath('//forecastday/day/maxwind_kph')[0].text_content(),
            'maxwind_mph': doc.xpath('//forecastday/day/maxwind_mph')[0].text_content(),
            'totalprecip_mm': doc.xpath('//forecastday/day/totalprecip_mm')[0].text_content(),
            'totalprecip_in': doc.xpath('//forecastday/day/totalprecip_in')[0].text_content(),
            'avgvis_km': doc.xpath('//forecastday/day/avgvis_km')[0].text_content(),
            'avgvis_miles': doc.xpath('//forecastday/day/avgvis_miles')[0].text_content(),
            'avghumidity': doc.xpath('//forecastday/day/avghumidity')[0].text_content(),
            'sunrise': doc.xpath('//forecastday/astro/sunrise')[0].text_content(),
            'sunset': doc.xpath('//forecastday/astro/sunset')[0].text_content(),
            'moonrise': doc.xpath('//forecastday/astro/moonrise')[0].text_content(),
            'moonset': doc.xpath('//forecastday/astro/moonset')[0].text_content(),
            'moon_phase': doc.xpath('//forecastday/astro/moon_phase')[0].text_content(),
            'moon_illumination': doc.xpath('//forecastday/astro/moon_illumination')[0].text_content()
        }

        date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')

    return weather_dict


@app.get("/trends_weather")
async def get_trends_weather(phrase: str):
    trends_weather_list = []

    start_date = datetime.today() - timedelta(days=6)
    start_date = start_date.strftime('%Y-%m-%d')

    try:
        trends = await get_trends(phrase, start_date)
    except:
        trends = {}

    try:
        weather = await get_weather(phrase)
    except:
        weather = {}

    date = start_date
    date_count = 0

    while date <= datetime.today().strftime('%Y-%m-%d'):

        trends_weather_list.append({
            'date': date
        })

        if len(trends['interest']) > date_count:
            trends_weather_list[date_count]['interest'] = trends['interest'][date_count]
        if date in weather.keys():
            trends_weather_list[date_count]['weather'] = weather[date]

        date_count += 1
        date = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

    return trends_weather_list
