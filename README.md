# Azure Daily Report Function

End-to-end automated reporting system built with Azure Functions, designed to run on a scheduled basis to generate daily reports. It integrates data from a PostgreSQL database and CSV files stored in Azure Blob Storage, producing Excel reports that are automatically sent via email.

## Overview
This Azure Function is triggered automatically on a daily schedule using a Timer Trigger.

The workflow includes:
- Loading input CSV files from Azure Blob Storage  
- Creating temporary tables in PostgreSQL  
- Executing reporting queries  
- Generating an Excel report  
- Sending the report automatically via email  

## Architecture

The system follows a simple end-to-end pipeline:

1. CSV files are stored in Azure Blob Storage  
2. An Azure Function (Timer Trigger) runs daily  
3. Data is loaded into PostgreSQL using temporary tables  
4. Reporting queries are executed  
5. An Excel file is generated using pandas  
6. The report is sent automatically via email  

## Technologies

Azure Functions (Python)
Azure Blob Storage
Azure Database for PostgreSQL
pandas
psycopg2
xlsxwriter
smtplib (Gmail SMTP)

## Local Development

The function can be executed locally using Azure Functions Core Tools.
Environment variables are configured through `local.settings.json`.
