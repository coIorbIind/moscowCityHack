import pandas as pd
import numpy as np
import nltk
import spacy

from pymorphy2 import MorphAnalyzer
import re

from string import punctuation
from sklearn.metrics.pairwise import cosine_similarity

punctuation = punctuation.replace('.', '')

nltk.download('stopwords')
nltk.download('punkt')


# !python -m spacy download ru_core_news_lg


def top_similar_vectors(text_vectors: list, target_vector: np.array, max_count: int):
    target_vector = target_vector.reshape((1, -1))

    vectors_dist = [{'text_id': text_id,
                     'Cosine measure': cosine_similarity(t_vect.reshape((1, -1)), target_vector)[0][0],
                     }
                    for text_id, t_vect in enumerate(text_vectors)]
    return sorted(vectors_dist, key=lambda x: x['Cosine measure'], reverse=True)[:max_count]


class SimilarityModel:
    def __init__(self, vect_path: str):
        self.tokenizer = nltk.tokenize.word_tokenize
        self.morph_analyzer = MorphAnalyzer()
        self.stop_words_lst = nltk.corpus.stopwords.words('russian')
        self.word_regex = '[А-я]+'
        self.vocabulary = dict()
        self.idf_coefs = dict()
        self.vect_path = vect_path
        self.vec_size = 0
        self.spacy_model = spacy.load('ru_core_news_lg')


    def train(self, texts: pd.DataFrame):
        preprocessed_texts = self.__preprocessing__(texts)

        # Creating vocabulary
        all_words = list()
        for t_text in preprocessed_texts:
            all_words += t_text

        self.vocabulary = {word: np.ones(300) for word in set(all_words)}

        # Getting embedding vectors for our vocabulary
        with open(self.vect_path, "rt", encoding="UTF-8") as file:
            file.readline()  # Reading first useless line
            for line in file:
                elements = line.split(' ')
                if elements[0] in self.vocabulary:
                    self.vocabulary[elements[0]] = np.array(elements[1:-1], np.float16)


        # Finding idf values for each word
        text_num = len(preprocessed_texts)

        for t_text in preprocessed_texts:
            unique_words = set(t_text)
            for word in unique_words:
                self.idf_coefs[word] = (self.idf_coefs.get(word, 0) + 1) / text_num
        # Saving word vector size
        self.vec_size = self.vocabulary[list(self.vocabulary.keys())[0]].shape[0]

        self.vectors = [self.get_text_vect(text) for text in texts.full_text]
        self.original_texts = texts

    def predict(self, text: str):
        text_vect = self.get_text_vect(text)

        # Finding most similar vectors
        sim_vect_lst = top_similar_vectors(self.vectors, text_vect, max_count=5)

        original_text = max(sim_vect_lst, key=lambda x: x['Cosine measure'])

        original_text_proc = self.spacy_model(self.original_texts.iloc[original_text['text_id']]['full_text'])
        target_text_proc = self.spacy_model(text)

        text_comp_res = self._compare_texts(original_text_proc, target_text_proc)

        text_comp_res['similarity'] = original_text['Cosine measure']

        # print(original_text['text_id'])
        # print(type(original_text['text_id']))
        # print(self.original_texts)
        # print(type(self.original_texts))

        # print(original_text)
        #
        # print(original_text['text_id'])
        #
        # print(self.original_texts.iloc[original_text['text_id']])

        text_comp_res['origId'] = self.original_texts.iloc[original_text['text_id']]['id']

        # print(self.original_texts.iloc[original_text['text_id']])

        directQuotesCount = len(self._get_quotes(text, self.original_texts.iloc[original_text['text_id']]['full_text']))
        text_comp_res['directQuotesCount'] = directQuotesCount

        return text_comp_res

    def _get_quotes(self, target_text, original_text):
        quotes = list()

        target_sentences = [item.strip() for item in target_text.split(".")]
        # print(target_sentences)

        original_sentences = [item.strip() for item in original_text.split(".")]
        # print(original_sentences)
        for target_sentence in target_sentences:
            if target_sentence and target_sentence in original_sentences:
                quotes.append(target_sentence + ".")

        return quotes

    def get_text_vect(self, text: str):
        # Getting document vector
        text_vector = np.zeros(self.vec_size, dtype=np.float16)

        # Text preprocessing
        prep_text = self.__preprocessing__([text])[0]

        for word_id, word in enumerate(prep_text):
            text_vector += self.vocabulary.get(word, 1) * self.idf_coefs.get(word, 0)
        text_vector /= (len(prep_text) + 1)

        return text_vector

    def __preprocessing__(self, texts: list):
        # Tokenization
        tokenized_texts = [self.tokenizer(t_text) for t_text in texts]

        # Lemmatization
        lemm_texts = [[self.morph_analyzer.parse(word)[0].normal_form for word in t_text
                       if re.match(self.word_regex, word)] for t_text in tokenized_texts]

        # Deleting stop words
        preprocessed_texts = [[word for word in t_text if word not in self.stop_words_lst] for t_text in lemm_texts]

        return preprocessed_texts

    def _find_similar_sentences_inds(self, original_sent_lst, target_sent_lst):
        # Finds ids of the similar sentences
        similar_sent_id_lst = list()

        for targ_ind, targ_sent in enumerate(target_sent_lst):
            sent_similarity = list()
            for orig_ind, source_sent in enumerate(original_sent_lst):
                sent_similarity.append((orig_ind, targ_sent.similarity(source_sent)))
            most_sim_sent = max(sent_similarity, key=lambda x: x[1])

            similar_sent_id_lst.append({"target_sent_ind": targ_ind,
                                        "source_sent_ind": most_sim_sent[0],
                                        "similarity": most_sim_sent[1]})

        return similar_sent_id_lst

    def _find_most_sim_words(self, targ_word, search_lst):
        # Finds most similar words to the target
        most_sim_word = None
        most_sim_val = 0

        for word_id, word in enumerate(search_lst):
            if targ_word.lemma_ == word.lemma_:
                return word_id, word
            elif targ_word.similarity(word) >= most_sim_val:
                most_sim_word = (word_id, word)
                most_sim_val = targ_word.similarity(word)

        return most_sim_word

    def _compare_texts(self, original_text, target_text):

        orig_sents = list(original_text.sents)
        targ_sents = list(target_text.sents)

        similar_sents_inds = self._find_similar_sentences_inds(orig_sents, targ_sents)

        sent_sim_threshold = 0.8
        # Finding closest sentences
        closest_sents_inds = [t_ind for t_ind in similar_sents_inds if t_ind['similarity'] >= sent_sim_threshold]
        unknown_sents_inds = [t_ind for t_ind in similar_sents_inds if t_ind['similarity'] < sent_sim_threshold]

        # Finding fake facts
        processed_sim_sents = list()

        words_threshold = 0.1

        result_text = ""
        fakes_count = 0

        for temp_ind in closest_sents_inds:
            # Getting sentences by index
            targ_sent = targ_sents[temp_ind['target_sent_ind']]
            orig_sent = orig_sents[temp_ind['source_sent_ind']]
            # This list stores elements that should be word tokens
            fake_words = list()
            fake_words_in_orig = list()

            # Finding subjects
            targ_subj_lst = list(filter(lambda word: 'nsubj' in word.dep_ or
                                                     'conj' in word.dep_ and 'nsubj' in word.head.dep_, targ_sent))

            orig_subj_lst = list(filter(lambda word: 'nsubj' in word.dep_ or
                                                     'conj' in word.dep_ and 'nsubj' in word.head.dep_, orig_sent))

            # Finding roots
            targ_root_lst = list(filter(lambda word: 'ROOT' in word.dep_ or
                                                     'advcl' in word.dep_ and 'ROOT' in word.head.dep_, targ_sent))

            orig_root_lst = list(filter(lambda word: 'ROOT' in word.dep_ or
                                                     'advcl' in word.dep_ and 'ROOT' in word.head.dep_, orig_sent))

            # Finding objects
            targ_obl_lst = list(filter(lambda word: 'obl' in word.dep_ or
                                                    'conj' in word.dep_ and 'obl' in word.head.dep_, targ_sent))

            orig_obl_lst = list(filter(lambda word: 'obl' in word.dep_ or
                                                    'conj' in word.dep_ and 'obl' in word.head.dep_, orig_sent))

            # Checking subjects
            for word in targ_subj_lst:
                temp_lst = list(filter(lambda temp_word: temp_word.lemma_ == word.lemma_
                                                         or temp_word.similarity(word) > words_threshold,
                                       orig_subj_lst))
                if not temp_lst:
                    fake_words.append(word)

            # Checking roots
            for word in targ_root_lst:
                temp_lst = list(filter(lambda temp_word: temp_word.lemma_ == word.lemma_
                                                         or temp_word.similarity(word) > words_threshold,
                                       orig_root_lst))
                if not temp_lst:
                    fake_words.append(word)

            # Checking obl
            for word in targ_obl_lst:
                temp_lst = list(filter(lambda temp_word: temp_word.lemma_ == word.lemma_
                                                         or temp_word.similarity(word) > words_threshold, orig_obl_lst))
                if not temp_lst:
                    fake_words.append(word)

            # Checking subjects opposite
            for word in orig_subj_lst:
                temp_lst = list(filter(lambda temp_word: temp_word.lemma_ == word.lemma_
                                                         or temp_word.similarity(word) > words_threshold,
                                       targ_subj_lst))
                if not temp_lst:
                    fake_words_in_orig.append(word)

            # Checking roots opposite
            for word in orig_root_lst:
                temp_lst = list(filter(lambda temp_word: temp_word.lemma_ == word.lemma_
                                                         or temp_word.similarity(word) > words_threshold,
                                       targ_root_lst))
                if not temp_lst:
                    fake_words_in_orig.append(word)

            # Checking obl opposite
            for word in orig_obl_lst:
                temp_lst = list(filter(lambda temp_word: temp_word.lemma_ == word.lemma_
                                       or temp_word.similarity(word) > words_threshold, targ_obl_lst))
                if not temp_lst:
                    fake_words_in_orig.append(word)

            targ_nums_lst = list(filter(lambda word: 'NUM' in word.pos_, targ_sent))

            orig_nums_lst = list(filter(lambda word: 'NUM' in word.pos_, orig_sent))

            for word in targ_nums_lst:
                temp_lst = list(filter(lambda temp_word: temp_word.lemma_ == word.lemma_
                                       or temp_word.similarity(word) > words_threshold,
                                       orig_nums_lst))
                if not temp_lst:
                    fake_words.append(word)

            for word in orig_nums_lst:
                temp_lst = list(filter(lambda temp_word: temp_word.lemma_ == word.lemma_
                                       or temp_word.similarity(word) > words_threshold,
                                       targ_nums_lst))
                if not temp_lst:
                    fake_words_in_orig.append(word)

            result_text = str(targ_sent)
            result_orig_text = str(orig_sent)

            # print(fake_words)

            # Marking fake words
            for word in targ_sent:
                if word in fake_words:  # and not word.pos_ == 'PROPN':
                    result_text = result_text.replace(str(word), '<span class="red">' + str(word) + '</span>')

            for word in orig_sent:
                if word in fake_words_in_orig:
                    result_orig_text = result_orig_text.replace(str(word),
                                                                '<span class="green">' + str(word) + '</span>')

            processed_sim_sents.append({
                "userSentence": result_text,
                "originalSentence": result_orig_text
            }
            )

            fakes_count += len(fake_words)

        result_dict = {
            "distortionCount": fakes_count,
            "stuffingCount": len(unknown_sents_inds),
            "sentences": processed_sim_sents
        }

        return result_dict


if __name__ == '__main__':
    model = SimilarityModel("")
    print("Created model")
    texts = pd.read_json("mos_ru.json", encoding="utf8")
    print("Text reading finished")
    print(texts.iloc[:20])
    model.train(texts.iloc[:20])
    print("Model training finished")
    model.predict("Привет мир")
