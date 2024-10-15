# Global Weather Application

## Overview

The Global Weather Application is a web-based tool built using Python Flask that provides real-time weather information for cities around the world. This application allows users to search for weather conditions in various locations, offering a user-friendly interface to access up-to-date meteorological data.

## Features

- **City Weather Search**: Users can search for weather information by city name.
- **Real-time Data**: Fetches current weather data from a reliable weather API.
- **Temperature Display**: Shows temperature in both Celsius and Fahrenheit.
- **Weather Conditions**: Provides information on current weather conditions (e.g., sunny, cloudy, rainy).
- **Additional Metrics**: Displays humidity, wind speed, and atmospheric pressure.
- **Responsive Design**: Optimized for various screen sizes and devices.

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **API**: OpenWeatherMap API for weather data
- **Deployment**: Heroku (or your preferred hosting platform)

## Prerequisites

Before you begin, ensure you have the following installed:
- Python (3.7 or later)
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Hashara13/Global-Weather-App.git
   ```

2. Navigate to the project directory:
   ```
   cd Global-Weather-App
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\\Scripts\\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the root directory and add your OpenWeatherMap API key:
   ```
   API_KEY=your_openweathermap_api_key
   ```

## Running the Application

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000` to access the application.

## Deployment

To deploy this application to a production environment:

1. Choose a hosting platform (e.g., Heroku, PythonAnywhere).
2. Follow the platform's instructions for deploying a Flask application.
3. Ensure you set the environment variables, including your API key, in the production environment.

## Contact

Hashara Nethmin - [GitHub](https://github.com/Hashara13)

Project Link: [https://github.com/Hashara13/Global-Weather-App](https://github.com/Hashara13/Global-Weather-App)
