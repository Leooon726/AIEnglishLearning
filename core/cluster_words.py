import os
import numpy as np
import logging
from sklearn.cluster import KMeans
from word_vector_manager import WordVectorManager
import csv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the number of cores to use
os.environ["LOKY_MAX_CPU_COUNT"] = "4"  # Replace 4 with the number of cores you want to use

def cluster_word_vectors(word_vectors, n_clusters):
    logging.info("Converting word vectors to numpy array.")
    # Convert list of word vectors to a numpy array
    X = np.array(word_vectors)
    
    logging.info("Initializing KMeans with %d clusters.", n_clusters)
    # Initialize KMeans with the desired number of clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    
    logging.info("Fitting KMeans model to the data.")
    # Fit the model to the data
    kmeans.fit(X)
    
    # Get the cluster labels
    labels = kmeans.labels_
    logging.info("Clustering completed. Labels obtained.")
    
    return labels, kmeans

class WordClusterer:
    def __init__(self, glove_file, input_csv, output_csv, n_clusters=20):
        self.glove_file = glove_file
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.n_clusters = n_clusters
        self.manager = WordVectorManager(glove_file)

    def load_word_vectors(self):
        logging.info("Loading word vectors from CSV file: %s", self.input_csv)
        return self.manager.load_from_csv(self.input_csv)

    def save_clustered_words(self, clustered_word_dicts):
        clustered_word_dicts.sort(key=lambda x: int(x['index'].rstrip('.')))
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['index', 'word', 'meaning', 'cluster_label', 'vector'])
            for word_dict in clustered_word_dicts:
                writer.writerow([word_dict['index'], word_dict['word'], word_dict['meaning'], word_dict['cluster_label'], word_dict['vector']])
        logging.info("Saved clustered word list to CSV file: %s", self.output_csv)

    def run(self):
        loaded_word_dicts = self.load_word_vectors()

        # Prepare to filter and assign cluster labels
        clustered_word_dicts = []
        word_vectors = []
        word_dicts_with_vectors = []
        for word_dict in loaded_word_dicts:
            if word_dict['vector']:
                word_vectors.append(word_dict['vector'])
                word_dicts_with_vectors.append(word_dict)
            else:
                word_dict['cluster_label'] = -1  # Assign label -1 for empty vectors
                clustered_word_dicts.append(word_dict)  # Still include in the output

        logging.info("Clustering word vectors into %d clusters.", self.n_clusters)
        labels, kmeans_model = cluster_word_vectors(word_vectors, self.n_clusters)

        # Add cluster labels to the filtered word_dicts
        logging.info("Adding cluster labels to word dictionaries.")
        for i, word_dict in enumerate(word_dicts_with_vectors):
            word_dict['cluster_label'] = labels[i]
            clustered_word_dicts.append(word_dict)  # Still include in the output

        self.save_clustered_words(clustered_word_dicts)

if __name__ == "__main__":
    glove_file = 'D:/Study/AIAgent/glove.42B.300d.txt'  # Adjust this path if necessary
    input_csv = 'D:/Study/AIAgent/output/CET4_700_word_vectors.csv'
    output_csv = 'D:/Study/AIAgent/output/CET4_700_clustered_word_list.csv'
    clusterer = WordClusterer(glove_file, input_csv, output_csv)
    clusterer.run()
