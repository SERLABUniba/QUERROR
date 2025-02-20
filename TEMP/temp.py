import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

# Sample list of texts (replace this with your actual list of 5000 texts)
texts = [
    "Sample text 1",
    "Sample text 12",
    "sample text 23",
    "sample text 46",
    "sample text 15",
    "sample text 61",
    "sample text 97",
    "sample text 83",
    "sample text 29",
    "sample text 1110",
    "sample text 3011",
    "sample text 1112",
    "sample text 7113",
    "sample text 1114",
    "sample text 1115",
    "sample text 3316",
    "sample text 7117",
    "sample text 1128",
    "sample text 1519",
    "sample text 9120",
]

top_num = 10

# Step 1: Text Vectorization using TF-IDF
# vectorizer = TfidfVectorizer()
# tfidf_matrix = vectorizer.fit_transform(texts)
#
# # Step 2: Compute the cosine similarity matrix
# similarity_matrix = cosine_similarity(tfidf_matrix)
#
# # Step 3: Set values of diagonal elements to 0 [as the [i][j] element is always 1 as it is a similarity matrix]
# np.fill_diagonal(similarity_matrix, 0)
#
# # similarity_matrix now contains the pairwise cosine similarity scores
# print(similarity_matrix)

# Create a list of lists with each list containing the top 5 similarities in descending order for each text
# While creating the top_5_similarities list, create each element of the list as a tuple containing the index of the
# text and the similarity score
# top_5_similarities = []
# for i in range(len(similarity_matrix)):
#     top_5_similarities.append(np.argsort(similarity_matrix[i])[::-1][:5])
#
# print(top_5_similarities)
#
# print(top_5_similarities[0][0])
#
# # Create a list of tuples (index, value) for the top 5 values
# top_5_tuples = [(index, similarity_matrix[i][index]) for index in top_5_similarities]
#
# print(top_5_tuples)

print(type(texts))
print(texts)
print(texts[0])
exit(0)

# Load a pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode the list of issues into dense vectors
embeddings = model.encode(texts, convert_to_tensor=True, show_progress_bar=True)

# Compute the cosine similarity matrix
cosine_similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)

# Convert the similarity matrix to numpy for easier handling if needed
cosine_similarity_matrix_np = cosine_similarity_matrix.cpu().numpy()

# print(cosine_similarity_matrix_np)

# Set values of diagonal elements to 0 [as the [i][j] element is always 1 as it is a similarity matrix]
# np.fill_diagonal(cosine_similarity_matrix_np, 0)

print(cosine_similarity_matrix_np)

# For every row create a list of top 5 similar issues along with their similarity scores
# Create an empty list to store the top 5 similar issues for each issue
top_5_similar_issues = []

# Iterate over each row in the similarity matrix
for i in range(cosine_similarity_matrix_np.shape[0]):
    # Get the row
    row = cosine_similarity_matrix_np[i]

    # Exclude the diagonal element by setting it to a very low value
    row[i] = -1

    # Get the indices of the top 5 values in the row
    top_5_indices = row.argsort()[-top_num:][::-1]

    # Retrieve the similarity scores corresponding to these indices
    top_5_scores = row[top_5_indices]

    # Create tuples of (index, score) for the top 5 similar issues
    top_5 = [(index, score) for index, score in zip(top_5_indices, top_5_scores)]

    # Append the list of top 5 similar issues for the current issue
    top_5_similar_issues.append(top_5)

# Print the top 5 similar issues for each issue
for idx, similar_issues in enumerate(top_5_similar_issues):
    print(f"Issue {idx} top 5 similar issues: {similar_issues}")

print(f"{top_5_similar_issues}")

