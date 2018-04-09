# Stock Portfolio using Pyramid Framework

**Author**: Beverly

**Version**: 0.1.0

## Overview
Stock Portfolio App created with Pyramid for CF Python 401 course

## Getting Started
<!-- What are the steps that a user must take in order to build this app on their own machine and get it running? -->
- Clone this repository to your local machine.
- Go into the repository directory.
- Start your virtual environment.
- Install the dependencies using the command `pip install -e .[testing]`
- Start the server using the command `pserve development.ini --reload`
- Point your browser to [http://localhost:6543](http://localhost:6543) to view the application

## Architecture
<!-- Provide a detailed description of the application design. What technologies (languages, libraries, etc) you're using, and any other relevant design information. This is also an area which you can include any visuals; flow charts, example usage gifs, screen captures, etc.-->
Written in Python using the Pyramid framework, specifically built with the the cookiecutter SQLAlchemy scaffold. Deployed with Heroku. Tested using Pytest.

## API
<!-- Provide detailed instructions for your applications usage. This should include any methods or endpoints available to the user/client/developer. Each section should be formatted to provide clear syntax for usage, example calls including input data requirements and options, and example responses or return values. -->
| Route | Name | Description |
|:--|--|:--|
| `/` | home | the home page |
| `/auth` | login | sign-up/sign-in to the app|
| `/portfolio` | portfolio | shows all stocks in your portfolio |
| `/detail/{ticker}` | detail | detailed view of a specific stock |
| `/stock` | add | search for and add a stock to your portfolio |

## Change Log
<!-- Use this are to document the iterative changes made to your application as each feature is successfully implemented. Use time stamps. Here's an example:

01-01-2001 4:59pm - Added functionality to add and delete some things.
-->
| Date | |
|:--|:--|
| 4-8-2018 2000 | Search/add stock view added, queries IEX Trading API |
| 4-7-2018 1600 | Static pages using Jinja2 templates working and detail view working. All views tested. |
