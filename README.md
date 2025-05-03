# Street-Fairy-Chatbot Implementation
Street-Fairy: Business Recommendations ChatBot with Personalized Itinerary Planning
Street Fairy is a business recommendation system that utilizes Yelp dataset to provide personalized suggestions to users.
The project integrates Snowflake embeddings and Streamlit to deliver real-time recommendations through a user-friendly interface.

**Overview**
The project aims to recommend businesses to users based on their preferences and recent visits. It processes data from the Yelp dataset, stores it in Snowflake, and utilizes embeddings to understand business characteristics. A Streamlit app serves as the front-end, allowing users to interact with the recommendation system seamlessly.

**Architecture**
Data Ingestion: Yelp dataset is stored in AWS S3 bucket.

**Data Loading**: Snowpipe is used to load data from S3 into Snowflake tables (business, reviews, users).

**Data Processing:**
DBT models are created on the Snowflake DWH - Business Model, Attribute Model, Categories model which would be base for the Business Embeddings Table 
Embeddings are created on the Business Embeddings table (MiniML Model) to capture their features.
User preferences are analyzed based on their reviews and interactions.


Front-End: A Streamlit app provides an interface for users to receive and interact with recommendations.
![image](https://github.com/user-attachments/assets/76c3cdf5-9d40-424e-9499-a31ddd8860fa)

Features
Real-Time Recommendations: Get instant business suggestions based on user preferences.
Interactive Interface: User-friendly Streamlit app for seamless interaction.
Scalable Architecture: Utilizes Snowflake and AWS S3 for efficient data storage and processing.
Advanced Analytics: Employs embeddings and LLMs for deep understanding of business features and user preferences.

**Login Page:**
![image](https://github.com/user-attachments/assets/10575529-c998-4ed4-90d0-6c75bc62cd02)

**Recommendation Page:**
![image](https://github.com/user-attachments/assets/77c418ac-da61-44fc-987f-7893c7383959)

**Feedback Loop:**
![image](https://github.com/user-attachments/assets/f2faab0a-fee5-4c54-8e8a-341296df505b)

# 📂Chatbot - FAISS_Implement/
# 📂main.py
Main UI router: sidebar, tabs (login & chat), navigation logic. Sets up the sidebar, manages tab navigation (Login/Register, Recommendations & Chat), and delegates control to the appropriate screen.

Main UI logic and navigation for the app.

Configures Streamlit’s page settings (title, layout).

Builds a sidebar with app info and user login status.

Uses two main tabs: Login/Register and Recommendations & Chat.

Delegates logic to screen_0 (login/register) and screen_2 (chat) based on user session state.

Ensures users must log in before accessing chat/recommendations.

# 📂screen.py
Main UI Router: Sidebar, Tabs (Login & Chat), Navigation Logic

The screen.py file handles the layout and navigation of the Streamlit app. It sets up the sidebar and manages the navigation between tabs: Login/Register and Recommendations & Chat. It delegates control to appropriate screens based on the user session state.

Key functionalities:
Configures Streamlit’s page settings, including title and layout.

Builds a sidebar with app information and user login status.

Uses two main tabs:

Login/Register

Recommendations & Chat

Delegates the logic to screen_0 (Login/Register) and screen_2 (Chat) based on the user session state.

Ensures that users must log in before accessing recommendations or chat.

# 📂screens/chat.py
Chat UI: manages chat history, user queries, recommendations, and conversation flow. Conversational chat interface. Handles user chat, displays chat history, handles user input, business recommendations, and context-aware suggestions based on user actions and search queries.

Conversational chat screen with the Street Fairy assistant.

Shows a sticky, modern chat UI using Streamlit’s chat components and custom CSS.

Displays chat history (user and assistant messages). Accepts and processes user chat input.

Checks if the user is referencing a previously recommended business. Handles search for nearby places using embedding-based similarity.

Shows friendly, summarized recommendations with LLM-generated responses (via Ollama). Supports "planning mode" for navigation between places.

Updates and reruns UI after each new user input.

# 📂screens/login.py
User login/registration UI; connects to Snowflake for authentication and preference storage. User authentication and registration.

Manages user login and new user registration. Connects to Snowflake to check credentials or create a new user. Loads and updates user preferences in session state.

User authentication and registration interface. Presents a radio button to switch between Login and Registration.

On login: Connects to Snowflake and verifies credentials. Loads user name, ID, and preference categories into session state. Initializes feedback tracking (liked/disliked categories).

On registration: Accepts user details and preferences. Inserts new user record into the Snowflake database. Handles errors (duplicate ID, missing fields). Provides clear feedback for success, errors, or incomplete forms.

# 📂utils/database.py
Database helper functions; handles connection and updates to user preferences in Snowflake.

Helper functions for database operations (Snowflake).

Loads Snowflake credentials from a secure key.json (not in repo).

Creates and returns a Snowflake database connection object.

Updates user preferences (CATEGORIES) in the database when users like/dislike businesses.

Uses Streamlit toast/alerts for feedback on preference updates.

Handles connection cleanup and error reporting gracefully.

# 📂utils/query.py
Embedding search using FAISS, distance calculation, and calls to the LLM API (Ollama) for natural language recommendations.

Loads the FAISS business embeddings collection, runs semantic similarity search with SentenceTransformer embeddings, computes distances, and returns ranked business results.

Also provides query_ollama() for generating recommendations using a local LLM via HTTP API.

Handles embedding search, vector retrieval, and LLM interaction. Loads a persistent FAISS collection with SentenceTransformer embeddings.

Performs semantic similarity searches for user queries: Returns metadata-rich business results (location, stars, categories, etc.).

Computes distances (using geopy) between user and business locations.

Handles missing data by generating default values (e.g., stars, distances).

Provides a function to send prompts to a local Ollama LLM server (or any compatible LLM API). Returns model-generated, contextually relevant recommendations for the chat UI. Uses caching for fast repeated access to the FAISS collection.

# 📂utils/planner.py
Planner: Handles the planning mode for guiding users between recommended places or managing a sequence of actions based on the user's choices.

Initialize Planner: Starts the planning session by receiving the user’s location, preferences, and previous recommendations.

Plan Next Steps: Based on user input, generates the next business recommendation by considering the user’s preferences and location.

Update Recommendations: Updates the planner state based on the user's action (e.g., selecting a business or asking for more details).

Handle User Decisions: Captures decisions such as 'I want to go to this place' or 'What is the next best recommendation?' and updates the flow accordingly.

Feedback Loop: Updates recommendations based on the feedback the user gives (e.g., "I liked this business").

# 📁DBT Models/
This directory contains all DBT models and configuration files used for transforming and enriching the business dataset for the recommendation engine.

# 1. Attribute_Model.sql
Extracts and flattens business attributes from JSON.

Parses the Attributes column for open businesses in selected states.
Flattens the JSON attributes into key-value pairs for easier downstream processing.
# 2. Attribute_Processing_Model.sql
Processes and normalizes complex, nested attribute values.

Cleans up attribute values by handling quotes, None, and other string patterns.
Further flattens nested JSON objects by concatenating attribute names and sub-keys.
# 3. Business_Model.sql
Cleans and structures the business table.

Selects open businesses with at least a 3-star rating from specified states.
Extracts business details including name, address, categories, and daily hours.
# 4. Category_Model.sql
Splits and flattens business categories.

Splits the Categories field into individual values for each business.
Produces a table of business-category pairs for flexible category analysis.
# 5. Final_Attribute_Model.sql
Combines and cleans processed attributes.

Merges results from Attribute_Model and Attribute_Processing_Model.
Removes invalid or placeholder values, standardizing the final attribute set for each business.
# 6. dbt_project.yml
DBT project configuration file.

Defines project structure, model/materialization defaults, and folder paths for models, macros, seeds, etc.
# 7. schema.yml
Schema and data quality tests for DBT models.

Documents each model and its columns.
Adds tests for primary/foreign keys (e.g., uniqueness and not-null constraints) to ensure data quality.

# 📄 Requirements.txt
Lists all Python dependencies required to run the project, including libraries for data processing, machine learning, and web application development.

# Usage:
<pre> ```bash streamlit run .\main.py ``` </pre>

<pre> ```bash ollama run mistral ``` </pre>


