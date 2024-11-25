from faker import Faker
import random
from datetime import datetime, timedelta
from databricks import sql

# Set up Faker and database connection
fake = Faker()
connection = sql.connect(
    server_hostname='adb-3035444690057649.9.azuredatabricks.net',
    http_path='/sql/1.0/warehouses/fc064804b30ebba1',
    access_token='dapi7b92a87c3b43646b04bcc79419aeb37d-2'
)

cursor = connection.cursor()

# Helper function to generate random dates
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# Generate mock data
def generate_mock_data():
    # 1. Insert Regions
    regions = []
    for _ in range(50):
        zipcode = fake.zipcode()
        region_name = fake.city()
        regions.append((zipcode, region_name))
    cursor.executemany("INSERT INTO disease_surveillance.Regions (zipcode, region_name) VALUES (?, ?)", regions)
    print(f"Inserted {len(regions)} regions.")

    # 2. Insert Diseases
    diseases = []
    for _ in range(20):
        disease_name = fake.word().capitalize()
        description = fake.sentence()
        diseases.append((disease_name, description))
    cursor.executemany("INSERT INTO disease_surveillance.Diseases (disease_name, description) VALUES (?, ?)", diseases)
    print(f"Inserted {len(diseases)} diseases.")

    # 3. Insert Vaccines
    vaccines = []
    for _ in range(10):
        vaccine_name = f"{fake.word().capitalize()} Vaccine"
        manufacturer = fake.company()
        description = fake.sentence()
        vaccines.append((vaccine_name, manufacturer, description))
    cursor.executemany(
        "INSERT INTO disease_surveillance.Vaccines (vaccine_name, manufacturer, description) VALUES (?, ?, ?)", vaccines
    )
    print(f"Inserted {len(vaccines)} vaccines.")

    # 4. Insert Patients
    patients = []
    for _ in range(1000):
        patient_name = fake.name()
        dob = fake.date_of_birth(minimum_age=0, maximum_age=90).strftime('%Y-%m-%d')
        gender = random.choice(["Male", "Female"])
        zipcode = random.choice(regions)[0]
        patients.append((patient_name, dob, gender, zipcode))
    cursor.executemany(
        "INSERT INTO disease_surveillance.Patients (patient_name, dob, gender, zipcode) VALUES (?, ?, ?, ?)", patients
    )
    print(f"Inserted {len(patients)} patients.")

    # 5. Insert Cases
    cases = []
    for _ in range(5000):
        patient_id = random.randint(1, 1000)  # Assuming patient_id starts at 1
        disease_id = random.randint(1, 20)
        diagnosis_date = random_date(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime('%Y-%m-%d')
        severity = random.choice(["Mild", "Moderate", "Severe"])
        notes = fake.text(max_nb_chars=50)
        cases.append((patient_id, disease_id, diagnosis_date, severity, notes))
    cursor.executemany(
        "INSERT INTO disease_surveillance.Cases (patient_id, disease_id, diagnosis_date, severity, notes) VALUES (?, ?, ?, ?, ?)", cases
    )
    print(f"Inserted {len(cases)} cases.")

    # 6. Insert Immunizations
    immunizations = []
    for _ in range(3000):
        patient_id = random.randint(1, 1000)
        vaccine_id = random.randint(1, 10)
        immunization_date = random_date(datetime(2020, 1, 1), datetime(2023, 12, 31)).strftime('%Y-%m-%d')
        administered_by = fake.name()
        immunizations.append((patient_id, vaccine_id, immunization_date, administered_by))
    cursor.executemany(
        "INSERT INTO disease_surveillance.Immunizations (patient_id, vaccine_id, immunization_date, administered_by) VALUES (?, ?, ?, ?)",
        immunizations
    )
    print(f"Inserted {len(immunizations)} immunizations.")

    connection.commit()

# Run mock data generation
generate_mock_data()

# Close the connection
cursor.close()
connection.close()
