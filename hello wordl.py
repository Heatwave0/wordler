from pprint import pprint
import string

def score_word(guess, word):
  score = ["⬛", "⬛", "⬛", "⬛", "⬛"]
  ignoreList = {}
  for ltr in string.ascii_lowercase:
    ignoreList.update({ltr:[]})
    
  for index in range(5):

    if guess[index] == word[index]:
      score[index] = "🟩"
      ignoreList[guess[index]] += [index]

    elif not any(z in ignoreList[guess[index]] for z in list(range(5))) and guess[index] in [x for i,x in enumerate(word) if i not in ignoreList[guess[index]]]:
      score[index] = "🟨"
      ignoreList[guess[index]] += [word.index(guess[index])]

  return ''.join(score)

 
with open("fiveLetters.txt") as wordList:
  temp = wordList.read().strip()
  words = sorted(list(temp.split(",")))

gameHistory = []
letterResults = {
  '0' : [],
  '1' : [],
  '2' : []
}

def greyCheck(grey, guess):
  a = []
  
  for i in range(len(grey)):
    if not any(z in ignoreYellow[grey[i]] for z in list(range(5))) and grey[i] in [x for y,x in enumerate(guess) if y not in ignoreGreen[grey[i]]]:
      a.append(True)
    else:
      a.append(False)
    
  return not any(a)


def greenCheck(green, greenPos, guess):
  a = [] 
  for i in range(len(green)):
    if green[i] == guess[greenPos[i]]:
      a.append(True)
      ignoreGreen[green[i]] += [greenPos[i]]
    else:
      a.append(False)

  return(all(a))
  

def yellowCheck(yellow, yellowPos, guess):
  a = []
  for i in range(len(yellow)):
    if yellow[i] in [x for y,x in enumerate(guess) if y not in ignoreYellow[yellow[i]]] and guess[yellowPos[i]] != yellow[i]:
      a.append(True)
      ignoreYellow[yellow[i]] += [yellowPos[i]]
    else:
      a.append(False)

  return(all(a))

ignoreGreen = {}
ignoreYellow = {}


while True:
  newWords = []
  
  while True:
    getWord = input("enter word: ")
    if getWord in words:
      break
    
    print('stupid ass bitch')
  while True:
    getResult = input("enter result as number (eg 00120 where 0 = grey, 1 = yellow, 2 = green: ")
    if getResult.isdecimal():
      break
    
    print('stupid ass')

  gameHistory.append([getWord, getResult])

  for i in range(5):
    if getResult[i] == '0':
      letterResults[getResult[i]] += getWord[i]
    else:
      letterResults[getResult[i]] += [[getWord[i], i]]

  
  
  for word in words:
    
    for ltr in string.ascii_lowercase:
      ignoreGreen.update({ltr:[]})
      ignoreYellow.update({ltr:[]})
      
    colourChecks = [
      greenCheck([i[0] for i in letterResults.get('2')], [i[1] for i in letterResults.get('2')], word),
      yellowCheck([i[0] for i in letterResults.get('1')], [i[1] for i in letterResults.get('1')], word),
      greyCheck(letterResults.get('0'), word)
    ]

    if all(colourChecks): newWords.append(word)

    
    
  print(newWords)
  print(len(newWords), "words remaining")

  if len(newWords) == 1:
    print("The word is", newWords[0])
    break

  else:

    # 0 - grey  1 - yellow  2 - green
    final = []

    # current word to "guess"
    for currentWord in words:
      score = "⬛⬛⬛⬛⬛"
      permuatations = {}

      # compare against every other word
      for word in newWords:

        # get the score of the word, add that to the counter
        score = score_word(currentWord, word)

        try:
          permuatations[score] += 1

        except KeyError:
          permuatations.update({score : 1})


      # dumb sort stuff


      permuatations = dict(sorted(permuatations.items(),key=lambda item: item[1], reverse=True))
      max_key = max(permuatations, key=permuatations.get)
      all_values = permuatations.values()
      max_value = max(all_values)
      a = [currentWord, max_value, max_key]
      # weight preference to words in newWords
      if a[0] in newWords:
        a[1] -= 0.01
      final.append(a)


      if len(final) % 100 == 0:
        print(len(final)//100, "/ 130  ", end="\r", flush=True)

    # output to file
    fileName = ', '.join([str(item) for item in gameHistory])
    open(fileName + ".txt", "x")
    final = sorted(final, key=lambda item: item[1])
    with open(fileName + ".txt", "w", encoding="UTF-8") as file:
      for item in final:
        file.write(f"Word: {item[0]}, Count: {item[1]}, Score: {item[2]}\n")
    print(final[0])
print("Done!          !!") 
