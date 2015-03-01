# StatTracker API

** Activities

* To see a list of all activities for your user:
  * curl -X GET -H "Authorization: Basic zackjcooper@gmail.com:password" http://localhost:5000/api/v1/activities

* To create an activity:
  * curl -X POST -H "Authorization: Basic zackjcooper@gmail.com:password" -H "Content-type: application/json" -d '{"name": "climb steps", "goal": "lose weight", "description": "climb 4 per day"}' http://localhost:5000/api/v1/activities/add

* To see a specific activity:
  * curl -X GET -H "Authorization: Basic zackjcooper@gmail.com:password" http://localhost:5000/api/v1/activities/<id>

* Update an activity
  * curl -X PUT -H "Authorization: Basic zackjcooper@gmail.com:password" -H "Content-type: application/json" -d '{"name": "Climb the steps", "goal": "lose weight", "description": "climb 4 per day"}' http://localhost:5000/api/v1/activities/update/<id>

* Delete an activity (also needs to be able to remove logs)
  * curl -X DELETE -H "Authorization: Basic zackjcooper@gmail.com:password" http://localhost:5000/api/v1/activities/delete/<id>





** Logs

* See a list of all logs for your user:
  * curl -X GET -H "Authorization: Basic zackjcooper@gmail.com:password" http://localhost:5000/api/v1/logs

* To see a specific log:
  * curl -X GET -H "Authorization: Basic zackjcooper@gmail.com:password" http://localhost:5000/api/v1/logs/<id>

* To create a log
  * curl -X POST -H "Authorization: Basic zackjcooper@gmail.com:password" -H "Content-type: application/json" -d '{"item_id":4, "value": "900", "logged_at": "2015/01/01"}' http://localhost:5000/api/v1/logs/add

* To update a log
  * curl -X PUT -H "Authorization: Basic zackjcooper@gmail.com:password" -H "Content-type: application/json" -d '{"value": "900", "logged_at": "2015/01/01"}' http://localhost:5000/api/v1/logs/update/<id>

* Delete a log
  * curl -X DELETE -H "Authorization: Basic zackjcooper@gmail.com:password" http://localhost:5000/api/v1/logs/delete/<id>
