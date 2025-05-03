# Street-Fairy-Chatbot
Street-Fairy: Business Recommendations ChatBot with Personalized Itinerary Planning
Street Fairy is a business recommendation system that leverages the Yelp dataset to provide personalized suggestions to users. The project integrates Snowflake and Streamlit to deliver real-time recommendations through a user-friendly interface.

Overview
The project aims to recommend businesses to users based on their preferences and reviews. It processes data from the Yelp dataset, stores it in Snowflake, and utilizes embeddings to understand business characteristics. A Streamlit app serves as the front-end, allowing users to interact with the recommendation system seamlessly.

Architecture
Data Ingestion: Yelp dataset is stored in AWS S3.

Data Loading: Snowpipe is used to load data from S3 into Snowflake tables (business, reviews, users).

Data Processing:

Embeddings are created for businesses to capture their features.
User preferences are analyzed based on their reviews and interactions.
Recommendation Engine: An LLM (Large Language Model) processes embeddings to generate personalized recommendations.

Front-End: A Streamlit app provides an interface for users to receive and interact with recommendations.
![image](https://github.com/user-attachments/assets/76c3cdf5-9d40-424e-9499-a31ddd8860fa)

Features
Real-Time Recommendations: Get instant business suggestions based on user preferences.
Interactive Interface: User-friendly Streamlit app for seamless interaction.
Scalable Architecture: Utilizes Snowflake and AWS S3 for efficient data storage and processing.
Advanced Analytics: Employs embeddings and LLMs for deep understanding of business features and user preferences.
