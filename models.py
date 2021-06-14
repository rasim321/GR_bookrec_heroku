from urllib.request import urlopen
import bs4
from googlesearch import search
from time import time 
import pandas as pd

book_df = pd.read_csv('data/books719.csv')
import numpy as np
simsort = np.load('data/simsort.npy')


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
  titles = df["title"][sorted_list[idx_num][0][-2:-(num_books+2):-1]].values
  return book_df.loc[book_df["title"].isin(titles),["title", "author", "avg_rate", "plot_summary"]]

def BookLinks(query):
  """
    Take a list of book titles and returns an array of links.

    :param p1: List of book titles
    :return: Array of book links from GoodReads
  """ 

  #Empty list to store links
  links = []

  #Search each search query
  for q in query:
    # print(q)

    #Specify search feature in goodreads.com
    url = ' site: goodreads.com'

    #Add the search query to the search term
    search_q = str(q) + url
    print(search_q)

    #Get the goodreads link 
    gdrd_l = search(search_q, tld="com", num=1, stop=1, pause=2)
    print(gdrd_l)

    #Append to list
    for i in gdrd_l:
      links.append(i)
    
    links[0] = links[0].replace("https://www.goodreads.com", "")
    title = book_df.loc[book_df["link"] == links[0], "title"]
  
  #Return the list
  return title.values[0]

def BookDetails(links, title_data=False, author_data=False, ratings_data = False):
  """
    Takes links tobook titles and returns a dataframe of information about each 
    book.

    :param p1: GoodReads links to the book
    :param p2: title_data = True if title data is needed
    :param p3: author_data = True if author data is needed
    :param p4: ratings_data = True if ratings data is needed
    :return: Dataframe of information for each book: title, author, avg rating, 
    number of ratings, plot summary, tags, and number of reviews
  """ 

  url = 'https://www.goodreads.com/'

  #Additonal Details
  title_df = []
  author_df = []
  avg_rating_df = []
  ratings_num_df = []

  #Regular details
  plot_df = []
  book_all_tags = []
  n_reviews = []
  count = 0

  for link in links:
  
    #check if link is the full url or just book link
    if "goodreads" in link:
      book_page = urlopen(link)
    else:
      book_page = urlopen(url + link)

    #Create the BS object
    soup = bs4.BeautifulSoup(book_page, "html.parser")
    count += 1

    #Check if title data is required
    if title_data == True:
      title = soup.select('#bookTitle')
      for j in title:
        title_df.append(j.text.strip())
    else:
      pass
    
    #Check if author data is required
    if author_data == True:
      author = soup.find("span", itemprop="name").text
      author_df.append(author)
    else:
      pass
    
    #Check if ratings data is required
    if ratings_data == True:
      rating = soup.find("span", itemprop="ratingValue")
      for l in rating:
        avg_rating_df.append(float(l.strip()))
      
      ratings_num = soup.find("meta", itemprop="ratingCount").get('content')
      ratings_num_df.append(ratings_num)
    else:
      pass


    #Get plot summaries
    plots = soup.select('#description span')
    if len(plots) > 1:
      summary = []

      for plot in plots:
        summary.append(plot.text)
      
      plot_df.append(summary[1])
        
    else:
      for plot in plots:
        plot_df.append(plot.text)



    #Get book tags
    book_tags = []

    tags = soup.select('.bookPageGenreLink')
    for tag in tags:
      book_tags.append(tag.text)

    book_tags = [x for x in book_tags if not any(c.isdigit() for c in x)]
    book_all_tags.append(book_tags)
    time.sleep(1)
    print("Book: " + str(count) +  " out of " + str(len(links)))


    #Get Number of Reviews:
    n_review = soup.find("meta", itemprop="reviewCount").get('content')
    n_reviews.append(n_review)
  
  if title_data==False:
    title_df = [None] * len(links)
  if author_data==False:
    author_df = [None] * len(links)
  if ratings_data==False:
    avg_rating_df = [None] * len(links)
    ratings_num_df = [None] * len(links)
    
  book_df = pd.DataFrame({
      'title': title_df,
      'author': author_df,
      "avg_rate": avg_rating_df,
      "number_of_ratings": ratings_num_df,
      "plot_summary": plot_df,
      "tags": book_all_tags,
      "reviews": n_reviews
  })
  return book_df

if __name__ == "__main__":
  print(similar_books("Great Expectations", book_df, 3, simsort))
  