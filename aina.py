import romajitable
import pykakasi
import re
from pydub import AudioSegment
import os.path
from os import path, symlink
import wave

kks = pykakasi.kakasi()
wordList = []
L = lambda x:re.sub('[bghkmnpr]~([auoei]|y[auo])|[sz]~[auoe]|[dt]~[aeo]|w~[ao]|([fv]~|ts)u|(j~|[cs]h)(i|y[auo])|y~[auo]|[auoien]'.replace('~','{1,2}'),'',x)==''
i = 0
j = 1
p = 0

with open('test.txt', 'r') as f:
    lines = f.readlines()

    for line in lines: 
            romaji = romajitable.to_kana(line)
            hira = romaji.hiragana.replace("・", "")
            weeb = kks.convert(hira)
            romajiLines = []
            removedDuplicates = []
            
            for item in weeb:
                romajiLines.append(format(item['hepburn'])) #turn line of text into romaji
            
            for v in romajiLines:
                if v not in removedDuplicates:
                    print(v)
                    removedDuplicates.append(v) #remove duplicate lines made by 
            
            for item in removedDuplicates:
                split_strings = []
                n  = 2
                export_sounds = []
                combined_sounds = AudioSegment.empty()
                combined = AudioSegment.empty()

                for index in range(0, len(item), n):
                  test = item[index : index + n] #increment 2 syllables at a time 
                  print(index, test, L(test))
                  if (L(test) != True): #check if pair of chars is valid romaji, if not...
                      test = item[index : index + n - 1] #try the first char
                      if (L(test)): #if first char is valid romaji
                          print(index, test, L(test)) 
                          split_strings.append(test)  
                          test = item[index + 1: index + n + 1]
                          if (L(test)): #check if second char is start of new syllable, if it is...
                              print(index, test, L(test))
                              split_strings.append(test)  
                          else:  #check if initial 2 chars + next char make a valid syllable
                              test = item[index: index + n + 1]
                              if (L(test)):
                                  print(index, test, L(test))
                                  split_strings.append(test) 
                              else:
                                continue
                      else: #if valid romaji
                          split_strings.append(test)
                          print(index, test, L(test))
                  else: #if pair of chars if valid romaji...
                      print(test)
                      split_strings.append(test)     
                #   split_strings.append(item[index : index + n])
                #   print(index)
                #   exit()
             
               
                for syllable in split_strings:
                    syllable = 'C:/Users/Avery/Desktop/test/voice/' + syllable + '.wav'
                    if (os.path.isfile(syllable)):
                        sound = AudioSegment.from_wav(syllable)
                        export_sounds.append(sound)

                for fname in export_sounds:
                    combined += fname    

                if (i % 2) == 0:
                    print(j)
                    generatedFile = 'test/' + str(j) + '.wav'
                    combined.export(generatedFile, format='wav')    
                    j += 1
                
                i += 1

            