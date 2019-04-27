# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    MyWord = word.lower()
    MyScore=0
    First_element_score = 0
    for s in MyWord:
        First_element_score += SCRABBLE_LETTER_VALUES.get(s,0)  
        # getting the values correspoinding to keys defined in dictionary
        #get is used to avoid if no not difined char is pound
    
    Second_element_score = (HAND_SIZE*len(MyWord))-(3*(n-len(MyWord)))
    if Second_element_score > 0:
        MyScore= First_element_score*Second_element_score
    else:
        MyScore = First_element_score
        
    return MyScore
    #pass  # TO DO... Remove this line when you implement this function

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):# -1 to reduce by one to use wild card *
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    #y = "*"
    hand["*"] = hand.get("*",0)+1
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    given_word = word.lower()
    New_Hand = hand.copy()
    for s in given_word:
        if s in New_Hand:
            New_Hand[s] -= 1
            
            if New_Hand[s]<=0:
                del(New_Hand[s])

    return New_Hand
            

    #pass  # TO DO... Remove this line when you implement this function

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    valid_word_status = False
    myword = ""
    MyHand = hand.copy()
    New_word_list = list(word)
    locator = -1  #to Know where is the * in word given by user
    
    for i in range(len(New_word_list)):
        if New_word_list[i] == "*":
            locator = i
            break
    for j in VOWELS:
        if locator < 0:
            myword = (''.join(New_word_list)).lower()
            break
        New_word_list[locator] = j
        myword = (''.join(New_word_list)).lower()
        #print(myword)
        if myword in word_list:
            MyHand[j] = 1
            valid_word_status = True
            break
    #print(myword, "********")
    if myword in word_list:
        for s in myword:
            if s in MyHand:
                valid_word_status = True
                MyHand = update_hand(MyHand,s)
            else:
                valid_word_status = False
                break
    
    return valid_word_status

    #pass  # TO DO... Remove this line when you implement this function

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    # it was not possible to add values with simple mathematics so need this funftion
    Handlen = sum(hand.values())
    
    
    return Handlen
    
    #pass  # TO DO... Remove this line when you implement this function

def User_input():
    word = input('Enter Word , or "!!"to indicate you are finished : ')
    
    return word

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    MyHand = hand  #taking n = HAND Size
    Hand_length = calculate_handlen(MyHand)
    
    #print('Enter Word , or "!!"to indicate you are finished : ')
    MyScore = 0
    while(Hand_length > 0):
        # Display the hand
        word = ""
        #substitute_letter = ""
        #print("Current Hand : ", " ".join(MyHand.keys())) 
        print("Current Hand :", end= " ")
        display_hand(MyHand)
            
        # Ask user for input
        word = User_input()
        # If the input is two exclamation points:        
        if word == "!!":
            # End the game (break out of the loop)
            break
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word,MyHand,word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                points = get_word_score(word , HAND_SIZE)
                MyScore += points
                print(word,"earned ", points,"points. Total :", MyScore ,"points")  
            
            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("That is not a valid word please choose a valid word")
            # update the user's hand by removing the letters of their inputted word
            MyHand = update_hand(MyHand , word)
            Hand_length = calculate_handlen(MyHand)
            
    
    if Hand_length <= 0:
        print("Ran out of letters. Toatal Score ", MyScore)
    else:
        print("Toatal Score ", MyScore)
        
    
    return MyScore
        
        # If the input is two exclamation points:
         
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.
    
    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    is_letter_availble = True
    is_vowel = False
    x = ""
    letter_value = hand[letter]
    while is_letter_availble:
        # first check if given letter is vowel or consonant
        is_vowel = False
        for v in VOWELS:
            if v == letter:
                is_vowel = True
        
        # if vowel then take any random vowel else take any random cosonant
        if is_vowel:
            x = random.choice(VOWELS)
        else:
            x = random.choice(CONSONANTS)
            
        if x in hand:
            is_letter_availble = True
        else:
            is_letter_availble = False
            hand[x] = letter_value
            del(hand[letter])
        
    
    pass  # TO DO... Remove this line when you implement this function
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    Round = int(input("Enter the total no. of Hands you want to pley "))
    TotalScore = 0
    HandScore = 0
    for i in range(Round):
        Hand = deal_hand(HAND_SIZE)
        Substituted_once = False
        #display_hand(Hand)
        #print("Current Hand: ",)
        print("Current Hand :", end= " ")
        display_hand(Hand)
        
        # for substitution  of the letter once
        if Substituted_once == False:
            is_valid_inpt = False
            Want_substitution = input("Do you want to substitute any letter in hand (yes/no) : ").lower()
            if Want_substitution == "yes":
                while is_valid_inpt == False:
                    substitute_letter = input("please enter the letter you want to substitue : ").lower()
                    if substitute_letter in Hand:
                        is_valid_inpt = True
                        substitute_hand(Hand , substitute_letter)
                        Substituted_once = True
                
        Replay = True
        while Replay:
            HandScore = play_hand( Hand,word_list)
            print("Your Score for this hand is ", HandScore)
            # to terminate the loop
            play_again = input("Do you want to replay this hand (Yes/No) : ").lower()
            if play_again == "no":
                Replay = False
        
        TotalScore += HandScore
        print("Your Total score is ", TotalScore)
            
        
   
    
    #print(get_word_score("weed", 6))
   


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    #play_hand(deal_hand(HAND_SIZE),word_list)
    play_game(word_list)