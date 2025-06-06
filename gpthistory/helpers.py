import json
import os
import pandas as pd
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Load environment variables from ~/.bin/.env first, then fallback to standard .env
dotenv_path = os.path.expanduser("~/.bin/.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define the path to the index file in the user's home directory
INDEX_PATH = os.path.join(os.path.expanduser('~'), '.gpthistory', 'chatindex.csv')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_text_parts(data):
    """
    Extract text parts from chat data.
    """
    text_parts = []
    message = data.get('message')
    if message:
        content = message.get('content')
        if content and content.get('content_type') == 'text':
            text_parts.extend(content.get('parts', []))
    return text_parts

def split_into_batches(array, batch_size):
    """
    Split an array into batches.
    """
    for i in range(0, len(array), batch_size):
        yield array[i:i + batch_size]

def generate_query_embedding(query):
    """
    Generate an embedding for a query using OpenAI API (updated for v1+).
    """
    try:
        response = client.embeddings.create(
            input=[query],
            model="text-embedding-3-small"  # Updated to latest model
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating query embedding: {e}")
        return [0.0] * 1536  # Return zero vector on error

def generate_embeddings(conversations):
    """
    Generate embeddings for conversations using OpenAI API (updated for v1+).
    """
    embeddings = []
    for i, batch in enumerate(split_into_batches(conversations, 100)):
        logger.info(f"Generating Embeddings for batch: {i + 1}")
        try:
            response = client.embeddings.create(
                input=batch,
                model="text-embedding-3-small"  # Updated to latest model
            )
            tmp_embedding = [embedding.embedding for embedding in response.data]
            embeddings += tmp_embedding
        except Exception as e:
            logger.error(f"Error generating embeddings for batch {i + 1}: {e}")
            # Add zero vectors for failed batch to maintain consistency
            tmp_embedding = [[0.0] * 1536] * len(batch)
            embeddings += tmp_embedding
    
    if len(embeddings) > 0:
        logger.info("Conversations (Chunks) = %d", len(conversations))
        logger.info("Embeddings = %d", len(embeddings))
    else:
        logger.info("No new conversations detected")
    return embeddings

def calculate_top_titles(df, query, top_n=1000):
    """
    Calculate top titles for a given query using embeddings (updated for v1+).
    """
    try:
        # Extract the embeddings from the DataFrame
        embedding_array = np.array(df['embeddings'].tolist())
        query_embedding = generate_query_embedding(query)
        
        # Calculate the dot product between the query embedding and all embeddings in the DataFrame
        dot_scores = np.dot(embedding_array, query_embedding)

        # DEBUG: Show score distribution
        logger.info(f"Score range: {dot_scores.min():.3f} to {dot_scores.max():.3f}, mean: {dot_scores.mean():.3f}")
        logger.info(f"Scores above 0.3: {np.sum(dot_scores >= 0.3)}, above 0.5: {np.sum(dot_scores >= 0.5)}, above 0.8: {np.sum(dot_scores >= 0.8)}")

        # Filter out titles with dot scores below the threshold (lowered from 0.8 to 0.3)
        mask = dot_scores >= 0.3
        filtered_dot_scores = dot_scores[mask]
        filtered_titles = df.loc[mask, 'text'].tolist()
        filtered_chat_ids = df.loc[mask, 'chat_id'].tolist()

        logger.info(f"Found {len(filtered_titles)} results above threshold 0.3")

        if len(filtered_titles) == 0:
            logger.info("No results found above threshold. Showing top 5 scores regardless:")
            top_5_indices = np.argsort(dot_scores)[::-1][:5]
            for i, idx in enumerate(top_5_indices):
                logger.info(f"  {i+1}. Score: {dot_scores[idx]:.3f} - {df.iloc[idx]['text'][:100]}...")
            return [], [], []

        # Sort the filtered titles based on the dot scores (in descending order)
        sorted_indices = np.argsort(filtered_dot_scores)[::-1][:top_n]

        # Get the top N titles and their corresponding dot scores
        chat_ids = [filtered_chat_ids[i] for i in sorted_indices]
        top_n_titles = [filtered_titles[i] for i in sorted_indices]
        top_n_dot_scores = filtered_dot_scores[sorted_indices]

        return chat_ids, top_n_titles, top_n_dot_scores
        
    except Exception as e:
        logger.error(f"Error in calculate_top_titles: {e}")
        # Return empty results on error
        return [], [], []