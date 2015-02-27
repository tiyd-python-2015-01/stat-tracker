# Stat Tracker

## Description

Build an application people can use to track any stats they want about themselves.

## Objectives

### Learning Objectives

After completing this assignment, you should understand:

* How to build Flask applications and APIs

### Performance Objectives

After completing this assignment, you should be able to:

* Design a simple database
* Create a Flask application

## Details

### Deliverables

* A Git repo called stat-tracker containing at least:
  * `README.md` file explaining how to run your project
  * a `requirements.txt` file
  * a way to seed your application with data
* An instance of your app running on Heroku

### Requirements  

* No PEP8 or Pyflakes warnings or errors
* Meets API specifications

## Normal Mode

You are going to build an application to track personal statistics. A personal statistic is a numerical record for a person in a time series by day. For example, let's say I wanted to track how many flights of stairs I walked up in a day. My last week might look like:

Date       | Flights
---------- | -------
02/19/2015 | 8 
02/20/2015 | 6 
02/21/2015 | 7 
02/22/2015 | 6
02/23/2015 | 8
02/24/2015 | 4
02/25/2015 | 6

Users of your application can create as many different activities to track as they want. They should have an easy-to-use interface to track their activities, allowing them to enter the number for the current day or any previous day.

You should allow for:

* User registration
* User login
* Creating a new activity to track
* Recording a stat for an activity for a day
* Editing a stat
* Showing a chart for an activity for any series of dates, defined by a start and stop date. The default should be the last 30 days.

For the chart, you can use whatever you like. Matplotlib is our old friend, but can be unwieldy. [Bokeh](http://bokeh.pydata.org/en/latest/) and [Plotly](https://plot.ly/python/) are other good choices to use with HTML.

You should also have an API. One of the ways people expect to use this application is via their phone, so you'll need a REST API.

### API Specification

For your API, I'm specifying the endpoints you'll need and what they should do. The URLs I'm using are not prefixed: yours should be with '/api/' and a version.

All the endpoints require authentication using HTTP Basic Auth.

Verb   | URL  | Action
------ | ---- | -------
GET | /activities | Show a list of all activities I am tracking, and links to their individual pages
POST | /activities | Create a new activity for me to track.
GET | /activities/{id} | Show information about one activity I am tracking, and give me the data I have recorded for that activity.
PUT | /activities/{id} | Update one activity I am tracking, changing attributes such as name or type. Does not allow for changing tracked data.
DELETE | /activities/{id} | Delete one activity I am tracking. This should remove tracked data for that activity as well.
POST or PUT | /activities/{id}/stats | Add tracked data for a day. The JSON sent with this should include the day tracked. You can also override the data for a day already recorded.
DELETE | /activities/{id}/stats | Remove tracked data for a day. You should send JSON that includes the date to be removed.

I am not specifying what the JSON these return should look like, but you should feel free to follow one of the many competing standards. [JSON API](http://jsonapi.org/) is very comprehensive.


## Hard Mode

In addition to the requirements from **Normal Mode**:

* Users should be able to record different types of stats. You can choose the types, but here are some suggestions:
  * Clicker-style stats. The UI on these should change so you have a way to increase them by one via a button click. Good for tracking things as you're doing them.
  * Time-goal stats. The stat has a beginning value, ending value, and ending date. Track as normal, but you should be able to see if you're on track to meet your goal. Examples: weight loss, building up for a long run.
  * Yes-no stats. Did I do this today? This is often called the "Seinfeld calendar" or [chain calendar](http://chaincalendar.com/about).
  * Stats on a scale instead of unbounded. Example: On a scale of 1 to 5, what's my happiness level today?

* Make sure your interface [is responsive](https://developers.google.com/web/fundamentals/layouts/rwd-fundamentals/) and works well via mobile.


## Nightmare Mode

* Give users a way to invite other users to collaborate/compete on a activity with them. Users can only add/edit their own data, but the activity charts will show everyone competing.


## Additional Resources

* [JSON API](http://jsonapi.org/)
* [Bokeh](http://bokeh.pydata.org/en/latest/) 
* [Plotly](https://plot.ly/python/)
* [Flask-RESTful](https://flask-restful.readthedocs.org/en/0.3.1/). A Flask plugin that could help or make this much worse.
* [RESTless](http://restless.readthedocs.org/en/latest/). Another Python library that could help or harm.
* [Kube](http://imperavi.com/kube/). A simpler CSS framework I've been using.
* [Peewee](https://peewee.readthedocs.org/en/latest/index.html). A less-featureful, but perhaps easier to use ORM.
