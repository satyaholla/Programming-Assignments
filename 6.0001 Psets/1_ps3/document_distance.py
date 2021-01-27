# 6.0001 Spring 2020
# Problem Set 3
# Written by: sylvant, muneezap, charz, anabell, nhung, wang19k, asinelni, shahul, jcsands

# Problem Set 3
# Name: <insert name>
# Collaborators: <insert collaborators>
# Time Spent: <insert time>
# Late Days Used: (only if you are using any)

import string

# - - - - - - - - - -
# Check for similarity by comparing two texts to see how similar they are to each other


### Problem 1: Prep Data ###
# Make a *small* change to separate the data by whitespace rather than just tabs
def load_file(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        list of strings holding the file contents where
            each string was separated by a newline character (\t) in the file
    """
    inFile = open(filename, 'r')
    line = inFile.read()
    inFile.close()
    line = line.strip().lower()
    for char in string.punctuation:
        line = line.replace(char, "")
    return line.split()

### Problem 2: Find Ngrams ###
def find_ngrams(single_words, n):
    """
    Args:
        single_words: list of words in the text, in the order they appear in the text
            all words are made of lowercase characters
        n:            length of 'n-gram' window
    Returns:
        list of n-grams from input text list, or an empty list if n is not a valid value
    """
    l = len(single_words)
    if n > l or n < 1:
        return []
    return [' '.join(single_words[x:x+n]) for x in range(l-n+1)]
    

### Problem 3: Word Frequency ###
def compute_frequencies(words):
    """
    Args:
        words: list of words (or n-grams), all are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string
        is a word (or n-gram) in words and the corresponding int
        is the frequency of the word (or n-gram) in words
    """
    d = {}
    for ngram in words:
        if ngram in d:
            d[ngram] += 1
        else:
            d[ngram] = 1
    return d

### Problem 4: Similarity ###
def get_similarity_score(dict1, dict2, dissimilarity = False):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary of words or n-grams for one text
        dict2: frequency dictionary of words or n-grams for another text
        dissimilarity: Boolean, optional parameter. Default to False.
          If this is True, return the dissimilarity score, 100*(DIFF/ALL), instead.
    Returns:
        int, a percentage between 0 and 100, inclusive
        representing how similar the texts are to each other

        The difference in text frequencies = DIFF sums words
        from these three scenarios:
        * If a word or n-gram occurs in dict1 and dict2 then
          get the difference in frequencies
        * If a word or n-gram occurs only in dict1 then take the
          frequency from dict1
        * If a word or n-gram occurs only in dict2 then take the
          frequency from dict2
         The total frequencies = ALL is calculated by summing
         all frequencies in both dict1 and dict2.
        Return 100*(1-(DIFF/ALL)) rounded to the nearest whole number if dissimilarity
          is False, otherwise returns 100*(DIFF/ALL)
    """
    def sumValues(d):
        tot = 0
        for i in d.values():
            tot += i
        return tot
    all = sumValues(dict1) + sumValues(dict2)

    diffFreq = dict(dict1)
    for k in dict2:
        if k in diffFreq:
            diffFreq[k] = abs(diffFreq[k] - dict2[k])
        else:
            diffFreq[k] = dict2[k]
    diff = sumValues(diffFreq)
    
    disScore = int(100*(diff/all))
    if dissimilarity:
        return disScore
    else:
        return 100 - disScore

### Helper Function
def sortedListOfDictMax(dict1):
    words = []
    m = max(dict1.values())
    for k in dict1:
        if dict1[k] == m:
            words.append(k)
    words.sort()
    return words


### Problem 5: Most Frequent Word(s) ###
def compute_most_frequent(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary for one text
        dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) in the input dictionaries

    The most frequent word:
        * is based on the combined word frequencies across both dictionaries.
          If a word occurs in both dictionaries, consider the sum the
          freqencies as the combined word frequency.
        * need not be in both dictionaries, i.e it can be exclusively in
          dict1, dict2, or shared by dict1 and dict2.
    If multiple words are tied (i.e. share the same highest frequency),
    return an alphabetically ordered list of all these words.
    """
    totalFreq = dict(dict1)
    for k in dict2:
        if k in totalFreq:
            totalFreq[k] += dict2[k]
        else:
            totalFreq[k] = dict2[k]
    return sortedListOfDictMax(totalFreq)
        
### Problem 6: Finding closest artist ###
def find_closest_artist(artist_to_songfiles, mystery_lyrics, ngrams = 1):
    """
    Args:
        artist_to_songfiles:
            dictionary that maps string:list of strings
            where each string key is an artist name
            and the corresponding list is a list of filenames (including the extension),
            each holding lyrics to a song by that artist
        mystery_lyrics: list of single word strings
            Can be more than one or two words (can also be an empty list)
            assume each string is made of lowercase characters
        ngrams: int, optional parameter. Default set to False.
            If it is greater than 1, n-grams of text in files
            and n-grams of mystery_lyrics should be used in analysis, with n
            set to the value of the parameter ngrams
    Returns:
        list of artists (in alphabetical order) that best match the mystery lyrics
        (i.e. list of artists that share the highest average similarity score (to the nearest whole number))

    The best match is defined as the artist(s) whose songs have the highest average
    similarity score (after rounding) with the mystery lyrics
    If there is only one such artist, then this function should return a singleton list
    containing only that artist.
    However, if all artists have an average similarity score of zero with respect to the
    mystery_lyrics, then this function should return an empty list. When no artists
    are included in the artist_to_songfiles, this function returns an empty list.
    """
    meanFreq = {}
    mysteryDict = compute_frequencies(find_ngrams(mystery_lyrics, ngrams))
    for artist in artist_to_songfiles:
        cumulScore = 0
        for fileName in artist_to_songfiles[artist]:
            artistDict = compute_frequencies(find_ngrams(load_file(fileName), ngrams))
            cumulScore += get_similarity_score(mysteryDict, artistDict)
        meanFreq[artist] = int(cumulScore/len(artist_to_songfiles[artist]))
    
    if len(meanFreq) == 0:
        return []
    closest = sortedListOfDictMax(meanFreq)
    if meanFreq[closest[0]] != 0:
        return closest
    return []

if __name__ == "__main__":
    pass
    #Uncomment the following lines to test your implementation
    # Tests Problem 0: Prep Data
    test_directory = "tests/student_tests/"
    world, friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    print(world) ## should print ['hello', 'world', 'hello']
    print(friend) ## should print ['hello', 'friends']

    # Tests Problem 1: Find Ngrams
    world_ngrams, friend_ngrams = find_ngrams(world, 2), find_ngrams(friend, 2)
    longer_ngrams = find_ngrams(world+world, 3)
    print(world_ngrams) ## should print ['hello world', 'world hello']
    print(friend_ngrams) ## should print ['hello friends']
    print(longer_ngrams) ## should print ['hello world hello', 'world hello hello', 'hello hello world', 'hello world hello']

    # Tests Problem 2: Get frequency
    world_word_freq, world_ngram_freq = compute_frequencies(world), compute_frequencies(world_ngrams)
    friend_word_freq, friend_ngram_freq = compute_frequencies(friend), compute_frequencies(friend_ngrams)
    print(world_word_freq) ## should print {'hello': 2, 'world': 1}
    print(world_ngram_freq) ## should print {'hello world': 1, 'world hello': 1}
    print(friend_word_freq) ## should print {'hello': 1, 'friends': 1}
    print(friend_ngram_freq) ## should print {'hello friends': 1}

    # Tests Problem 3: Similarity
    word_similarity = get_similarity_score(world_word_freq, friend_word_freq)
    ngram_similarity = get_similarity_score(world_ngram_freq, friend_ngram_freq)
    print(word_similarity) ## should print 40
    print(ngram_similarity) ## should print 0

    # Tests Problem 4: Most Frequent Word(s)
    freq1, freq2 = {"hello":5, "world":1}, {"hello":1, "world":5}
    most_frequent = compute_most_frequent(freq1, freq2)
    print(most_frequent) ## should print ["hello", "world"]

    # Tests Problem 5: Find closest matching artist
    test_directory = "tests/student_tests/"
    artist_to_songfiles_map = {
    "artist_1": [test_directory + "artist_1/song_1.txt", test_directory + "artist_1/song_2.txt", test_directory + "artist_1/song_3.txt"],
    "artist_2": [test_directory + "artist_2/song_1.txt", test_directory + "artist_2/song_2.txt", test_directory + "artist_2/song_3.txt"],
    }
    mystery_lyrics = load_file(test_directory + "mystery_lyrics/mystery_1.txt") # change which number mystery lyrics (1-5)
    print(find_closest_artist(artist_to_songfiles_map, mystery_lyrics)) # should print ['artist_1']
