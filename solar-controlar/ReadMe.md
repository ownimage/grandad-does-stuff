# Introduction

I have solar panels and a GivEnergyInverter and battery.  

My tariff means that it is better to charge my battery during the day with excess PV energy (which I could sell at about 9p/unit)
rather than overnight (where it costs me 15p/unit).

But I also want my battery to be 100% full at the start of the peak discharge price time where it can cost me 36p per unit to use
and I can sell for 26p.

So this project aims to get a solar forcast for the next day, and charge the battery overnight to the right level based on my typical usage.

## Prerequisites

You need to have a solar panels, a GivEnergy inverter and battery and a https://givenergy.cloud/ login.

We are going to get our solar prediction from https://solcast.com/
You need to create a login and define your solar installation there to get a forcast.
API documentation https://docs.solcast.com.au/

# Create the docker image
```sh
docker build -t solar-controlar:latest .
```

# Running the Container

## First time configuration
```shell
copy docker-compose-template.yml docker-compose.yml
```
**Edit the values of docker-compose.yml to reflect your environment.**  
DO NOT CHECK THIS INTO SOURCE CONTROL - unless you know what you are doing.

## Start the container and exec into it
```shell
docker compose up -d
```

```shell
docker exec -it -w /app solar-controlar bash
```
Note this is cmd not PowerShell


## Getting a Forcast
Currently 2 stage process:

### 1 get the forecast to a json file
```shell
python forecast_fetch.py > forecast.json
```
### 2 process the json file
```shell
python forecast.py
```






## MVP


## Other junk

We are going to get our solar prediction from toolkit.solcast.com.au
API documentation https://docs.solcast.com.au/


set SOLCAST_API_KEY=<your-api-key>
set SOLCAST_SITE_ID=<your-site-id>
```shell
docker run -it --rm -e SOLCAST_API_KEY=%SOLCAST_API_KEY% -e SOLCAST_SITE_ID=%SOLCAST_SITE_ID% -v "%cd%":/app -w /app solar-controlar:latest bash
```

```
python main.py
```

What I need is a way to get forecasts and historic data.  I will compare the historic data with the GivEnergy
historic actuals to adjust the forcast to get a better result.

```shell
curl -X GET "https://api.givenergy.cloud/v1/inverter/FD2325G412/data?start=2024-01-01T00:00:00Z&end=2024-01-31T23:59:59Z" \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTc3MDIxOS1jYWE2LTRmOTctOTE3Ni0zNDBlZGMzZDQxNTgiLCJqdGkiOiI4ZGRjYjQxNzEwYzViOTY5YzdhOTI2M2E4M2IzNTU2M2I4ZDU3YmVlOTRiOTU0ZjQ4ZDM0YTYzOTdhY2FiMGFiNjMyYTM0ZDk2MzcxYjAxNiIsImlhdCI6MTc0NTY4MjkyMy4zOTcsIm5iZiI6MTc0NTY4MjkyMy4zOTcwMDQsImV4cCI6MTc0NjI4NzcyMy4zODY2ODEsInN1YiI6Ijc1MTE4Iiwic2NvcGVzIjpbImFwaSJdfQ.hCQ9cKQwIFv2IUvJdmEA0o1XQc908zxRkXYg76q0dBfAaWDBDr4lg0PDcj_YCt2YpTYJHRy2NpqSKiXvT-sRx7tTw06YhXsbfvercQODwMzj9s4LqvWvGQIvGYatx3DDpz_hXJH7jqdApLlb5k9z0BwYD8YnoTUxiXWtc9_6h9sB3V7L-2f6VHV6tSmBdcayiV41AFxqKpBWRXqhb-6ucjBIgFIBhKj0vkbE-EYKp083oSPNr8YbN4XuFZ2rL-8PQgEzijrsY5ngAFYSPkGMgWe_fAw9qB32ZJBUNBi0kQmijSCSUaHWNnCKWAFlLLtU7Gpg-9TqW_Sw9_9irOO7-hGCX1-Y2CvFIFQhVVqzm5SztVp2bJAExI_nXbNI0rxhwUefSiQtdUmwPIfkcExZ8NWkt0zpdC_m1d7OlJ4gVCwE2CN8BTAE_pbewVEIB0TiUfdVS1IJqTLs_FME3klp2BiwiE4angTR1B3p5Gs91yKcRl5dOnKRTJmmkPOPOKUqKe8jppu4-L8tgngyeWPyDmtw-dJ_IcbrmyAePXd_K5ZpO0uliSDbf1N_zjlXp15Tbv7i8z9DucmhlqDL-bFp8s5rtSOIir3K09ZbpYfSHNCz9VSkxYV66MfX4ThsLxalNwCxUg_FCNBCw6fZs8yl8VlQlzp9O9WXaYhAoPiZxmc" \
     -H "Accept: application/json"
```

