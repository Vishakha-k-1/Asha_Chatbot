try:
    from google.cloud import aiplatform
    PROJECT_ID = "your-project-id"
    LOCATION = "us-central1"
    
    # Initialize Vertex AI
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    print("Vertex AI client initialized successfully.")
except Exception as e:
    print(f"Error initializing Vertex AI: {e}")
