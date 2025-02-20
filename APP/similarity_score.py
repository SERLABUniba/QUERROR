import re
from transformers import BertModel, BertTokenizer
import torch
# import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util


def calculate_cosine_similarity(text1, text2):
    # Create the Document Term Matrix
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([text1, text2])

    # Compute the cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    print("cosine")
    return cosine_sim[0][0]


def calculate_semantic_similarity(text1, text2):
    # Load a pre-trained model
    # model = SentenceTransformer('all-MiniLM-L6-v2')
    # model = SentenceTransformer('all-mpnet-base-v2')
    model = SentenceTransformer('flax-sentence-embeddings/stackoverflow_mpnet-base')

    # Encode the paragraphs
    embeddings = model.encode([text1, text2])

    # Compute the cosine similarity
    cosine_sim = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    print("semantic")
    return cosine_sim.item()


def get_bert_embeddings(text, model, tokenizer):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)

    # Get the hidden states from the BERT model
    with torch.no_grad():
        outputs = model(**inputs)
        hidden_states = outputs.last_hidden_state

    # Compute the mean of the token embeddings
    embeddings = torch.mean(hidden_states, dim=1)
    return embeddings


def calculate_bert_similarity(text1, text2):
    # Load pre-trained BERT model and tokenizer
    model_name = 'bert-base-uncased'
    model = BertModel.from_pretrained(model_name)
    tokenizer = BertTokenizer.from_pretrained(model_name)

    # Tokenize the input texts
    tokenized_text1 = tokenizer(text1, return_tensors='pt', truncation=True, padding=True, max_length=512)
    tokenized_text2 = tokenizer(text2, return_tensors='pt', truncation=True, padding=True, max_length=512)

    # Get the BERT embeddings for the tokenized texts
    with torch.no_grad():
        embeddings1 = model(**tokenized_text1).last_hidden_state.mean(dim=1)
        embeddings2 = model(**tokenized_text2).last_hidden_state.mean(dim=1)

    # Get embeddings for both texts
    # embeddings1 = get_bert_embeddings(text1, model, tokenizer)
    # embeddings2 = get_bert_embeddings(text2, model, tokenizer)

    # Compute cosine similarity
    cosine_sim = cosine_similarity(embeddings1.numpy(), embeddings2.numpy())
    # print(f"BERT Cosine Similarity: {cosine_sim}")
    # similarity_score = (round(cosine_sim[0][0]*100, 2))
    similarity_score = cosine_sim[0][0]
    # print(f"BERT Cosine Similarity Score: {similarity_score}")
    # print("BERT")
    return similarity_score


def remove_sp_char(text):
    """
    Remove special characters, punctuations, new lines, and tabs from the text
    :param text:
    :return:
    """
    # Remove new lines
    text = text.replace('\n', ' ')
    # Remove tabs
    text = text.replace('\t', ' ')
    # Remove special characters
    text = re.sub(r'[^\w\s]', '', text)
    return text


def sbert_sim(texts):
    # Load a pre-trained sentence transformer model
    # model = SentenceTransformer('all-MiniLM-L6-v2')
    model = SentenceTransformer('flax-sentence-embeddings/stackoverflow_mpnet-base')

    # Encode the list of issues into dense vectors
    embeddings = model.encode(texts, convert_to_tensor=True, show_progress_bar=True)

    # Compute the cosine similarity matrix
    cosine_similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)

    # Convert the similarity matrix to numpy for easier handling if needed
    cosine_similarity_matrix_np = cosine_similarity_matrix.cpu().numpy()

    # print(cosine_similarity_matrix_np)

    return cosine_similarity_matrix_np


def sbert_sim_best_scores(cosine_similarity_matrix_np, top_num):
    # For every row create a list of top 5 similar issues along with their similarity scores
    # Create an empty list to store the top 5 similar issues for each issue
    top_similar_issues = []

    # Iterate over each row in the similarity matrix
    for i in range(cosine_similarity_matrix_np.shape[0]):
        # Get the row
        row = cosine_similarity_matrix_np[i]

        # Exclude the diagonal element by setting it to a very low value
        row[i] = -1

        # Get the indices of the top 5 values in the row
        top_indices = row.argsort()[-top_num:][::-1]

        # Retrieve the similarity scores corresponding to these indices
        top_scores = row[top_indices]

        # Change the indices to reflect real number of issues
        top_indices = top_indices + 1  # + 1 to not show [0] index for arrays

        # Create tuples of (index, score) for the top 5 similar issues
        tops = [(index, score) for index, score in zip(top_indices, top_scores)]

        # Append the list of top 5 similar issues for the current issue
        top_similar_issues.append(tops)

    # Print the top 5 similar issues for each issue
    # for idx, similar_issues in enumerate(top_5_similar_issues):
    #     print(f"Issue {idx} top 5 similar issues: {similar_issues}")

    # print(f"{top_5_similar_issues}")
    return top_similar_issues


def main():
    # Sample paragraphs
    # text1 = "This is the first paragraph of text that we want to compare."
    # text2 = "Here is the second paragraph. It should be compared to the first one."

    text1 = "This is the paragraph."
    text2 = "where is the paragraph."

    # similarity_score = calculate_bert_similarity(remove_sp_char(text1), remove_sp_char(text2))
    # similarity_score = calculate_cosine_similarity(text1, text2)
    similarity_score = calculate_semantic_similarity(text1, text2)
    # print(f"BERT Cosine Similarity Score: {similarity_score}")

    if similarity_score > 0.8:
        print("The two texts are semantically similar.")
    else:
        print("The two texts are not semantically similar.")


if __name__ == "__main__":
    main()
