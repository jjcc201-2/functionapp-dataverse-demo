# Functionapp-dataverse-demi

## Description

This repository showcases an Azure Function App, which interacts with Dataverse using the Dataverse API. This is based off an HTTP trigger, but can be adapted to use different triggers in order to be part of an event driven architecture (e.g. a timer-trigger based on a poll system, or through events that are pushed to the HTTP endpoint). 

The primary function of this app is to write data to a specified table in Dataverse. This allows for dynamic and real-time data updates, initiated by an HTTP request. 

## Usage

To use this function app, an HTTP request must be made to the app's endpoint. The request should contain the necessary data to be written to the Dataverse table. Upon receiving the request, the app will process the data and write it to the specified table using the Dataverse API. This demo will take in the firstname and lastname of a contact and will then write this row into the Dataverse table assuming both fields are present. 
