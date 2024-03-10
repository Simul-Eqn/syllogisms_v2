from syllogism import * 

def get_n_statements(num:int, typeName:str): 
    sss = [] 
    cancelled = False 
    while len(sss) < num: 
        # get type 
        stdout.write("\nType of "+typeName+" syllogism(0 to display help): ") 
        try:
            type_n = int(stdin.readline())
            if type_n == -1: 
                # quit 
                return None 
            if type_n == 0:
                #display help
                stdout.write("-1: quit \n0: show syllogism statement formats \n1: all [] are [] \n2: some [] are [] \n3: some [] are not [] \n4: no [] are []\n\n")
                continue 
            if type_n<-1 or type_n>4:
                1/0 
            
            #n is the syllogism type, from 1 to 4.


            stdout.write("Variable names (space separated): ") 
            while True:
                try:
                    temp = stdin.readline()
                    if temp.lower() == "quit":
                        cancelled = True
                        1/0 
                        #break 
                    a, b = temp.split() 
                    break
                except:
                    1/0 
                    
            
            #a and b are the variable names (string) 
            stdout.write("Confirm syllogism statement? (y/n): ")
            temp = stdin.readline().strip().lower() 
            if temp == 'y':
                sss.append(SyllogismStatement(type_n, a, b)) 
                stdout.write("Syllogism statement appended successfully. \n\n") 
            else:
                stdout.write("Syllogism statement cancelled. \n\n") 

        except: 
            if cancelled:
                stdout.write("CANCELLED\n\n\n")
            else: 
                stdout.write("Invalid input format. \n\n")
    
    return sss 



if __name__ == "__main__": 

    stdout.write('SYLLOGISM EVALUATOR !!!!!!!!!! \n\n')
    while True:
        stdout.write(
    """MENU:
1) EVALUATE N-TO-1 CHAIN SYLLOGISM BY NUMBER 
2) EVALUATE SYLLOGISM (MANUAL)
3) SAVE CURRENT SYLLOGISM TO .SYL FILE 
4) LOAD SYLLOGISM FROM .SYL FILE 
5) ADD PREMISES TO CURRENT SYLLOGISM (not yet working) 
6) ADD CONCLUSIONS TO CURRENT SYLLOGISM (not yet working) 
7) SHOW CURRENT SYLLOGISM INFORMATION 
8) RE-SOLVE CURRENT SYLLOGISM 
9) SHOW VISUALIZATION FOR CURRENT SYLLOGISM SOLVE 
10) DISPLAY SYLLOGISM MEANINGS
Choice: """) 
        try:
            n = int(stdin.readline())
        except:
            stdout.write("Invalid input format. \n\n")
            continue
        
        if n==1:
            # get n_in 
            stdout.write("Number of inputs: ") 
            try:
                n_in = int(stdin.readline())
                if n_in<2: 1/0 
            except:
                stdout.write("Invalid input. \n\n")
                continue
                
            # get v 
            stdout.write("Syllogism number: ") 
            try:
                v = int(stdin.readline())
                if v<0: 1/0 
            except:
                stdout.write("Invalid input. \n\n")
                continue

            syl = Syllogism.get_chain_syllogism(n_in, v) 

            syl.process_premises() 
            ress = syl.evaluate_conclusions() 
            stdout.write("CONCLUSION: " + str(syl.conclusions[0]) + " : "+str(ress[0])) 
            stdout.write("\n\n") 

        elif n==2: 

            # get all variable names 
            stdout.write("Variable names (space-separated): ") 
            varnames = stdin.readline().strip() 

            # get number of premises 
            stdout.write("Number of premises: ") 
            try:
                n_prem = int(stdin.readline())
                if n_prem<2: 1/0 
            except:
                stdout.write("Invalid input. \n\n")
                continue

            # get premises 
            premises = get_n_statements(n_prem, "premise") 
            if (premises == None): # user has quit 
                continue 


            # decide if gen conclusions or not 
            stdout.write("Evaluate all conclusions given a list of variable names? (y/n): ") 
            inp = stdin.readline().strip() 
            gen_conclusions = (inp=='y' or inp=='Y') 
            
            if gen_conclusions: 
                # get variable names and generate conclusions 
                stdout.write("Variable names allowed (space-separated): ") 
                con_varnames = stdin.readline().strip().split() 
                conclusions = Syllogism.get_conclusions_with_varnames(con_varnames) 

            else: 
                # get number of conclusions 
                stdout.write("Number of conclusions: ") 
                try:
                    n_con = int(stdin.readline())
                    if n_con<0: 1/0 
                except:
                    stdout.write("Invalid input. \n\n")
                    continue

                # for each conclusion 
                conclusions = get_n_statements(n_con, "conclusion") 
                if (conclusions == None): # user has quit 
                    continue 


            syl = Syllogism(premises, conclusions) 

            syl.process_premises() 
            ress = syl.evaluate_conclusions() 
            stdout.write("\n\nCONCLUSIONS: \n") 
            for i in range(len(syl.conclusions)): 
                stdout.write(str(syl.conclusions[i])+" : "+str(ress[i]) + '\n') 
            stdout.write("\n\n\n") 
            
        elif n==3: 
            if (syl): 
                savepath = "" 
                while (savepath == ""): 
                    try: 
                        stdout.write("File name/path (ends in .syl): ") 
                        savepath = stdin.readline().strip() 
                        if savepath[-4:] != '.syl': 1/0 
                    except: 
                        stdout.write("Invalid input format. \n\n") 
                        savepath = "" 
                
                # try saving 
                try: 
                    syl.save(savepath) 
                    stdout.write("SUCCESSFULLY SAVED SYLLOGISM!\n\n") 
                except: 
                    stdout.write("ERROR SAVING SYLLOGISM.\n\n")

            else: 
                stdout.write("NO CURRENT SYLLOGISM. \n\n") 
        
        elif n==4: 
            loadpath = "" 
            while (loadpath == ""): 
                try: 
                    stdout.write("File name/path (ends in .syl): ") 
                    loadpath = stdin.readline().strip() 
                    if loadpath[-4:] != '.syl': 1/0 
                except: 
                    stdout.write("Invalid input format. \n\n") 
                    loadpath = "" 
            
            try: 
                syl = Syllogism.get_syllogisms_from_file(loadpath)[-1] 
            except: 
                stdout.write("Error loading syllogism from file.") 

            try: 
                syl.process_premises() 
                ress = syl.evaluate_conclusions() 

                stdout.write("\n\nPREMISES: \n") 
                for i in range(len(syl.premises)): 
                    stdout.write(str(syl.premises[i])+"\n") 
                stdout.write("\n\n\n") 

                stdout.write("\n\nCONCLUSIONS: \n") 
                for i in range(len(syl.conclusions)): 
                    stdout.write(str(syl.conclusions[i])+" : "+str(ress[i]) + '\n') 
                stdout.write("\n\n\n") 
            except: 
                stdout.write("ERROR PROCESING SYLLOGISM\n\n")
        
        elif n==5: 
            if (syl): 
                # get number of premises 
                stdout.write("Number of premises to add: ") 
                try:
                    n_prem = int(stdin.readline())
                    if n_prem<2: 1/0 
                except:
                    stdout.write("Invalid input. \n\n")
                    continue

                # get premises 
                premises = get_n_statements(n_prem, "premise") 
                if (premises == None): # user has quit 
                    continue 

                syl.add_premises_and_process(premises) 

                stdout.write("SUCCESSFULLY ADDED PREMISES AND PROCESSED!\n\n")
            else: 
                stdout.write("NO CURRENT SYLLOGISM. \n\n") 
            
        elif n==6: 
            if (syl): 
                # get number of conclusions 
                stdout.write("Number of conclusions: ") 
                try:
                    n_con = int(stdin.readline())
                    if n_con<0: 1/0 
                except:
                    stdout.write("Invalid input. \n\n")
                    continue

                # for each conclusion 
                conclusions = get_n_statements(n_con, "conclusion") 
                if (conclusions == None): # user has quit 
                    continue 

                ress = syl.add_conclusions_and_evaluate(conclusions) 
                stdout.write("\n\nNEW CONCLUSIONS: \n") 
                for i in range(len(conclusions)): 
                    stdout.write(str(conclusions[i])+" : "+str(ress[i]) + '\n') 
                stdout.write("\n\n\n") 
                
            else: 
                stdout.write("NO CURRENT SYLLOGISM. \n\n") 

        elif n==7: 
            if syl: 
                stdout.write("\n\nPREMISES: \n") 
                for i in range(len(syl.premises)): 
                    stdout.write(str(syl.premises[i])+"\n") 
                stdout.write("\n\n\n") 

                stdout.write("\n\nCONCLUSIONS: \n") 
                for i in range(len(syl.conclusions)): 
                    stdout.write(str(syl.conclusions[i]) + '\n') 
                stdout.write("\n\n\n") 
            else: 
                stdout.write("NO CURRENT SYLLOGISM. \n\n") 

        elif n==8: 
            if syl: 
                ress = syl.evaluate_conclusions() 

                stdout.write("\n\nPREMISES: \n") 
                for i in range(len(syl.premises)): 
                    stdout.write(str(syl.premises[i])+"\n") 
                stdout.write("\n\n\n") 

                stdout.write("\n\nCONCLUSIONS: \n") 
                for i in range(len(syl.conclusions)): 
                    stdout.write(str(syl.conclusions[i])+" : "+str(ress[i]) + '\n') 
                stdout.write("\n\n\n") 
            else: 
                stdout.write("NO CURRENT SYLLOGISM. \n\n") 
        
        elif n==9: 
            if syl: 
                syl.show_visualization(block=True) 
            else: 
                stdout.write("NO CURRENT SYLLOGISM. \n\n") 

        elif n==10: 
            stdout.write('''
DEFINITIONS:

all A are B:
everything in A are also in B

some A are B:
>= 1 thing in A is also in B

some A are not B:
>= 1 thing in A is not also in B

no A are B:
0 things in A are also in B AND A has at least one thing


''')
        
        else: 
            # have a way to terminate. 
            break 
