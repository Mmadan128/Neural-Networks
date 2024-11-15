import numpy as np
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
# Content-based filtering
def content_based_scores(events, user_preferences):
    # Calculate cosine similarity between user preferences and event genres
    content_similarity = cosine_similarity(user_preferences, events.iloc[:, 2:])
    return content_similarity[0]

# Collaborative filtering with NMF
def collaborative_scores(user_event_data, user_id):
    nmf = NMF(n_components=2, random_state=42)
    user_factors = nmf.fit_transform(user_event_data)  # Shape: (num_users, n_components)
    event_factors = nmf.components_  # Shape: (n_components, num_events)
    
    # Get predicted scores for all events for the given user (user_id)
    predicted_scores = np.dot(user_factors[user_id], event_factors)  # Shape: (num_events,)
    return predicted_scores  # Predicted scores for all events

# Hybrid recommendation combining content-based and collaborative filtering
def hybrid_scores_r(events, user_preferences, user_event_data, user_id, alpha=0.6, beta=0.4):
    # Get content-based scores (genre similarity)
    content_scores = content_based_scores(events, user_preferences)
    
    # Get collaborative-based scores (predicted ratings for each event)
    collab_scores = collaborative_scores(user_event_data, user_id)
    
    # Ensure both scores have the same shape (length)
    if len(content_scores) != len(collab_scores):
        raise ValueError(f"Content scores length: {len(content_scores)}, Collaborative scores length: {len(collab_scores)}")
    
    # Combine the scores using alpha and beta
    hybrid_scores = alpha * content_scores + beta * collab_scores
    
    # Sort the events by hybrid score (descending order)
    sorted_indices = np.argsort(hybrid_scores)[::-1]
    recommended_events = events.iloc[sorted_indices]
    
    return recommended_events[["event_id", "title"]]

# Example user preferences and event data (replace with real data)
user_preferences = np.array([[1, 0, 1, 0, 0, 0, 0]])  # Example user preferences
events = pd.DataFrame({
    "event_id": [1, 2, 3, 4, 5],
    "title": ["Rock Concert", "Stand Up", "Hockey Match", "Tech Conference", "Dance Performance"],
    "music": [1, 0, 0, 0, 0],
    "sports": [0, 0, 1, 0, 0],
    "comedy": [0, 1, 0, 0, 0],
    "art": [0, 0, 0, 0, 0],
    "tech": [0, 0, 0, 1, 0],
    "theater": [0, 0, 0, 0, 0],
    "dance": [0, 0, 0, 0, 1],
})

# Example user-event interaction data (replace with real data)
user_event_data = np.array([
    [5, 3, 0, 0, 0],  # User 1
    [0, 4, 5, 0, 0],  # User 2
    [5, 0, 4, 0, 0],  # User 3
])

user_id = 0  # First user (User 1)

# Get recommendations for the user
recommended_events = hybrid_scores_r(events, user_preferences, user_event_data, user_id)
print("Recommended Events:")
print(json.dumps(recommended_events))