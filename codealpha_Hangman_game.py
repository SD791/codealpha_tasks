import random

words = ["hangman", "python", "challenge", "programming", "developer"]a

def get_random_word():
    return random.choice(words)

def display_state(word, guessed_letters, incorrect_guesses):
    print("Word:", " ".join([letter if letter in guessed_letters else "_" for letter in word]))
    print("Incorrect guesses:", incorrect_guesses)

def play_hangman():
    print("Welcome to Hangman!")
    word = get_random_word()
    guessed_letters = set()
    incorrect_guesses = 0
    max_incorrect_guesses = 6
    
    while incorrect_guesses < max_incorrect_guesses:
        display_state(word, guessed_letters, incorrect_guesses)
        guess = input("Guess a letter: ").lower()
        
        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue
        
        guessed_letters.add(guess)
        
        if guess in word:
            print(f"Good guess! The letter '{guess}' is in the word.")
        else:
            incorrect_guesses += 1
            print("Wrong guess!")
        
        if all(letter in guessed_letters for letter in word):
            print("Congratulations! You guessed the word:", word)
            return
    
    print("Game over! The word was:", word)


play_hangman()
