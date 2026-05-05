# Azure Daily Report Function

This project is an Azure Function App that runs on a daily schedule to generate
reports using data from a PostgreSQL database and CSV files stored in Azure Blob Storage.

## Overview

The function is triggered automatically every day using a Timer Trigger.
It performs the following steps:

- Loads input CSV files from Azure Blob Storage
- Creates temporary tables in PostgreSQL
- Executes reporting queries
- Generates an Excel report

## Technologies

- Azure Functions (Python)
- Azure Blob Storage
- Azure Database for PostgreSQL
- pandas
- psycopg2
- xlsxwriter

## Architecture

- Input data is stored externally as CSV files in Azure Blob Storage
- The function dynamically loads the data at runtime
- Temporary tables are used for report generation
- The solution is fully automated and serverless

## Local Development

The function can be executed locally using Azure Functions Core Tools.
Environment variables are configured through `local.settings.json`.