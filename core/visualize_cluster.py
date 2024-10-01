import pandas as pd

class ClusterReader:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.grouped = self.df.groupby('cluster_label')
        self.cluster_labels = list(self.grouped.groups.keys())
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.cluster_labels):
            cluster_label = self.cluster_labels[self.current_index]
            group = self.grouped.get_group(cluster_label)
            self.current_index += 1
            return cluster_label, group[['index', 'word', 'meaning']]
        else:
            raise StopIteration

# Usage
if __name__ == "__main__":
    cluster_reader = ClusterReader('D:\Study\AIAgent\AIEnglishLearning\output\CET4_700_clustered_word_list.csv')
    for cluster_label, group in cluster_reader:
        print(f"Cluster Label: {cluster_label}")
        print(group[['word', 'meaning']])
        
        # convert to a list of tuple(word, meaning)
        word_meaning_tuples = list(zip(group['word'], group['meaning']))
        print(word_meaning_tuples)

        print("\n")
        input()
