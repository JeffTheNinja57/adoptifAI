# AdoptifAI

AdoptifAI is a web application designed to assist animal shelters in managing their animals and increasing adoption rates. The platform allows shelters to add animal profiles, generate engaging descriptions using the Gemini AI API, and reach a wider audience. Guests can browse animals available for adoption, while shelters have access to advanced management features.

---

## Table of Contents
1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
    - [Running with Docker Compose](#running-with-docker-compose)
5. [Usage](#usage)
    - [Accessing the Application](#accessing-the-application)
    - [Registering as a Shelter](#registering-as-a-shelter)
    - [Managing Animals](#managing-animals)
    - [Generating Descriptions](#generating-descriptions)
6. [License](#license)

---

## Features
- **Shelter Registration and Authentication**: Secure registration and login for animal shelters.
- **Animal Management**: Read, Add, Update, and Delete animal profiles.
- **Guest Access**: Visitors can browse animals available for adoption.
- **Description Generation**: Generate engaging animal descriptions using the Gemini AI API.
- **Translation for Animals**: Generate translations of the descriptions with a click of a button.
- **Bulk Upload**: Upload CSV files to add multiple animals at once.
- **Responsive Frontend**: User-friendly interface built with React.
- **API Documentation**: Interactive API docs available via Swagger UI.

---

## Technology Stack

**Backend**:
- Python 3.12
- FastAPI
- SQLModel (with Pydantic)
- SQLite (easy integration with FastAPI; can be replaced with PostgreSQL or MySQL)
- Uvicorn (ASGI server)
- JWT Authentication

**Frontend**:
- React
- Axios
- React Router DOM
- React Toastify (for notifications)

**AI Integration**:
- Gemini AI API (for description generation)
- Fine-tuned HuggingFace model

**Deployment**:
- Docker
- Docker Compose

---

## Prerequisites
- **Python**: Version 3.12
- **Node.js**: Version 18 or higher
- **npm**: Version 8 or higher
- **Docker** (optional, for containerization)
- **Docker Compose** (optional, for running both services together)
- **Gemini AI API Key**: Required for generating descriptions (you can sign up for an API key from the Gemini AI platform)
- **Sentencepiece**: Required for running the HuggingFace translation model

---

## Installation

You can run the application either by setting up the backend and frontend separately or by using Docker Compose to run both services together.

### Backend Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/adoptifai.git
   ```
2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```
4. **Create a .env File**:
   In the backend directory, create a file named `.env` with the following content:
   ```env
   DATABASE_URL=sqlite:///./data/animals.db
   GEMINI_API_KEY=your_gemini_api_key
   ENVIRONMENT=development
   ```
   Replace `your_gemini_api_key` with your actual Gemini API key.

5. **Run the Backend Server**:
    ```bash
    cd adoptifai/backend
   ```
   
   ```bash
   uvicorn app.main:app #for development continue the uvicorn run script with "--reload"
   ```
   The backend API will be available at [http://localhost:8000](http://localhost:8000).
   API documentation is accessible at [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend Setup
1. **Navigate to the Frontend Directory**:
   ```bash
   cd ../frontend
   ```
2. **Install Dependencies**:
   ```bash
   npm install
   ```
3. **Start the Frontend Development Server**:
   ```bash
   npm start
   ```
   The frontend application will be available at [http://localhost:3000](http://localhost:3000).

---

## Running with Docker Compose

Alternatively, you can run both the backend and frontend using Docker Compose.
THIS IS CURRENTLY NOT OPERATIONAL. IT WILL BE IMPLEMENTED IN THE FUTURE!

1. **Ensure Docker and Docker Compose are Installed**.

2. **Navigate to the Project Root**
   
3. **Create a .env File**:
   In the project root directory, create a `.env` file with the following content:
   ```env
   DATABASE_URL=sqlite:///data/animals.db
   GEMINI_API_KEY=your_gemini_api_key
   ENVIRONMENT=development
   ```
4. **Build and Start the Containers**:
   ```bash
   docker compose up --build
   ```
   The frontend will be available at [http://localhost:3000](http://localhost:3000).
   The backend API will be available at [http://localhost:8000](http://localhost:8000).

5. **Stopping the Containers**:
   To stop the containers, press `Ctrl+C`.

6. **To remove them:**
   ```bash
   docker-compose down
   ```

---

## Usage

### Accessing the Application
- **Frontend** (a.k.a. The Website): Open your browser and navigate to [http://localhost:3000](http://localhost:3000).
- **Backend API**: API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Registering as a Shelter
1. **Navigate to the Registration Page**:
   - Click on the "Register" link in the navigation bar.
2. **Fill in the Registration Form**:
   - **Shelter Name**: Enter the name of your shelter.
   - **Location**: Provide the shelter's location.
   - **Contact Email**: Enter a valid email address.
   - **Password**: Create a secure password.
   - **API Key**: Provide your Gemini AI API key.
3. **Submit the Form**:
   - Click on the "Register" button to create your account.

### Managing Animals
- **Add a New Animal**:
  1. **Login**: Ensure you're logged in as a shelter. If you just registered, you don't need to log in again.
  2. **Navigate to "Add Animal"**: Click on the "Add Animal" link.
  3. **Fill in the Animal Details**: Provide all required information.
  4. **Submit**: Click "Add Animal" to save the animal profile.

- **Update an Animal**:
  1. **Navigate to the Shelter Account Page**.
  2. **Click on the desired Animal**: Will take you to the Animal's Detail Page.
  3. **Click on "Update Animal"**.
  4. **Modify the Details**.
  5. **Submit**: Click "Update Animal" to save changes.

- **Delete an Animal**:
  1. **Navigate to the Shelter Account Page**.
  2. **Click on the desired Animal**: Will take you to the Animal's Detail Page.
  3. **Click on "Delete Animal"**.
  4. **Confirm Deletion**.

- **Upload Animals via CSV**:
  1. **Navigate to the Shelter Account Page**.
  2. **Click on the desired Animal**: Will take you to the Animal's Detail Page.
  3. **Navigate to "Upload CSV"**.
  4. **Select Your CSV File**: Ensure it follows the required format:
  ```bash
  animal_type,name,age,color,months_in_shelter,behavior,health,vaccinated,target_audience
  ```
  5. **Submit**: Click "Upload" to process the file.

### Generating Descriptions
- **Generate Description for a Single Animal**:
  1. **Navigate to the Shelter Account Page**.
  2. **Click on the desired Animal**.
  3. **Click on "Generate Description"**.
  4. **Wait for Confirmation**: The description will be generated and saved.

### Generating Translations
- **Generate Translation for a Single Animal**:
  1. **Navigate to the Shelter Account Page**.
  2. **Click on the desired Animal**.
  3. **Click on "Generate Translation"**.
  4. **Wait for Confirmation**: The translation will be generated and saved.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

Special thanks to all teammates and the professor.
