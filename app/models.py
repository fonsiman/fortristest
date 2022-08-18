from pydantic import BaseModel, Field, validator

from typing import Optional

from datetime import datetime, timedelta, date
import re


class LifeExpectancy(BaseModel):
    average_life_expectancy: float


class Unemployment(BaseModel):
    rate: float


class TrendsInputs(BaseModel):
    phrase: str = Field(
        ...,
        title='List with the phrases that you want to know the trend in Google.',
        description='Required. The data will be returned in days. If the date range is very large, weekly trends will be '
                    'returned. '
    )
    start_date: Optional[date] = Field(
        default=None,
        title='Start date of the interest search.',
        description='Optional. In ISO 8601 format: YYYY-MM-DD. Data available from 2004-01-01. If you specify a '
                    'start_date but not an end_date, trends from start_date to the current day will be displayed. '
    )
    end_date: Optional[date] = Field(
        default=None,
        title='List with the end dates of the interest search.',
        description='Optional. In ISO 8601 format: YYYY-MM-DD. Data available from 2004-01-01. If you specify a '
                    'end_date but not an start_date, the data available up to the end_date will be displayed. '
    )


    @validator('start_date')
    def check_start_date_value(cls, v, values):
        if v is not None:
            v = v.strftime('%Y-%m-%d')
            if 'end_date' in values:
                end_date = values['end_date'].strftime('%Y-%m-%d')
                if v > end_date:
                    raise ValueError('Please, introduce a valid date range. start_date must be before end_date.'
                                     ' If you specify a start_date but not an end_date, trends from start_date '
                                     'to the current day will be displayed. If instead you specify an end_date and not a '
                                     'start_date, the data available up to the end_date will be displayed. Also, '
                                     'start_date must be before the current date.')
                if v > datetime.today().strftime('%Y-%m-%d'):
                    raise ValueError('start_date must be before of the current date.')

        elif 'end_date' in values:
            v = '2004-01-01'
        else:
            v = datetime.today() - timedelta(days=13)
            v = v.strftime('%Y-%m-%d')

        return v

    @validator('end_date')
    def check_end_date_value(cls, v):
        if v is not None:
            v = v.strftime('%Y-%m-%d')
            if v < '2004-01-01':
                raise ValueError('Data is available from 2004-01-01. Please check the end_date.')
        else:
            v = datetime.today()
            v = v.strftime('%Y-%m-%d')

        return v


class TrendsOutput(BaseModel):
    interest: list[int] = []
