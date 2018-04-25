# Implementing REST API with Python - Flask

## What is API
API stands for Application Programming Interface. It is a way to share information
on application data over the internet. There are various kind of API but normally
people are referencing to HTTP API when talking about APIs. In terms of HTTP API,
user will be giving input in a pre-defined format and the website will response
by sending information data in a certain format as well.

## What is REST
REST stands for Representational State Transfer. It is a standard methodology
to create HTTP APIs. For simplicity purpose, REST can be understood as api that
uses RESTful urls (_get_, _post_, _put_, _delete_).

## Requirement:
* `Python 3.6.5`
* `Flask 0.12.2`
* `Flask-RESTful 0.3.6`

## Notes
this is simple code inspired from https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3
This code creates an API of database of people's profile.