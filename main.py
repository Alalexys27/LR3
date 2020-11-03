import ast
import random
import json 
import os
import math
import sys
import pandas
from abc import ABC, abstractmethod

class AbstractClass(ABC):

    @abstractmethod
    def encrypt(self, **args):
        raise Exception("Данный метод переопределяется в дочернем классе.\
             Его логика уникальная для каждого отдельного класса.")

    @abstractmethod
    def decrypt(self, **args):
        raise Exception("Данный метод переопределяется в дочернем классе.\
             Его логика уникальная для каждого отдельного класса.")

    @abstractmethod
    def gen(self, **args):
        raise Exception("Данный метод переопределяется в дочернем классе.\
             Его логика уникальная для каждого отдельного класса.")

    def _create_file(self, fname: str, dic):
        output = json.dumps(dic)
        f = open(fname,'w')
        f.write(output)
        f.close()
    
    def _open_file_dec(self, inp_way_decrypt: str):
        f = open(inp_way_decrypt,'r')
        content=f.read()
        dic=ast.literal_eval(content)
        f.close()
        return dic

class Zam(AbstractClass):
    def __init__(self):
        self.Name_method="ZAM"

    def gen(self):
        # 1) Пользователь указывает файл алфавита;
        inp_way_alphabet=str(input("\n ---Введите путь к файлу (алфавит): "))
        # 2) Программа генерирует ключ по алфавиту(если алфавит не подходит для генерации ключа - сообщаете об этом пользователю); 
        try:
            file=open(inp_way_alphabet, "r")
            content=file.read()
            dic=ast.literal_eval(content)
            file.close()
            #print(dic)
            for value in dic.values():   # получение значений
                m1=value
            m2=m1.copy()
            random.shuffle(m2)
            #print(m1,"\n",m2)
            list1 = [0] * len(m1)
            for i in range(len(m1)):
                list1[i]=[m1[i],m2[i]]
            #print(list1)
            dic_key={"alg_type": self.Name_method,"key":list1}
            #print(dic_key)
            # 3) Пользователь указывает имя файла ключа;
            inp_name_key=input("\n ---Введите имя файла ключа: ")
            # 4) Программа сохраняет ключ в отдельном файле с именем, указанным пользователем.
            fname=inp_name_key+".key"
            self._create_file(fname, dic_key)
            print(">> Сгенерирован ключ (метод замены)") 
        except:
            print("Файл не существует!")

    def encrypt(self,inp_way_encrypt,inp_way_key_en):
        text_en=""
        f = open(inp_way_encrypt,'r')
        for line in f:
            text_en=text_en+line.rstrip('\n')+" "
        text_en=text_en[:-1]
        f.close()
        # print(text_en)
        # 4) Программа зашифровывает текст;
        t1=list()
        t1 = [0]*len(text_en)
        file=open(inp_way_key_en, "r")
        content=file.read()
        dic_key=ast.literal_eval(content)
        file.close()
        if dic_key['alg_type']==self.Name_method:
            m_k=dic_key['key']
            fl1=0
            fl2=0
            for j in range(len(text_en)):
                for i in range(len(m_k)):
                    if text_en[j]==m_k[i][0]:
                        t1[j]=m_k[i][1]
                        fl1=0
                        break
                    else:
                        fl1=1
                if fl1==1:
                    fl2=fl2+1
            if fl2==0:
                text_en=''.join([str(elem) for elem in t1])
                # print(text_en)
                # 5) Программа сохраняет результат в отдельном файле( к текущему имени файла добавляется расширение .encrypt). 
                dic_en={"alg_type": self.Name_method,"text":text_en}
                fname = inp_way_encrypt + ".encrypt"
                self._create_file(fname, dic_en)
                print(">> Текст зашифрован методом замены")
            else:
                print(">> Текст содержит неизвестные символы!")
        else:
            print(">> Неверый ключ!")

    def decrypt(self,inp_way_decrypt,inp_way_key_de):
        dic = self._open_file_dec(inp_way_decrypt)
        if dic['alg_type']==self.Name_method:
            text_de=dic['text']
            t1=list()
            t1 = [0]*len(text_de)
            file=open(inp_way_key_de, "r")
            content=file.read()
            dic_key=ast.literal_eval(content)
            file.close()
            if dic_key['alg_type']==self.Name_method:
                m_k=dic_key['key']
                fl1=0
                fl2=0
                for j in range(len(text_de)):
                    for i in range(len(m_k)):
                        if text_de[j]==m_k[i][1]:
                            t1[j]=m_k[i][0]
                            fl1=0
                            break
                        else:
                            fl1=1
                    if fl1==1:
                        fl2=fl2+1
                if fl2==0:
                    text_de=''.join([str(elem) for elem in t1])
                    dic_de={"alg_type": self.Name_method,"text":text_de}
                    fname = inp_way_decrypt + ".decrypt"
                    self._create_file(fname, dic_de)
                    print(">> Текст расшифрован методом замены") 
                else:
                    print(">> Неверный ключ!")
            else:
                print(">> Неверный ключ!") 
        else:
            print(">> Неверный метод для данного файла!")  

class Per(AbstractClass):
    def __init__(self):
        self.Name_method="PER"
    
    def gen(self):
        inp_way_alphabet=str(input("\n ---Введите путь к файлу (алфавит): "))
        try:
            file=open(inp_way_alphabet, "r")
            content=file.read()
            dic_alph=ast.literal_eval(content)
            file.close()
            #print(dic)
            for value in dic_alph.values():   # получение значений
                alph=value
            # 1) Пользователь указывает длину юлока перестановки;
            inp_lenth=int(input("\n ---Укажите длину блока перестановки: "))
            # 2) Программа генерирует ключ указанного размера;
            key=inp_lenth
            dic_key={"alg_type": self.Name_method,"key":key, "alph": alph}
            # 3) Пользователь указывает имя файла ключа;
            inp_name_key=input("\n ---Введите имя файла ключа: ")
            # 4) Программа сохраняет ключ в отдельном файле с именем, указанным пользователем.
            fname=inp_name_key+".key"
            self._create_file(fname, dic_key)
            print(">> Сгенерирован ключ (метод перестанвки)") 
        except:
            print("Введено неверное значение")

    def encrypt(self,inp_way_encrypt,inp_way_key_en):
        text_en=""
        f = open(inp_way_encrypt,'r')
        for line in f:
            text_en=text_en+line.rstrip('\n')+" "
        text_en=text_en[:-1]
        f.close()
        #print(text_en)
        file=open(inp_way_key_en, "r")
        content=file.read()
        dic_key=ast.literal_eval(content)
        file.close()
        i=0
        if dic_key['alg_type']==self.Name_method:
            k=int(dic_key['key'])
            d = {x+1:'' for x in range(k)}
            for i in [text_en[0+x:k+x] for x in range(0, len(text_en), k)]:
                c = 1
                for j in i:
                    d[c] += j
                    c += 1
            #print(d)
            text_en=''.join([x for x in d.values()])
            dic_en={"alg_type": self.Name_method,"text":text_en}
            fname = inp_way_encrypt + ".encrypt"
            self._create_file(fname, dic_en)
            print(">> Текст зашифрован методом перестановки") 
        else:           
            print(">> Неверный ключ!")

    def decrypt(self,inp_way_decrypt,inp_way_key_de):
        dic = self._open_file_dec(inp_way_decrypt)
        if dic['alg_type']==self.Name_method:
            s=dic['text']
            file=open(inp_way_key_de, "r")
            content=file.read()
            dic_key=ast.literal_eval(content)
            file.close()
            if dic_key['alg_type']==self.Name_method:
                k=dic_key['key']
                d = {x+1:'' for x in range(k)}
                c=0
                v=1
                h=(len(s)-(len(s)//k)*k)
                while(v<=h):
                    for j in range((len(s)//k)+1): 
                        d[v] += s[j+c]
                    c +=(len(s)//k)+1
                    v +=1
                while(v<k+1):
                    for j in range((len(s)//k)):
                        d[v] += s[j+c]
                    c +=(len(s)//k)
                    v +=1
                x = []
                c=0
                while(c<(len(s)//k)):
                    for j in d.values():
                        x.append(j[c])
                    c+=1
                for i in range(h):
                    x.append(d[i+1][-1])

                text_de=''.join(x)
                dic_de={"alg_type": self.Name_method,"text":text_de}
                fname = inp_way_decrypt + ".decrypt"
                self._create_file(fname, dic_de)
                print(">> Текст расшифрован методом перестановки")
            else:
                print(">> Неверный ключ!") 
        else:
            print(">> Неверный метод для данного файла!") 

# Доделать !!!

class Gam(AbstractClass):
    def __init__(self):
        self.Name_method="GAM"

    def gen(self):
        inp_way_alphabet=str(input("\n ---Введите путь к файлу (алфавит): "))
        try:
            file=open(inp_way_alphabet, "r")
            content=file.read()
            dic_alph=ast.literal_eval(content)
            file.close()
            #print(dic)
            for value in dic_alph.values():   # получение значений
                alph=value
            # 2) Пользователь указывает длинну гаммы (N);
            inp_lenth=int(input("\n ---Укажите длину гаммы: "))
            # 2) Программа генерирует ключ указанного размера;
            key=[0]*inp_lenth
            for i in range(inp_lenth):
                key[i]=random.randrange(0,len(alph),1)
            dic_key={"alg_type": self.Name_method,"key":key, "alph": alph}
            # 3) Пользователь указывает имя файла ключа;
            inp_name_key=input("\n ---Введите имя файла ключа: ")
            # 4) Программа сохраняет ключ в отдельном файле с именем, указанным пользователем.
            fname=inp_name_key+".key"
            self._create_file(fname, dic_key)
            print(">> Сгенерирован ключ (метод гаммирования)") 
        except:
            print("Введено неверное значение")

    def encrypt(self,inp_way_encrypt,inp_way_key_en):
        text_en=""
        f = open(inp_way_encrypt,'r')
        for line in f:
            text_en=text_en+line.rstrip('\n')+" "
        text_en=text_en[:-1]
        f.close()

        dic_k = self._open_file_dec(inp_way_key_en)
        if dic_k['alg_type']==self.Name_method:
            alph = dic_k['alph']
            len_text = len(text_en)
            len_alph = len(alph)
            key_list = dic_k['key']

            keyText = []
            gamma = []
            for i in range(len(key_list)):
                keyText.append(alph[int(key_list[i])])
            key_len = len(keyText)
            
            for i in range(len(keyText)):
                gamma.append(keyText[i])
            
            for i in range(len_text // key_len):
                for symb in gamma:
                    keyText.append(symb)
            for i in range(len_text % key_len):
                keyText.append(keyText[i])
    
            encrypt_text = ''
            for i in range(len_text):
                a = text_en[i]
                b = keyText[i]
                a_i = int(alph.index(a))
                b_i = int(alph.index(b))
                ab_sum = a_i + b_i
                ab_final = ab_sum % len_alph
                encrypt_text+=alph[ab_final]
            
            dic_en={"alg_type": self.Name_method,"text":encrypt_text}
            fname = inp_way_encrypt + ".encrypt"
            self._create_file(fname, dic_en)
            
            print(">> Текст зашифрован методом гаммирования") 
        else:
            print(">> Неверный ключ!")

    def decrypt(self,inp_way_decrypt,inp_way_key_de):
        dic = self._open_file_dec(inp_way_decrypt)
        if dic['alg_type']==self.Name_method:
            de_text=dic['text']
            file=open(inp_way_key_de, "r")
            content=file.read()
            dic_key=ast.literal_eval(content)
            file.close()
            if dic_key['alg_type']==self.Name_method:
       
                dic_k = self._open_file_dec(inp_way_key_de)
                alph = dic_k['alph']
                len_text = len(de_text)
                len_alph = len(alph)
                key_list = dic_k['key']

                keyText = []
                gamma = []
                for i in range(len(key_list)):
                    keyText.append(alph[int(key_list[i])])
                key_len = len(keyText)
                
                for i in range(len(keyText)):
                    gamma.append(keyText[i])
                
                for i in range(len_text // key_len):
                    for symb in gamma:
                        keyText.append(symb)
                for i in range(len_text % key_len):
                    keyText.append(keyText[i])
        
                decrypt_text = ''
                for i in range(len_text):
                    a = de_text[i]
                    b = keyText[i]
                    a_i = int(alph.index(a))
                    b_i = int(alph.index(b))
                    ab_sum = a_i - b_i
                    ab_final = ab_sum % len_alph
                    decrypt_text+=alph[ab_final]

                dic_de={"alg_type": self.Name_method,"text":decrypt_text}
                fname = inp_way_decrypt + ".decrypt"
                self._create_file(fname, dic_de)
                print(">> Текст расшифрован методом гаммирования") 
            else:
                print(">> Неверный ключ!") 
        else:
            print(">> Неверный метод для данного файла!") 

        

#--------------

def Encrypt():
    # 1) Пользователь выбирает метод шифровки;
    print("\n_________________________\nМетод шифровки:\n_________________________")
    print(" --- 1) Замена \n --- 2) Перестановка \n --- 3) Гаммирование")
    inp_method_en=input("Введите соответствующую цифру: ")
    try:
        inp_method_en=int(inp_method_en)
        if 1 <= inp_method_en <= 3:
            # 2) Пользователь выбирает файл текста;
            inp_way_encrypt=input("\n ---Введите путь к файлу (текст): ")
            try: 
                # 3) Пользователь выбирает файл ключа(осуществляется проверка на наличия расширения .key, проверка на соответствие ключа методу шифрования);
                inp_way_key_en=str(input("\n ---Введите путь к файлу (ключ): "))
                if inp_way_key_en.split('.')[-1] == 'key':
                    if inp_method_en == 1:
                        En1=Zam()
                        En1.encrypt(inp_way_encrypt,inp_way_key_en)
                    if inp_method_en == 2:
                        En2=Per()
                        En2.encrypt(inp_way_encrypt,inp_way_key_en)
                    if inp_method_en == 3:
                        En3=Gam()
                        En3.encrypt(inp_way_encrypt,inp_way_key_en)
                else: 
                    print(">> Неверный формат файла!") 
            except:
                print(">> Файл не найден!")
        else:
            print(">> Введено неверное число!")
    except:
        print(">> Введено неверное значение при выборе метода шифрования!")

def Decrypt():
    # 1) Пользователь выбирает метод расшифровки;
    print("\n_________________________\nМетод расшифровки:\n_________________________")
    print(" --- 1) Замена \n --- 2) Перестановка \n --- 3) Гаммирование")
    inp_method_de=input("Введите соответствующую цифру: ")
    try:
        inp_method_de=int(inp_method_de)
        if 1 <= inp_method_de <= 3:
            # 2) Пользователь выбирает файл шифротекст(осуществляется проверка на наличия расширения .encrypt); 
            inp_way_decrypt=input("\n ---Введите путь к файлу (текст): ")
            if inp_way_decrypt.split('.')[-1] == 'encrypt':
                # 3) Пользователь выбирает файл ключа(осуществляется проверка на наличия расширения .key, проверка на соответствие ключа методу шифрования);
                inp_way_key_de=input("\n ---Введите путь к файлу (ключ): ")
                if inp_way_key_de.split('.')[-1] == 'key':
                    # 4) Программа расшифровывает шифротекст;
                    if inp_method_de==1:
                        De1=Zam()
                        De1.decrypt(inp_way_decrypt,inp_way_key_de)
                    if inp_method_de==2:
                        De2=Per()
                        De2.decrypt(inp_way_decrypt,inp_way_key_de)
                    if inp_method_de==3:
                        De3=Gam()
                        De3.decrypt(inp_way_decrypt,inp_way_key_de)
                else:
                    print(">> Неверный формат файла ключа!") 
            else:
                print(">> Неверный формат файла с текстом!") 
        else:
            print(">> Введено неверное число!")
    except:
        print(">> Введено неверное значение при выборе метода расшифровки!")

def En_De():
    print("\n_________________________\nЗашифровать/Расшифровать\n_________________________")
    print(" --- 1) Зашифровать \n --- 2) Расшифровать ")
    inp_de_en=input("Введите соответствующую цифру: ")
    try:
        inp_de_en=int(inp_de_en)  
        if 1 <= inp_de_en <= 2:
            if inp_de_en == 1:
                Encrypt()
            if inp_de_en == 2:
                Decrypt()     
        else:
            print(">> Введено неверное число!")
    except:
        print(">> Введено неверное значение при выборе (зашифровать/расшифровать)!")

def Generate():
    print("\n____________________\nСгенерировать ключ\n____________________")
    print(" --- 1) Для метода замены \n --- 2) Для метода перестанвки \n --- 3) Для метода гаммирования")
    inp_key_method=input("Введите соответствующую цифру: ")
    try:
        inp_key_method=int(inp_key_method) 
        if 1 <= inp_key_method <= 3:
            if inp_key_method == 1:
                Gen1=Zam()
                Gen1.gen()
            if inp_key_method == 2:
                Gen2=Per()
                Gen2.gen()
            if inp_key_method == 3:
                Gen3=Gam()
                Gen3.gen()
        else:
            print(">> Введено неверное число!") 
    except:
        print(">> Введено неверное значение при выборе метода генерации ключа!")

def func():
    print("\n\nГлавное меню: \n --- 1) Зашифровать/Расшифровать \n --- 2) Сгенерировать ключ ")
    inp=input("Введите соответствующую цифру: ")
    try:
        inp=int(inp)
        if 1 <= inp <= 2:
            if inp == 1:
                En_De()
            if inp == 2:
                Generate()   
        else:
            print(">> Введено неверное число!")
    except:
        print(">> Введено неверное значение при выборе действия в главном меню!")

if __name__ == "__main__":
    func()