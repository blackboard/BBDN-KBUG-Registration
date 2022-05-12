# Kansas Blackboard Users Group Registration

This service is a heroku-hosted application that provides the registration form and Blackboard Learn REST integration to create users and enroll them in K-BUG virtual meeting courses. 

## Setup

As this is hosted in heroku, you will want to be sure to set up your remote git repositories correctly. The first step is to clone this repository locally with `git clone https://github.com/blackboard/BBDN-KBUG-Registration.git`. This will create a remote repo called origin, so when you want to check code back into the repository, you can use:

```
git add .
git commit -am "text about the changes you made"
git push origin
```

To deploy your changes to Heroku, you will use a similar procedure, but the first time, you will need to create a new remote deployment.

```
git remote set-url --add heroku https://git.heroku.com/kbug-registration.git
```

Once this is done, whenever you want to deploy the code you will:
```
git add .
git commit -am "text about the changes you made"
git push heroku
```

You will also need to [install the Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and have a Heroku account, and the admin for the Heroku App will need to [add you as a collaborator](https://devcenter.heroku.com/articles/collaborating#collaborator-permissions-for-apps-in-a-personal-account). 

## Configuring the project

To configure the project, you will need to copy ConfigTemplate.py to Config.py and add the following information:

key | value | notes
--- | --- | ---
"verify_certs" | "True" | Whether to verify SSL certs. Should always be True
"learn_rest_url" | "devcon.blackboard.com" | the domain hosting the Learn users
"learn_rest_key" | "YOURRESTKEY" | The REST key associated with the application in Learn
"learn_rest_secret" | "YOURRESTSECRET" | The REST secret associated with the application in Learn
"app_url" | "https://kbug-registration.herokuapp.com" | the url to the registration service in Heroku

## How to update

Updating for each conference is pretty simple. Very little of the code changes, you just need to change dates, add the appropriate course pk1, and update any text that you want to update.

In [registration.html](templates/registration.html) we store the landing page text. You will need to update the dates here and make any text changes you want. 

In [confirmation.html](templates/confirmation.html), we also store the date, so you will need to update this.

In [RestUserController.py](RestUserController.py) on line 23, there is a line like this:
```
self.courseId = "_866_1"
```

Update the pk1 value to match the new course.

Once these three files are update, you should deploy to Heroku and then push the changes back to the Github repository. See the section above for instructions.

## Notes and troubleshooting

This is a free Heroku service which means that a) the service goes to sleep after a period of non use. Then next person to register will experience a slight delay while the service wakes up again. In addition, the service resets itself once every 24 hours, so there is a breif period of unavailability each day.

A helpful tool in troubleshooting any issues is the heroku cli. From the command line in the directory that you have cloned this project, you can just type `heroku logs --tail` 


