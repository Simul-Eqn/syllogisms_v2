from sys import stdin, stdout, setrecursionlimit 
setrecursionlimit(1000010) 

import matplotlib.pyplot as plt 
from pyvenn import venn

debugging = True 


'''
structure 1: all A are B 
structure 2: some A are B 
structure 3: some A are not B 
structure 4: no A are B
so each structure is s1 + s2 + s3 + s4 
format:

given that:
all A are B
some B are C
is it true that:
some A are not C

'''

'''
DEFINITIONS:
all A are B:
everything in A are also in B

some A are B:
>= 1 thing in A is also in B

some A are not B:
>= 1 thing in A is not also in B

no A are B:
0 things in A are also in B AND A has at least one thing 
'''



class SyllogismStatement:     
    def __init__(self, *l): 
        assert len(l)==3, "Invalid Syllogism Statement List - must be of length 3. " 
        assert (isinstance(l[0], int)), "Invalid Syllogism Statement List - first element must be a number. " 
        assert (1 <= l[0] and l[0] <= 4), "Invalid Syllogism Statement List - first element must be from 1 to 4 (inclusive). " 
        assert (isinstance(l[1], str)), "Invalid Syllogism Statement List - second element must be a string. " 
        assert (isinstance(l[2], str)), "Invalid Syllogism Statement List - third element must be a string. " 

        self.num = l[0] 
        self.t1 = l[1] 
        self.t2 = l[2] 
    
    def __list__(self): 
        syllogism = [self.num, self.t1, self.t2] 
        return [i for i in syllogism] 
    
    def __str__(self): 
        if (self.num == 1): 
            #all A are B
            s1 = "all "
            s2 = " are "
        elif (self.num == 2):
            #some A are B 
            s1 = "some "
            s2 = " are "
        elif (self.num == 3):
            #some A are not B
            s1 = "some "
            s2 = " are not "
        else:
            #no A are B
            s1 = "no "
            s2 = " are "
        
        return s1 + self.t1 + s2 + self.t2 

    def __eq__(self, ss2): 
        assert (isinstance(ss2, SyllogismStatement)), "Cannot compare Syllogism Statement with other types" 
        
        if (self.num != ss2.num): return False 
        
        # Some and No can have different order 
        if (self.num==2 or self.num==4): 
            return (  ( (self.t1 == ss2.t1) and (self.t2 == ss2.t2) ) 
                    or ( (self.t1 == ss2.t2) and (self.t2 == ss2.t1) )  )
        else: 
            return ( (self.t1 == ss2.t1) and (self.t2 == ss2.t2) ) 


    @staticmethod 
    def equals(ss1, ss2, v1:list, v2:list): 
        # v1 is variables for v1 
        # v2 is variables for v2 
        assert (isinstance(ss1, SyllogismStatement)), "Cannot compare Syllogism Statement with other types" 
        assert (isinstance(ss2, SyllogismStatement)), "Cannot compare Syllogism Statement with other types" 
        if (ss1.num != ss2.num): return False 

        order1 = [v1.index(ss1.t1), v1.index(ss1.t2)] 
        order2 = [v2.index(ss2.t1), v2.index(ss2.t2)] 
        
        # Some and No can have different order 
        if (ss1.num==2 or ss1.num==4): 
            return (  ( (order1[0] == order2[0]) and (order1[1] == order2[1]) ) 
                    or ( (order1[0] == order2[1]) and (order1[1] == order2[0]) )  ) 
        else: 
            return ( (order1[0] == order2[0]) and (order1[1] == order2[1]) ) 



class Syllogism: 
    @staticmethod 
    def get_nto1_chains(n:int): 
        assert (n>=2), "N of syllogism must be at least 2" 
        def nto1_syl_generator(): 
            for v in range(6**n): 
                yield Syllogism.get_chain_syllogism(n, v) 
        return nto1_syl_generator 

    @staticmethod 
    def get_varnames(n:int): 
        # this returns n variables, not the variables needed for n-to-1 syllogism 
        prev = "" 
        varnames = [] 
        for i in range(n): 
            if (i%26==0 and i!=0): 
                prev += "A" 
            varnames.append(prev + chr(ord("A")+i)) 
        return varnames 

    @staticmethod 
    def get_chain_syllogism(n:int, v:int): # constructor to make Chain Syllogism 
        assert (n>=2), "N of syllogism must be at least 2" 
        self = Syllogism([], []) 
        self.n_premises = n 
        self.premises = [] 
        self.n_conclusions = 1 
        self.conclusions = [] 
        self.solveArr = None 

        # set premises and conclusions 
        varnames = Syllogism.get_varnames(n+1) 
        self.varnames = varnames 
        for i in range(n): 
            temp = (v%6)+1 
            if (temp <= 4): # normal order 
                self.premises.append(SyllogismStatement(temp, varnames[i], varnames[i+1])) 
            else: # reversed all (1), reversed some not (3) 
                self.premises.append(SyllogismStatement(((temp-4)*2)-1, varnames[i+1], varnames[i])) 
            v //= 6 
        temp = (v%6)+1 
        if (temp <= 4): # normal order 
            self.conclusions.append(SyllogismStatement(temp, varnames[-1], varnames[0])) 
        else: # reversed all (1), reversed some not (3) 
            self.conclusions.append(SyllogismStatement(((temp-4)*2)-1, varnames[0], varnames[-1])) 

        # done :)) return it yay 
        return self 
    
    @staticmethod 
    def get_chain_syllogism_all_conclusions(n:int, v:int): # constructor to make Chain Syllogism, but w all conclusions 
        assert (n>=2), "N of syllogism must be at least 2" 
        self = Syllogism([], []) 
        self.n_premises = n 
        self.premises = [] 
        self.n_conclusions = 1 
        self.conclusions = [] 
        self.solveArr = None 

        # set premises and conclusions 
        varnames = Syllogism.get_varnames(n+1) 
        self.varnames = varnames 
        for i in range(n): 
            temp = (v%6)+1 
            if (temp <= 4): # normal order 
                self.premises.append(SyllogismStatement(temp, varnames[i], varnames[i+1])) 
            else: # reversed all (1), reversed some not (3) 
                self.premises.append(SyllogismStatement(((temp-4)*2)-1, varnames[i+1], varnames[i])) 
            v //= 6 

        # add all possible conclusions 
        self.conclusions = Syllogism.get_conclusions_with_varnames(self.varnames) 
        '''for con_num in range(6): 
            for first in self.varnames: 
                for second in self.varnames: 
                    if (con_num <= 4): # normal order 
                        self.conclusions.append(SyllogismStatement(con_num, first, second)) 
                    else: # reversed all (1), reversed some not (3) 
                        if (first == second): continue # prevent these duplicates 
                        self.conclusions.append(SyllogismStatement(((con_num-4)*2)-1, second, first)) 
        ''' 

        # done :)) return it yay 
        return self 

    @staticmethod 
    def get_syllogisms_from_file(path:str): # returns a list of all syllogisms in a file 
        fin = open(path, 'r') 
        data = fin.readlines() 
        fin.close() 

        syls = [] 
        reading_premise = True 
        premises = [] 
        conclusions = [] 
        i = 0 
        while i < len(data): 
            d = data[i] 
            if (d.strip() == "Given that:"): 
                reading_premise = True 
                Syllogism.print("READING GIVEN THAT")

            elif (d.strip() == "Is it true that:"): 
                reading_premise = False 
                Syllogism.print("READING IS IT TRUE THAT") 

            elif (d.strip() == ''): 
                if not reading_premise: 
                    syls.append(Syllogism(premises, conclusions)) 
                    reading_premise = True 
                    premises = [] 
                    conclusions = [] 
                    i += 2 # skip the other newline and "Given that:" 
                    continue 
                else: 
                    # start reading conclusions instead 
                    reading_premise = False 
                    i += 2 # skip the reading "Is it true that:" 
                    continue 
            else: 
                ssl = d.strip().split() 
                if len(ssl) == 5: 
                    # some not 
                    ss = SyllogismStatement(3, ssl[1], ssl[4]) 
                elif ssl[0] == "all": 
                    ss = SyllogismStatement(1, ssl[1], ssl[3]) 
                elif ssl[0] == "some": 
                    ss = SyllogismStatement(2, ssl[1], ssl[3]) 
                elif ssl[0] == "no": 
                    ss = SyllogismStatement(4, ssl[1], ssl[3]) 
                else: 
                    raise Exception("Cannot process file") 
                
                if reading_premise: 
                    premises.append(ss) 
                else: 
                    conclusions.append(ss) 
            i += 1 

        return syls 


    @staticmethod 
    def get_conclusions_with_varnames(varnames:list): 
        res = [] 
        for con_num in range(1,7): 
            for first in varnames: 
                for second in varnames: 
                    if (con_num <= 4): # normal order 
                        res.append(SyllogismStatement(con_num, first, second)) 
                    else: # reversed all (1), reversed some not (3) 
                        if (first == second): continue # prevent these duplicates 
                        res.append(SyllogismStatement(((con_num-4)*2)-1, second, first)) 
        return res 

    @staticmethod 
    def print(*args): 
        if debugging: 
            print(*args) 

    @staticmethod 
    def blist_to_idx(yay:list): 
        res = 0 
        for i in range(len(yay)): 
            res <<= 1 
            res += yay[i] 
        return res 


    def __init__(self, premises:list, conclusions:list): 
        self.n_premises = len(premises) 
        self.premises = premises 
        self.n_conclusions = len(conclusions) 
        self.conclusions = conclusions 

        self.solveArr = None 
        self.solveExistances = None 

        varnames = set() 
        for s in premises:
            varnames.add(s.t1)
            varnames.add(s.t2)
        for s in conclusions:
            varnames.add(s.t1)
            varnames.add(s.t2)
        
        self.varnames = list(varnames) 
    
    def add_premises(self, *premises): 
        # TODO: verify and add premises 
        self.solveArr = None 
        self.solveExistances = None 
        pass 

    def add_premises_and_process(self, *premises): 
        # TODO: process it live yay 
        pass 

    def add_conclusions(self, *conclusions): 
        pass 

    def add_conclusions_and_evaluate(self, conclusions): # RETURN CONCLUSION EVALUATION RESULTS 
        return [False for _ in range(len(conclusions))] 

    def process_premises(self): # returns True if no contradiction, False if contradiction 
        self.solveArr = [0 for _ in range(2**len(self.varnames))] 
        # for the indices, they're, in binary, 0000, 0001, 0010, so on. 
        # the first binary digit is varnames[0], then second is varnames[1], and so on. 
        self.solveExistances = [] 
        
        for premise in self.premises: 
             self.eval_premise(premise) 
    
        if self.check_contradiction():
            stdout.write("Contradicting syllogisms found, please retry. \n\n\n")
            return False 
        
        Syllogism.print() 
        Syllogism.print("SOLVE:", self.solveArr) 
        Syllogism.print("EXISTANCES:", self.solveExistances) 

        return True 
    
    def eval_premise(self, premise): 
        Syllogism.print("\nEVALUATING PREMISE:", premise) 
        if premise.num== 1:
            #all [] are []
            Syllogism.print("all [] are []") 

            # all that are in A but not in B do not exist. 
            idx1 = self.varnames.index(premise.t1) 
            idx2 = self.varnames.index(premise.t2) 
            other_idxs = [] 
            for i in range(len(self.varnames)): 
                if (i==idx1 or i==idx2): continue 
                other_idxs.append(i) 
            
            yay = [0 for _ in self.varnames]  
            yay[idx1] = 1 
            yay[idx2] = 0 

            def increment_yay_from(i): 
                if i<0: return # this is normal yay 
                if (yay[other_idxs[i]] == 1): 
                    yay[other_idxs[i]] = 0 
                    increment_yay_from(i-1) 
                else: 
                    yay[other_idxs[i]] = 1 

            for _ in range(2**len(other_idxs)): 
                increment_yay_from( len(other_idxs)-1 ) 
                idx = Syllogism.blist_to_idx(yay) 
                if (self.solveArr[idx] > 0): 
                    # deal with the existances 
                    for ex_idx in range(len(self.solveExistances)): 
                        if ((1<<ex_idx) & self.solveArr[idx]): 
                            self.solveExistances[ex_idx] -= 1 
                self.solveArr[idx] = -1 
            
        elif premise.num == 2:
            #some [] are []
            Syllogism.print("some [] are []") 

            # all that are in A and also in B have an existance. 
            ex_binary = 1 << len(self.solveExistances) 
            ex_cnt = 0 

            idx1 = self.varnames.index(premise.t1) 
            idx2 = self.varnames.index(premise.t2) 
            other_idxs = [] 
            for i in range(len(self.varnames)): 
                if (i==idx1 or i==idx2): continue 
                other_idxs.append(i) 
            
            yay = [0 for _ in self.varnames]  
            yay[idx1] = 1 
            yay[idx2] = 1 

            def increment_yay_from(i): 
                if i<0: return # this is normal yay 
                if (yay[other_idxs[i]] == 1): 
                    yay[other_idxs[i]] = 0 
                    increment_yay_from(i-1) 
                else: 
                    yay[other_idxs[i]] = 1 

            for _ in range(2**len(other_idxs)): 
                increment_yay_from( len(other_idxs)-1 ) 
                idx = Syllogism.blist_to_idx(yay) 
                if (self.solveArr[idx] >= 0): 
                    # add the existance 
                    self.solveArr[idx] |= ex_binary 
                    ex_cnt += 1 
            self.solveExistances.append(ex_cnt) 
            
        elif premise.num == 3:
            #some [] are not []
            Syllogism.print("some [] are not []") 
            
            # all that are in A but not in B have an existance. 
            ex_binary = 1 << len(self.solveExistances) 
            ex_cnt = 0 

            idx1 = self.varnames.index(premise.t1) 
            idx2 = self.varnames.index(premise.t2) 
            other_idxs = [] 
            for i in range(len(self.varnames)): 
                if (i==idx1 or i==idx2): continue 
                other_idxs.append(i) 
            
            yay = [0 for _ in self.varnames]  
            yay[idx1] = 1 
            yay[idx2] = 0 

            def increment_yay_from(i): 
                if i<0: return # this is normal yay 
                if (yay[other_idxs[i]] == 1): 
                    yay[other_idxs[i]] = 0 
                    increment_yay_from(i-1) 
                else: 
                    yay[other_idxs[i]] = 1 

            for _ in range(2**len(other_idxs)): 
                increment_yay_from( len(other_idxs)-1 ) 
                idx = Syllogism.blist_to_idx(yay) 
                if (self.solveArr[idx] >= 0): 
                    # add the existance 
                    self.solveArr[idx] |= ex_binary 
                    ex_cnt += 1 
            self.solveExistances.append(ex_cnt) 
            
        elif premise.num == 4:
            #no [] in []
            Syllogism.print("no [] in []") 

            # all that are in A and also in B do not exist. 
            idx1 = self.varnames.index(premise.t1) 
            idx2 = self.varnames.index(premise.t2) 
            other_idxs = [] 
            for i in range(len(self.varnames)): 
                if (i==idx1 or i==idx2): continue 
                other_idxs.append(i) 
            
            yay = [0 for _ in self.varnames]  
            yay[idx1] = 1 
            yay[idx2] = 1 

            def increment_yay_from(i): 
                if i<0: return # this is normal yay 
                if (yay[other_idxs[i]] == 1): 
                    yay[other_idxs[i]] = 0 
                    increment_yay_from(i-1) 
                else: 
                    yay[other_idxs[i]] = 1 

            for _ in range(2**len(other_idxs)): 
                increment_yay_from( len(other_idxs)-1 ) 
                idx = Syllogism.blist_to_idx(yay) 
                if (self.solveArr[idx] > 0): 
                    # deal with the existances 
                    for ex_idx in range(len(self.solveExistances)): 
                        if ((1<<ex_idx) & self.solveArr[idx]): 
                            self.solveExistances[ex_idx] -= 1 
                self.solveArr[idx] = -1 
            
    def check_contradiction(self): 
        # check for contradictions - one of the existances have zero leftover. 
        for ex_num in self.solveExistances: 
            if ex_num <= 0: 
                Syllogism.print("CONTRADICTION AT EX NUM:",ex_num) 
                return True 
        return False 

    def evaluate_conclusions(self): # returns a array of 1/0/-1 for for deftrue/maybe/deffalse for each conclusion 
        assert (self.solveArr != None), "Must process premises of a Syllogism before evaluating its conclusions" 
        
        ress = [] 
        for conclusion in self.conclusions: 
            ress.append(self.eval_conclusion(conclusion)) 
        
        return ress 

    def eval_conclusion(self, conclusion): 
        print("\nEVALUATING SYLLOGISM:", conclusion) 
        if conclusion.num == 1:
            #all [] are []
            Syllogism.print("all [] are []") 

            # check all that are in A but not in B do not exist. 
            idx1 = self.varnames.index(conclusion.t1) 
            idx2 = self.varnames.index(conclusion.t2) 
            other_idxs = [] 
            for i in range(len(self.varnames)): 
                if (i==idx1 or i==idx2): continue 
                other_idxs.append(i) 
            
            yay = [0 for _ in self.varnames]  
            yay[idx1] = 1 
            yay[idx2] = 0 

            def increment_yay_from(i): 
                if i<0: return # this is normal yay 
                if (yay[other_idxs[i]] == 1): 
                    yay[other_idxs[i]] = 0 
                    increment_yay_from(i-1) 
                else: 
                    yay[other_idxs[i]] = 1 

            # check if they're all -1 : deftrue 
            all_neg1 = True 
            # check if they altogether contain an existence 
            existences = [0 for _ in range(len(self.solveExistances))] 

            for _ in range(2**len(other_idxs)): 
                Syllogism.print(yay) 
                idx = Syllogism.blist_to_idx(yay) 
                if (self.solveArr[idx] >= 0): 
                    all_neg1 = False 
                    if (self.solveArr[idx] > 0): 
                        # add all the existences 
                        for ex_idx in range(len(self.solveExistances)): 
                            if ((1<<ex_idx) & self.solveArr[idx]): 
                                existences[ex_idx] += 1 
                increment_yay_from( len(other_idxs)-1 ) 
            
            if (all_neg1): 
                return 1 # def true 
            else: 
                # check the existences 
                deffalse = False 
                for ex_idx in range(len(self.solveExistances)): 
                    if (existences[ex_idx] == self.solveExistances[ex_idx]): 
                        deffalse = True 
                        break 
                if (deffalse): 
                    return -1 # indeed def false 
                else: 
                    return 0 # maybe 

        elif conclusion.num == 2:
            # some [] are []
            Syllogism.print("some [] are []") 
            Syllogism.print("This is the reverse of: ") 
            return -(self.eval_conclusion(SyllogismStatement(4, conclusion.t1, conclusion.t2))) 
            
        elif conclusion.num == 3:
            # some [] are not []
            Syllogism.print("some [] are not []") 
            Syllogism.print("This is the reverse of: ") 
            return -(self.eval_conclusion(SyllogismStatement(1, conclusion.t1, conclusion.t2))) 
        
        elif conclusion.num == 4:
            # no [] are []
            Syllogism.print("no [] are []") 

            # check all that are in A and also in B. 
            idx1 = self.varnames.index(conclusion.t1) 
            idx2 = self.varnames.index(conclusion.t2) 
            other_idxs = [] 
            for i in range(len(self.varnames)): 
                if (i==idx1 or i==idx2): continue 
                other_idxs.append(i) 
            
            yay = [0 for _ in self.varnames]  
            yay[idx1] = 1 
            yay[idx2] = 1 

            def increment_yay_from(i): 
                if i<0: return # this is normal yay 
                if (yay[other_idxs[i]] == 1): 
                    yay[other_idxs[i]] = 0 
                    increment_yay_from(i-1) 
                else: 
                    yay[other_idxs[i]] = 1 

            # check if they're all -1 : deftrue 
            all_neg1 = True 
            # check if they altogether contain an existence 
            existences = [0 for _ in range(len(self.solveExistances))] 

            for _ in range(2**len(other_idxs)): 
                Syllogism.print(yay) 
                idx = Syllogism.blist_to_idx(yay) 
                if (self.solveArr[idx] >= 0): 
                    all_neg1 = False 
                    if (self.solveArr[idx] > 0): 
                        # add all the existences 
                        for ex_idx in range(len(self.solveExistances)): 
                            if ((1<<ex_idx) & self.solveArr[idx]): 
                                existences[ex_idx] += 1 
                increment_yay_from( len(other_idxs)-1 ) 
            
            if (all_neg1): 
                return 1 # def true 
            else: 
                # check the existences 
                #Syllogism.print("EXISTENCES:", existences)
                deffalse = False 
                for ex_idx in range(len(self.solveExistances)): 
                    if (existences[ex_idx] == self.solveExistances[ex_idx]): 
                        deffalse = True 
                        break 
                if (deffalse): 
                    return -1 # indeed def false 
                else: 
                    return 0 # maybe 

    def show_visualization(self, title:str="Visualization of Syllogism", block:bool=False): 
        assert (self.solveArr != None), "Must process premises of a Syllogism before showing its visualization" 
        assert (len(self.varnames) > 1), "Cannot show visuaslization for Syllogism with only one term" 
        assert (len(self.varnames) < 7), "Cannot show visuaslization for Syllogism with more than 6 terms" 

        labels = {} 

        # add labels 
        for bitmask in range(2**len(self.varnames)):
            vals = [(bitmask>>i)%2 for i in range(len(self.varnames))]
            key = ""
            for val in vals:
                key += str(val)
            
            value = self.solveArr[Syllogism.blist_to_idx(vals)] 
            #value = str(eval(genQuery(self.varnames, (-1,-1,-1), -1, -1, vals)))
            labels[key] = value 

        # get visualization 
        fig, ax = eval("venn.venn"+str(len(self.varnames))+"(labels, self.varnames)")
        plt.title(title) 
        plt.show(block=block) 
    
    def __str__(self): 
        res = "Given that: \n" 
        for premise in self.premises: 
            res += str(premise)+'\n' 
        
        res += "\nIs it true that: \n"
        for conclusion in self.conclusions: 
            res += str(conclusion)+'\n' 
        
        res += '\n' 
        return res 
    
    def save_solve(self, path): 
        assert (self.solveArr != None), "Must process premises of a Syllogism before saving its solve" 
        out = open(path, 'a+') 
        out.write(str(self.solveArr)) 
        out.write('\n') 
        out.write(str(self.solveExistances))
        out.write('\n\n') 
        out.close() 
    
    def save(self, path): 
        out = open(path, 'a+') 
        out.write(str(self)) 
        out.close() 



