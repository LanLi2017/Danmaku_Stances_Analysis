from scipy.spatial import distance
from sklearn.feature_extraction.text import CountVectorizer


# cosine
def cosine_distance_countvectorizer_method(s1, s2):
    sentences = [s1, s2]

    # text to vector
    vectorizer = CountVectorizer()
    all_sentences_to_vector = vectorizer.fit_transform(sentences)
    text_to_vector_v1 = all_sentences_to_vector.toarray()[0].tolist()
    text_to_vector_v2 = all_sentences_to_vector.toarray()[1].tolist()

    # distance of similarity
    cosine = distance.cosine(text_to_vector_v1, text_to_vector_v2)
    print('Similarity of two sentences are equal to ', round((1-cosine)*100, 2), '%')
    return cosine


def clustering_video(sliding_window_size=5):


    pass


def main():
    pass


if __name__=='__main__':
    main()



