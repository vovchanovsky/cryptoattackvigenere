# -*- coding: cp1251 -*-
from collections import Counter
from random import randint
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
freqalphabet = "оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъ"

def fread(filename):
    file = open(filename)
    text = file.read()
    file.close()
    return text

def clear_text():
    string = fread('text.txt').lower().replace('ё','е')
    for i in string:
        if not(i in alphabet):
            string = string.replace(i, '')
    clear_file = open('clear_text.txt', 'w')
    clear_file.write(string)
    clear_file.close()
    print('Text cleaned and saved successfully.')

clear_text()

def encodeVG(text, key):
    ciphertext=''
    j=0
    for letter in text:
        j%=len(key)
        ciphertext+=alphabet[(alphabet.find(letter)+alphabet.find(key[j]))%len(alphabet)]
        j+=1
    print_index(ciphertext, len(key))

def count_index(ciphertext):
    index=0
    for letter in alphabet:
        d=ciphertext.count(letter)*(ciphertext.count(letter)-1)/float(len(ciphertext)*(len(ciphertext)-1))
        index+=d
    return index
    
def print_index(ciphertext, lenkey):
    index=str(lenkey)+' '+str(count_index(ciphertext))
    print index
    clear_file = open('index.txt', 'a')
    clear_file.write(index+'\n')
    clear_file.close()

def keygen(N):
    key=''
    for i in range(N):
        key+=alphabet[randint(0, len(alphabet)-1)]
    encodeVG(fread('clear_text.txt'), key)
    
def nearest(lst, target):
  return min(lst, key=lambda x: abs(x-target))

def attackVG(ciphertext):
    d = {}
    file = open('index.txt')
    line = file.readlines()
    normindex = line[0].split()[1]
    file.close()
    print 'For ciphertext'
    for r in range(1, 31):
        val = 0
        for i in range(r):
            val+=count_index(str(ciphertext[i::r]))
        val /= r
        d[val] = r
        print r, ' ',val
    while len(d) !=0:
        attackkeyVG(ciphertext, d.pop(nearest(d.keys(), float(normindex))))
        switch = raw_input('Do you want to change key length?(y/n)')
        if switch == 'n':
                  break
    while True:
        key=raw_input('key:')
        result=decodeVG(fread('unknown.txt'), key)
        print result
        switch = raw_input('Do you want to try again?(y/n)')
        if switch == 'n':
            clear_file = open(key+'.txt', 'w')
            clear_file.write(result)
            clear_file.close()
            break

def attackkeyVG(ciphertext, lenkey):
    print 'Key length:', lenkey
    keys=[]
    n=5
    
    for j in range(lenkey):
        keys.append('')
    for i in range(lenkey):
       mc=Counter(ciphertext[i::lenkey]).most_common(n)
       for j in range(n):
           keys[i]+=alphabet[(alphabet.find(mc[j][0])-alphabet.find(freqalphabet[0]))%len(alphabet)]
       print str(keys[i])[:3]

def decodeVG(ciphertext, key):
    text=''
    j=0
    for letter in ciphertext:
        j%=len(key)
        text+=alphabet[(alphabet.find(letter)-alphabet.find(key[j]))%len(alphabet)]
        j+=1
    return text
          
def start():
    open('index.txt', 'w').close()
    print_index(fread('clear_text.txt'), 0)
    for N in range(2, 6):
        keygen(N)
    for N in range(10, 21):
        keygen(N)
    attackVG(fread('unknown.txt'))

start()
