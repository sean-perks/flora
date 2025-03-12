# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 11:37:31 2023
This is old code that was not built using definitions and needs to be refactored eventually.
It works as is and is fairly accurate at spell check. it is VERY slow, so that needs fixing also


@author: sperks
"""

from ui.input_validation import *
from joblib import Memory
from os.path import expanduser

from Levenshtein import distance as levenshtein
import pandas as pd
import timeit



class SpellCheck:
    memory = Memory(expanduser('~/.cache/spell'), verbose=0)
    mega_df = pd.read_pickle(r"C:\Users\sperks\PycharmProjects\flora basic\data\mega_species_list_pickle.pkl")
    mega_df.fillna(value = "NONE", inplace = True)
    ALL_SPECIES = list(mega_df["scientific_name"])
    SYNONYM_DF = mega_df[mega_df["Synonym Symbol"] != "NONE"]
    SYNONYMS = list(SYNONYM_DF["scientific_name"])

    @classmethod
    @memory.cache
    def load_words(cls):
        return tuple([x.strip() for x in cls.ALL_SPECIES])

    @classmethod
    @memory.cache
    def spell(cls, word, count=3, dict_words=None):
        dict_words = cls.load_words() if dict_words is None else dict_words
        word_list = sorted(dict_words, key=lambda dw: levenshtein(word, dw))[:count]
        word_dict = {}
        c=1
        for item in word_list:
            word_dict[str(c)] = item
            c += 1
        return word_dict

    @classmethod
    def lookup_symbol(cls, symbol):
        for index, row in cls.mega_df.iterrows():
            if row["Symbol"] == symbol:
                return row["scientific_name"]
            return None

    @classmethod
    def check_synonym(cls, word):
        if word not in cls.SYNONYMS:
            return word
        for index, row in cls.SYNONYM_DF.iterrows():
            if row["scientific_name"] == word:
                new_name = cls.lookup_symbol(row["Symbol"])
                if new_name is not None:
                    return new_name
                else:
                    return word


    @staticmethod
    def print_dict(dict):
        print()
        for k, v in dict.items():
            print(f"{k}. {v}")


    @classmethod
    def spell_check_list(cls, species_list):
        new_list = []
        if species_list is None:
            return
        for word in species_list:
            # word found in the mega usda list
            if word in cls.ALL_SPECIES:
                checked_word = cls.check_synonym(word)
                if checked_word != word:
                    accept_synonym = y_n(f"\n{word} is a synonym! Would you like to use the new name: {checked_word}? (y/n): ")
                    if accept_synonym:
                        new_list.append(checked_word)
                    else:
                        new_list.append(word)
                else:
                    new_list.append(checked_word)
            # word not in mega usda list (spelt wrong)
            else:
                word_dict = cls.spell(word)
                word_dict[str(len(word_dict) + 1)] = "None of these"
                choices = list(word_dict.keys())
                print(f"\n\nOriginal spelling: {word}")
                cls.print_dict(word_dict)
                choice = select_item(
                    prompt="\nSelect correct spelling: ",
                    error=f"Answer must be in: {list(word_dict.keys())}",
                    choices=choices,
                )
                if choice == choices[-1]:
                    new_list.append(word)
                else:
                    new_list.append(word_dict[choice])

        if new_list == species_list:
            print("\nNo Spelling Errors!")
        return new_list


