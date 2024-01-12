import pandas as pd

# read the csv file
blog_corpus = pd.read_csv("blogtext.csv", nrows=10000)

# slice by age
blog_corpus = blog_corpus.loc[(blog_corpus["age"] > 22)]

# collect unique blog IDs
blog_id_set = set(blog_corpus["id"])

# initialise variables
loops = 0
files = 1

for blog_id in blog_id_set:
    #check how many loops have been done
    #there should be a new file every 25 blogs
    if loops == 25:
        loops = 0
        files += 1
        
    #write the text of each blog post to the current file
    filename = "blog" + str(files) + ".txt"
    blog = blog_corpus.loc[(blog_corpus["id"] == blog_id)]
    try: 
        blog["text"].to_csv(filename, sep=" ", mode="a", index=False)
    except Exception as e:
        print("Error writing file: ", e)
    
    #increment loops variable
    loops += 1

