from flask import Flask, render_template, request
from databricks import sql

app = Flask(__name__)

# Databricks connection
def get_db_connection():
    connection = sql.connect(
        server_hostname='adb-3035444690057649.9.azuredatabricks.net',
        http_path='/sql/1.0/warehouses/fc064804b30ebba1',
        access_token='dapi7b92a87c3b43646b04bcc79419aeb37d-2'
    )
    print("Database connection established.")
    return connection

@app.route('/')
def index():
    return render_template('ds_index_clean.html')

@app.route('/add_all', methods=['GET', 'POST'])
def add_all():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            # Required fields
            patient_name = request.form['patient_name']
            dob = request.form['dob']
            zipcode = request.form['zipcode']

            # Optional fields
            gender = request.form.get('gender', None)
            disease_id = request.form.get('disease_id', None)
            diagnosis_date = request.form.get('diagnosis_date', None)
            severity = request.form.get('severity', None)
            notes = request.form.get('notes', None)
            vaccine_id = request.form.get('vaccine_id', None)
            immunization_date = request.form.get('immunization_date', None)
            administered_by = request.form.get('administered_by', None)

            # Map zipcode to region_id
            cursor.execute("""
                SELECT region_id FROM disease_surveillance.Regions WHERE zipcode = ?
            """, (zipcode,))
            region = cursor.fetchone()

            if not region:
                print(f"Invalid zipcode: {zipcode}")
                return "Invalid zipcode selected."

            region_id = region[0]
            print(f"Zipcode {zipcode} mapped to Region ID: {region_id}")

            # Check if patient already exists
            cursor.execute("""
                SELECT patient_id FROM disease_surveillance.Patients 
                WHERE patient_name = ? AND dob = ?
            """, (patient_name, dob))
            patient = cursor.fetchone()

            if patient:
                # Patient exists, get patient_id
                patient_id = patient[0]
            else:
                # Add new patient
                cursor.execute("""
                    INSERT INTO disease_surveillance.Patients (patient_name, dob, gender, zipcode, region_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (patient_name, dob, gender, zipcode, region_id))
                conn.commit()

                # Fetch the new patient_id
                cursor.execute("""
                    SELECT patient_id FROM disease_surveillance.Patients
                    WHERE patient_name = ? AND dob = ?
                """, (patient_name, dob))
                patient_id = cursor.fetchone()[0]

            # Add new case information if provided
            if disease_id and diagnosis_date:
                cursor.execute("""
                    INSERT INTO disease_surveillance.Cases (patient_id, disease_id, diagnosis_date, severity, notes)
                    VALUES (?, ?, ?, ?, ?)
                """, (patient_id, disease_id, diagnosis_date, severity, notes))

            # Add new immunization information if provided
            if vaccine_id and immunization_date:
                cursor.execute("""
                    INSERT INTO disease_surveillance.Immunizations (patient_id, vaccine_id, immunization_date, administered_by)
                    VALUES (?, ?, ?, ?)
                """, (patient_id, vaccine_id, immunization_date, administered_by))

            conn.commit()
            return "Successfully Submitted!"

        except Exception as e:
            print(f"Error: {e}")
            return f"An error occurred: {e}"
        finally:
            conn.close()

    # Fetch dropdown options for zipcodes, diseases, and vaccines
    cursor.execute("SELECT zipcode FROM disease_surveillance.Regions")
    zipcodes = cursor.fetchall()
    cursor.execute("SELECT disease_id, disease_name FROM disease_surveillance.Diseases")
    diseases = cursor.fetchall()
    cursor.execute("SELECT vaccine_id, vaccine_name FROM disease_surveillance.Vaccines")
    vaccines = cursor.fetchall()
    conn.close()
    return render_template('ds_add_all_clean.html', zipcodes=zipcodes, diseases=diseases, vaccines=vaccines)

if __name__ == "__main__":
    app.run(debug=True)
