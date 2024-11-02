
# AI Disease Diagnosis System

## Overview

The AI Disease Diagnosis System is an innovative Django-based web application designed to diagnose various diseases using artificial intelligence. By leveraging a patient's medical history and government ID, the system allows for efficient and accurate disease detection. It also generates comprehensive doctor reports to aid in the diagnosis and treatment process.

## Features

- **Disease Diagnosis**: Utilizes AI algorithms to analyze symptoms and diagnose diseases.
- **Patient History Management**: Securely stores and retrieves patient medical history using government ID for identification.
- **Doctor Reports**: Generates detailed reports based on the analysis for healthcare professionals.
- **User-Friendly Interface**: Intuitive design for easy navigation and operation.

## Technologies Used

- Django
- Python
- SQLite (or your preferred database)
- TensorFlow / PyTorch (for AI algorithms)
- HTML, CSS, JavaScript (for the front end)

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-disease-diagnosis.git
   cd ai-disease-diagnosis
   ```

2. **Set up a virtual environment**:
   It's recommended to create a virtual environment to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   Set up the database schema:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   Start the application with the following command:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

1. **Register a Patient**: Navigate to the registration page and enter the patient's information, including their government ID.
2. **Input Symptoms**: Provide symptoms for diagnosis through the patient dashboard.
3. **Receive Diagnosis**: The AI system analyzes the symptoms and provides potential diagnoses.
4. **Generate Doctor Report**: After diagnosis, generate a comprehensive report for the doctor.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.
