def anagrams(phrase, shortest=2):
    """Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words 
    have length >= shortest. Phrases in answer must have words in 
    lexicographic order (not all permutations)."""
    # your code here
    results=set()
    phrase=phrase.replace(' ','')
    helper(phrase,shortest,results)
    return results
    
def helper(letters,shortest,results,this_result=[]):
    if len(letters)==0:
        results.add(' '.join(entry for entry in sorted(this_result)))
        return
    elif len(letters)<shortest:
        return
    else:
        words=find_words(letters)
        for word in words:
            if len(word)>=shortest:
                this_result.append(word)
                helper(removed(letters,word),shortest,results,this_result)
                this_result.pop()
