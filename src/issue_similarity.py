from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')


def calculate_similarity(source, destination):
    embedding_1 = model.encode(source, convert_to_tensor=True)
    embedding_2 = model.encode(destination, convert_to_tensor=True)

    return (util.pytorch_cos_sim(embedding_1, embedding_2)).item()


def calculate_similarity_batch(source, sentences):
    embedding_source = model.encode([source], convert_to_tensor=True)
    embedding_destinations = model.encode(sentences, convert_to_tensor=True)

    cosine_similarities = util.pytorch_cos_sim(embedding_source, embedding_destinations)

    similarities_list = cosine_similarities[0].tolist()

    return similarities_list


def extract_max_match(base_text, comparing_texts):
    similarity_scores = calculate_similarity_batch(base_text, comparing_texts)
    max_score = max(similarity_scores)
    return max_score, similarity_scores
