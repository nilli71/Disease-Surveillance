# Project Title
The Disease Surveillance Application is a Flask-based web app that allows users to manage patients, diseases, cases, and immunizations. It integrates with a Databricks SQL database for efficient storage and querying, simulating a real-world disease tracking system.

## Features
- Add and manage patient, case, and immunization data.
- Dynamic dropdowns for fields such as gender, zipcodes, diseases, and vaccines.
- Mock data generation for testing.

## File Descriptions
- ds_app_final_clean.py: The main Flask application. Handles routing, database connections, and form submissions.
- ds_index_clean.html: The homepage of the app. Provides navigation to add new data or manage records.
- ds_add_all_clean.html: The form for adding patient, case, and immunization information. Includes dynamic dropdowns and calendar inputs.
- mock_data_gen: Code used to generate mock data for testing the application, integrated into the database.

##Tech Stack
- Backend: Flask
- Database: Databricks SQL
- Frontend: HTML
- Mock Data: Python Faker library

## How to Run
- 1. Install dependencies.
- 2. Run the app using `python ds_app_final_clean.py`.
- 3. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Known Limitations:

- Region Redundancy:
The Patients table includes both zipcode and region_id, creating unnecessary redundancy. In future versions, region_id can be removed, and region information can be derived dynamically from the Regions table using the zipcode.

- Mock Data:
The current mock data is basic and may need refinement to include realistic mappings between zipcodes and regions.


## Future Work

- Database Normalization: Simplify the Patients table by removing the region_id column.
- Machine Learning Integration: Add predictive models to forecast disease severity and analyze vaccine effectiveness.
- Data Visualizations: Create dashboards for trends in disease cases and immunization coverage.
- Cloud Deployment: Deploy the application to a cloud platform for broader access.

