# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 11:37:31 2023
This is old code that was not built using definitions and needs to be refactored eventually.
It works as is and is fairly accurate at spell check. it is VERY slow, so that needs fixing also


@author: sperks
"""
from dask import delayed, compute
import dask.dataframe as dd
import pandas as pd

from ui.input_validation import *
from joblib import Memory
from os.path import expanduser

from Levenshtein import distance as levenshtein
import pandas as pd
import timeit



class SpellCheck:
    mega_df = pd.read_pickle(r"C:\Users\sperks\PycharmProjects\flora basic\data\mega_species_list_pickle.pkl")
    mega_df = dd.from_pandas(mega_df, npartitions=4)
    mega_df = mega_df.fillna("NONE")
    ALL_SPECIES = set(mega_df["scientific_name"].compute())
    SYNONYM_DF = mega_df[mega_df["Synonym Symbol"] != "NONE"]
    SYNONYMS = set(SYNONYM_DF["scientific_name"].compute())


    @classmethod
    def spell(cls, word, count=3):
        def compute_distances(df):
            df["lev_distance"] = df["scientific_name"].apply(
                lambda x: levenshtein(word, x)
            )
            df_sorted = df.sort_values("lev_distance", ascending=True).head(count)

            # get best matches
            return df_sorted[["scientific_name", "lev_distance"]]

        meta = pd.DataFrame(columns=["scientific_name", "lev_distance"], dtype='object')
        closest_matches = cls.mega_df.map_partitions(compute_distances, meta=meta)
        closest_combined = closest_matches.compute().sort_values("lev_distance", ascending=True).head(count).reset_index()


        word_dict = {str(i+1): row["scientific_name"] for i, row in closest_combined.iterrows()}
        return word_dict

    @classmethod
    def lookup_symbol(cls, symbol):
        # Looking up a scientific name based on its symbol
        # This is still using Dask but performs better with pandas for small lookups
        symbol_df = cls.mega_df[cls.mega_df["Symbol"] == symbol]
        symbol_row = symbol_df.compute()
        if not symbol_row.empty:
            return symbol_row["scientific_name"].iloc[0]
        return None

    @classmethod
    def check_synonym(cls, word):
        # Check if the word is a synonym, return the correct name if it's a synonym
        if word not in cls.SYNONYMS:
            return word
        synonym_row = cls.SYNONYM_DF[cls.SYNONYM_DF["scientific_name"] == word]
        synonym_row = synonym_row.compute()
        if not synonym_row.empty:
            new_name = cls.lookup_symbol(synonym_row["Symbol"].iloc[0])
            if new_name is not None:
                return new_name
        return word

    @staticmethod
    def print_dict(dict):
        # Utility function to print the dictionary
        for k, v in dict.items():
            print(f"{k}. {v}")

    @classmethod
    def spell_check_list(cls, species_list, count=3):
        # Main spell-checking function
        new_list = []
        if species_list is None:
            return new_list

        for word in species_list:
            # Word found in the mega USDA list
            if word in cls.ALL_SPECIES:  # We compute the Dask DataFrame for this check
                checked_word = cls.check_synonym(word)
                if checked_word != word:
                    accept_synonym = y_n(
                        f"\n{word} is a synonym! Would you like to use the new name: {checked_word}? (y/n): ")
                    if accept_synonym:
                        new_list.append(checked_word)
                    else:
                        new_list.append(word)
                else:
                    new_list.append(checked_word)
            # Word not in mega USDA list (spelt wrong)
            else:
                word_dict = cls.spell(word, count)  # Call the spell method for Levenshtein distance
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


if __name__ == "__main__":
    test = ["achila millyfoluim", "taxus brevinfolium", "rubuss parvinflorum"]
    test_result = SpellCheck.spell_check_list(test, 5)
    print(test_result)