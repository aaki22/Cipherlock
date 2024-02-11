
import time

rem_count=[]
bin_chunks=[]
Str=''
mode=0
size=8

def text_to_binary_list(text):
    binary_list = [bin(ord(char))[2:].zfill(8) for char in text]
    return binary_list

def binary_data_to_8BIT(binary_data):
    binary_data_chunks = []

    for i in range(0, len(binary_data), 8):
        if binary_data[i] == '%':
            break
        else:
            binary_data_chunks.append(binary_data[i:i+8])
    return binary_data_chunks

def binary_to_text(Str):
    return chr(int(Str,2))


def xor_binary_strings(str1, str2):
    result = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(str1, str2))
    return result

def conv_64bit(binary_chunks,bin_list):
    
    outer_count=0
    inner_count=0
    
    for chunk in binary_chunks:

        if inner_count<8:
            bin_list[outer_count].append(chunk)
            inner_count=inner_count+1
            

        if inner_count >=8:
            inner_count=0
            outer_count+=1
            bin_list.append([])

    if (len(bin_list[-1])%2 != 0):
            bin_list[outer_count].append('00000000')


def negation_swap(str):

    ls=''.join('1' if bit=='0' else '0' for bit in str[4:]+str[:4])

    return ls
def count_checker(rem1):
    count=0
    for chunk in range(len(rem1)):
        for j in range(len(rem1[chunk])):
            count+=j
    return str(count)


def eny_write(rem1,rem2,Str_len,rem1_len,rem2_len):
   
    with open('eny-data.txt', 'w') as En_file:
        for chunk in range(len(rem1)):
            for j in range(len(rem1[chunk])):
                Str = ''.join(rem1[chunk][j])
                rem1_len+=len(Str)
                En_file.write(Str)

        for chunk in range(len(rem2)):
            for j in range(len(rem2[chunk])):
                Str = ''.join(rem2[chunk][j])
                rem2_len=len(Str)
                En_file.write(Str)
        
        if Str_len>=1:
            #En_file.write("%,"+str(len(rem2_len)[::-1]))
            En_file.write("%,"+str(rem1_len)[::-1]) 
                

def encryption(bin_list,Str_len,rem1_len,rem2_len,rem1,rem2):
    inner_count=0
    outer_count=1

    #cypher text-1
    for chunk in range(len(bin_list)):
        for j in range(int(len(bin_list[chunk]) / 2)):
            
            #print(inner_count,outer_count)
            if outer_count<8:
                rem1[chunk].append(''.join(xor_binary_strings(bin_list[chunk][inner_count],bin_list[chunk][outer_count])+bin_list[chunk][outer_count]))
                outer_count+=2
                inner_count=inner_count+2
            #print(bin_list[chunk][inner_count],bin_list[chunk][outer_count])


            if outer_count>=8:
                inner_count=0
                outer_count=1
                rem1.append([])
                
    #cypher text-2

    for chunk in range(len(bin_list)):
        for j in range(1,len(bin_list[chunk]),2):

            rem2[chunk].append(negation_swap(bin_list[chunk][j]))

        if (chunk != len(bin_list)-1):

            rem2.append([])
            

    #writing the encryted data inta a filw
    #rem1
    eny_write(rem1,rem2,Str_len,rem1_len,rem2_len)

    

def decryption(file,R_str,rem1_decry,rem2_decry):
    inner_count=0
    outer_count=1
    
    mode=1
    txt=file.read()
    Str=''

    for i in range(len(txt)-1,0,-1):

        if(txt[i] == '%'):
            break
        elif (txt[i] != ','):
            Str+=txt[i]
            
        elif (txt[i] == ','):
            rem_count.append(int(Str))
            Str=''
            pass

    bin_chunks=binary_data_to_8BIT(txt)
    

    #rem1 decryption
    for i in range(int((rem_count[0]/8)/2)):
        rem1_decry.insert(i,''.join(xor_binary_strings(bin_chunks[inner_count],bin_chunks[outer_count])))    
        outer_count+=2
        inner_count=inner_count+2
    

    #rem2 decrtption
    for i in range(len(bin_chunks)-int((rem_count[0]/8)),0,-1):
        rem2_decry.append(negation_swap(bin_chunks[len(bin_chunks)-i]))
        #print(bin_chunks[len(bin_chunks)-i])
   

    for i,j in zip(rem1_decry,rem2_decry):
        if i == '00000000' or j == '00000000':
            pass
        else:
            R_str+=binary_to_text(i)
            R_str+=binary_to_text(j)
    return R_str
    
def report(bin_list,mode,Rem1=None,Rem2=None,Rem1_decry=None,Rem2_decry=None,r_str=None):
    time.sleep(1)
    print(f'{"---"*5} final report {"---"*5}\n')
    
    if (mode==0):
        time.sleep(1)
        print(f"binary value of the txt :\n{bin_list}")
        time.sleep(1)
        print(f"cypher text-1 : \n{Rem1}")
        time.sleep(1)
        print(f"cypher text-2 : \n{Rem2}")
    if (mode == 1):
        print(f"decrypted cypher text-1 : {Rem1_decry}")
        time.sleep(1)
        print(f"decrypted cypher text-2 : {Rem2_decry}")
        time.sleep(1)
        print()
        print(f"decrypted txt :")
        print(r_str)
        

        


def main():

    run=True
    mode=0
    input_text=''
    rem1_len=0
    rem2_len=0
    bin_list=[[]]
    rem1=[[]]
    rem2=[[]]
    rem1_decry=[]
    rem2_decry=[]
    R_str=""
    
    while run:

        print('---'*20)

        print("1.Encryption")
        print("2.Decryption")
        print("3.Exit\n")

        choice=int(input("Enter your choice : "))

        if (choice == 1):
            mode=0
            print("1.Enter the text")
            print("2. open file\n")

            choice_1=int(input("Enter your choice : "))

            if (choice_1 ==1):
                input_text = input("Enter the text : ")
                input_text+=" "

            if (choice_1 ==2):
                path=input("enter your file path : ")
                file=open(path,'r')
                input_text=file.read()
                input_text+=" "

            Str_len=len(input_text)
            binary_chunks= text_to_binary_list(input_text)

            conv_64bit(binary_chunks,bin_list)

            encryption(bin_list,Str_len,rem1_len,rem2_len,rem1,rem2)
            time.sleep(1.5)
            print("\ntext was successfully Encrypted!\n")
            time.sleep(1)
            report(bin_list,mode,Rem1=rem1,Rem2=rem2)
            bin_list=[[]]
            rem1=[[]]
            rem2=[[]]

        elif (choice ==2):
            mode=1

            print("1.Default")
            print("2.open file\n")

            choice_2=int(input("Enter your choice : "))

            if (choice_2 == 1):
                file=open("eny-data.txt",'r')
            elif (choice_2 == 2):
                path=input("Enter the file path : ")
                file=open(path,'r')


            R_str=decryption(file,R_str,rem1_decry,rem2_decry)
            time.sleep(1.5)
            print("\ntext was successfully decrypted!\n")
            time.sleep(1)
            report(bin_list,mode,Rem1_decry=rem1_decry,Rem2_decry=rem2_decry,r_str=R_str)
            R_str=""
            rem1_decry=[]
            rem2_decry=[]

        elif (choice == 3):
            run=False


if __name__ == '__main__':
    main()







    


