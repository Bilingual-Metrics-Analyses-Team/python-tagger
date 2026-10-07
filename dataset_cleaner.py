import pandas as pd
import re
import emoji # This needs to be installed in the environment

# Reads the TikTok comments file
df = pd.read_csv("nosabocomments.csv", delimiter=',')
#print(df)
#print(df.columns)
#print(len(df)) 

comment_column = "text"

def remove_emojis_only(comment):
    comment_without_emojis = emoji.replace_emoji(comment, replace="") # Removes emojis from the comment
    comment_without_emojis = comment_without_emojis.strip() # Removes spaces left behind
    return comment_without_emojis == "" # Returns True if nothing remains, that is, if the comment was just a string of emojis

def remove_username_only(comment):
    comment = comment.strip() # Removes white spaces before and after the comment
    new_comment = []
    for word in comment.split(): # Goes over each word in the comment
        if not word.startswith("@"): # Keeps the word if it is not a username, that is, if it does not start with @
            new_comment.append(word)
    return " ".join(new_comment) # Joins the remaining words back into a comment and returns them
    
# This is because the previous function leaves text with emojis too 
def remove_emojis(comment): 
    comment = emoji.replace_emoji(comment, replace="") # Removes emojis but keeps the text
    comment = " ".join(comment.split()) # Removes extra spaces left behind by the emojis
    return comment

# Now I start calling the functions
rows_to_remove = []

# Goes over each comment in the text column
for index, comment in df[comment_column].items():
    if remove_emojis_only(comment): # If the function returns True
        rows_to_remove.append(index) # We add it to the list of comments to remove

#print(df.loc[rows_to_remove, comment_column]) # This is a check to make sure just comments with emojis are being removed

df = df.drop(rows_to_remove) # Removes the complete rows if they are emoji only
df = df.reset_index(drop=True) # Resets the row numbers

print("Rows removed:", len(rows_to_remove)) # 13382
print("Rows remaining:", len(df)) # 112197 

# Now we remove emojis from comments that also have text
df[comment_column] = df[comment_column].apply(remove_emojis)

print("Rows removed:", len(rows_to_remove)) 
print("Rows remaining:", len(df))

# Now we start working on the username comments, they have the at in front of the names
df[comment_column] = df[comment_column].apply(remove_username_only)
print(df[comment_column].head(50))
df = df[df[comment_column] != ""].reset_index(drop=True)  # Removes rows that no longer contain any text

print("Final number of rows in the dataset:", len(df))

# Saves thenew  cleaned dataset
df.to_csv("nosabocomments_cleaned.csv", index=False)
