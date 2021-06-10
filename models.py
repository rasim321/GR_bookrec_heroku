def similar_books(title, df, num_books, sorted_list):
  """
  Returns similar books to the book title provided.

  :param p1: Book Title
  :param p2: Dataframe of books to search from
  :param p3: Number of recommendations
  :param p4: The sorted list of books to search from
  :return: Return number of book recommendations equivalent to the num_books
  """

  idx_num = df[df["title"] == title].index.values
  return df["title"][sorted_list[idx_num][0][-2:-(num_books+2):-1]].values


# import pandas as pd
# import numpy as np

# book_df = pd.read_csv("data/books719.csv")
# simsort = np.load('data/simsort.npy')

# print(similar_books("Great Expectations", book_df, 2, simsort))