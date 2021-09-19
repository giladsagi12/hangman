#Gilad Sagi Fridman


import hangman_helper



def list_to_string(lst):
    """converts a given list to a string (returns string)"""
    string = ""
    for l in lst:
        string += l
    return string


def update_word_pattern(word, pattern, letter):
    """gets an input of a letter and returns the updated word pattern as a string"""
    pattern_list = list(pattern)
    word_list = list(word)
    for x in range(len(word_list)):
        if word_list[x] == letter:
            pattern_list[x] = letter
    return list_to_string(pattern_list)



def run_single_game(word_list, score):
    """
    :param word_list: a given list of words
    :param score: the score of the player
    lets the player choose between a guess of a word, a letter or a hint
    :return: the score of the player after the game
    """

    word = hangman_helper.get_random_word(word_list)
    pattern = "_" * len(word)
    wrong_guess_lst = []
    hangman_helper.display_state(pattern, wrong_guess_lst, score,
                                 "insert a letter, a word or ask for a hint")
    while pattern != word and score > 0:
        inpt = hangman_helper.get_input()
        if inpt[0] == hangman_helper.LETTER:
            score, pattern = choseLetter(inpt, score, word, wrong_guess_lst, pattern)
        elif inpt[0] == hangman_helper.WORD:
            score, pattern = choseWord(inpt, word, pattern, score)
            if pattern.count("_") != 0:
                hangman_helper.display_state(pattern, wrong_guess_lst, score,"no")
        else:
            score, filtered_word_lst = choseHint(score, word_list, pattern, wrong_guess_lst)
            hangman_helper.show_suggestions(filtered_word_lst)
    if pattern == word:
        hangman_helper.display_state(pattern,wrong_guess_lst,score,"w" )
    if score == 0:
        print("l, the word was " + word)
    return score


def choseHint(score, word_list, pattern, wrong_guess_lst):
    """reduces a point and returns the filtered list of words,
    by calling 'filter_words_list'"""
    score -= 1
    filtered_word_lst = filter_words_list(word_list, pattern, wrong_guess_lst)
    filtered_filtered_word_lst = []
    if len(filtered_word_lst) > hangman_helper.HINT_LENGTH:
        for h in range(hangman_helper.HINT_LENGTH):
            filtered_filtered_word_lst.append \
                (filtered_word_lst[(len(filtered_word_lst) * h) // hangman_helper.HINT_LENGTH])
        return score, filtered_filtered_word_lst
    return score, filtered_word_lst

def choseWord(inpt, word, pattern, score):
    """
    this function gets a guess of a word from the player
    and returns the updated score and the pattern of the word
    """
    if inpt[1] == word:
        score += pattern.count("_") * (pattern.count("_") + 1) // 2
        pattern = word
    else:
        score -= 1
    return score, pattern

def choseLetter(inpt, score, word, wrong_guess_lst, pattern):
    """this function gets a guess of a letter from the player, checks if
     the letter in the word and returns the updated score
    and the pattern of the word accordingly"""
    letter = inpt[1]
    if (len(letter) != 1 or not ord(letter) in range(97,122)
            or letter in wrong_guess_lst or letter in pattern):
        hangman_helper.display_state(pattern, wrong_guess_lst, score,
                                     "insert one lowercase letter. make sure you"
                                     "have not guessed this letter before")
        return score, pattern
    if letter in word:
        pattern = update_word_pattern(word, pattern, letter)
        n = pattern.count(letter)
        score += (n * (n + 1) // 2) - 1
        hangman_helper.display_state(pattern, wrong_guess_lst, score, "guessed correctly")
    else:
        score -= 1
        wrong_guess_lst.append(letter)
        hangman_helper.display_state(pattern, wrong_guess_lst, score, "incorrect")
    return score, pattern

def filter_words_list(words, pattern, wrong_guess_lst):
    """returns a list of possible words from the word list, regarding of
    the pattern and the wrong guesses"""
    filtered_words_list = []
    for word in words:
        if len(pattern) == len(word):
            word_correct = True
            for x in range(len(pattern)):
                if pattern[x] != "_":
                    if word[x] != pattern[x]:
                        word_correct = False
                if pattern[x] != "_":
                    if word.count(pattern[x]) != pattern.count(pattern[x]):
                            word_correct = False
                for l in wrong_guess_lst:
                    if word.count(l) != 0:
                        word_correct = False
            if word_correct:
                filtered_words_list.append(word)
    return filtered_words_list


def main():
    total_score = hangman_helper.POINTS_INITIAL
    total_score = run_single_game(hangman_helper.load_words(), total_score)
    count = 1
    while total_score > 0:
        if hangman_helper.play_again("Play again?"):
            total_score = run_single_game(hangman_helper.load_words(), total_score)
            count += 1
            print("u have played " + str(count) + " games")

        else:
            count += 1
            print("u have played " + str(count) + " games , and score = " + str(total_score))
            break
    if total_score == 0:
        if hangman_helper.play_again("Play new game set?"):
            print("U have played " + str(count) + " games")
            main()

if __name__ == "__main__":
    main()