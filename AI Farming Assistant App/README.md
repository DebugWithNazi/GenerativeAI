# AI Climate & Smart Farming Assistant

A Streamlit application that provides AI-powered insights for climate monitoring and smart farming practices.

## Features

- Real-time weather data and forecasts
- Air quality monitoring
- Smart farming data analysis
- AI-powered climate insights
- PDF report generation

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   AIRVISUAL_API_KEY=your_airvisual_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Environment Variables

The following environment variables need to be set in your `.env` file:

- `GROQ_API_KEY`: Your Groq API key for AI model access
- `AIRVISUAL_API_KEY`: Your AirVisual API key for air quality data

## Deployment on Hugging Face
https://huggingface.co/spaces/Naz786/AI-Climate-and-Farming-Assistance-App

