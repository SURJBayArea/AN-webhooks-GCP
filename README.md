# AN-webhooks-GCP
Serverless endpoint for Action Network webhooks, deployed on Google Cloud Platform.

When a new SURJ Bay Area member fills out the Intro Meeting Commitment form and expresses interest in joining one or more committees,
this endpoint sends an email to the committee(s) to notify them about the new member.

## Getting started

Install [Serverless](https://www.serverless.com/framework/docs/providers/google/guide/installation/):
```
$ npm install -g serverless
```
Install python dependencies:
```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Deploying

(requires [GCP credentials](https://www.serverless.com/framework/docs/providers/google/guide/credentials/))
```
$ serverless deploy
```
