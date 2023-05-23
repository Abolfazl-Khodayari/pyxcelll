import re
class tables:
    def __init__(self, column=5, row=10):
        self.table = [['None' for _ in range(column)] for _ in range(row)]
        self.classdic = {}
        self.column = column
        self.row = row
    def __repr__(self):
        return str(self.table)
    def setFunc(self, row, column, expFunc):
        if (row >= self.row) or (column >= self.column):
            global errors
            errors += 1
        else:
            a = expFunc
            if context != 0:
                if dics:
                    a = removeVariables(a, dics)          
            self.table[row][column] = a
    def display(self):
        mat = [[0 for i in range(self.column)] for i in range(self.row)]
        for i in range(self.row):
            for j in range(self.column):
                mat[i][j] = solver(self.table[i][j])
        mat.insert(0, [num2AA(i) for i in range(self.column)])
        for i in range(self.row+1):
            mat[i].insert(0,str(i))
        lens = [max(map(len, col)) for col in zip(*mat)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in mat]
        print('\n'.join(table))
    def setvall(self, key, exp):
        self.classdic[key] = exp
    def setcell(self, row, column, exp):
        if (row >= self.row) or (column >= self.column):
            global errors
            errors += 1
        else:
            self.table[row][column] = exp

def AA2num(a):
    a = re.sub(r'"', '', a)
    Dic1 = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10,
        'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, 'R':17, 'S':18, 'T':19, 'U':20,
        'V':21, 'W':22, 'X':23, 'Y':24, 'Z':25}
    a = a[::-1]
    i, c = 0, 0
    while i != (len(a)):
        b = Dic1[a[i]]
        if i == 0: c += b
        else: c += (b+1)*(26**i)
        i += 1
    return c
def num2AA(a):
    a = int(a)
    Dic2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ans = ''
    while a >= 0:
        i = a%26
        ans += Dic2[i]
        a //= 26
        a -= 1
    ans = ans[::-1]
    return ans
def solver(a):
    global errors
    def multi(a):
        global errors
        pattern = re.compile(r'(("[^"]*")|([0-9]+\.?[0-9]*))(\s*)?(\*|\/)(\s*)?(("[^"]*")|([0-9]+\.?[0-9]*))')
        matches = pattern.search(a)
        part1 = (matches.group(1))
        str1 = re.search(r'".*"',part1)
        float1 = re.search(r'[0-9]+\.[0-9]+',part1)
        if not str1:
            if not float1:
                part1 = int(part1)
            else:
                part1 = float(part1)
        act = (matches.group(5))
        part2 = (matches.group(7))
        str2 = re.search(r'".*"',part2)
        float2 = re.search(r'[0-9]+\.[0-9]+',part2)
        if not str2:
            if not float2:
                part2 = int(part2)
            else:
                part2 = float(part2)
        d = (matches.group(0))
        if str1 and str2:
            errors = 1
            return(1,1)
        else:
            if act == '*':
                if (str1 and float2) or (str2 and float1):
                    errors = 1
                    return(1,1)
                else:
                    ans = part1 * part2
            else:
                if str1 or str2 or part2 == 0:
                    errors = 1
                    return(1,1)
                else:
                    ans = part1 / part2
            ans = str(ans)
            if re.search(r'\".*',ans):
                ans = '\"' + re.sub(r'\"','',ans) + '\"'
            elif re.search(r'[0-9]+\.0+\b',ans):
                ans = re.sub(r'\.0+', '', ans)
            b = a.replace(d,ans)
            return (b,0)
            
    def sumstr(a):
        global errors
        pattern = re.compile(r'(("[^"]*")|([0-9]+\.?[0-9]*))(\s*)?(\+|\-)(\s*)?(("[^"]*")|([0-9]+\.?[0-9]*))')
        matches = pattern.search(a)
        part1 = (matches.group(1))
        str1 = re.search(r'".*"',part1)
        float1 = re.search(r'[0-9]+\.[0-9]+',part1)
        excel1 = re.search(r'"[A-Z]+"',part1)
        int1 = 0
        if not str1:
            if not float1:
                part1 = int(part1)
                int1 = 1
            else:
                part1 = float(part1)
        act = (matches.group(5))
        part2 = (matches.group(7))
        str2 = re.search(r'".*"',part2)
        float2 = re.search(r'[0-9]+\.[0-9]+',part2)
        excel2 = re.search(r'"[A-Z]+"',part2)
        int2 = 0
        if not str2:
            if not float2:
                part2 = int(part2)
                int2 = 1
            else:
                part2 = float(part2)
        d = (matches.group(0))
        if str1 and str2:
            if act == '-':
                errors = 1
                return(1,1)
            else:
                ans = part1 + part2
        else:
            if (str1 and float2) or (float1 and str2):
                errors = 1
                return(1,1)
            else:
                if excel1 and int2:
                    if act == '+': ans = '"' + num2AA(AA2num(part1)+part2) + '"'
                    else:
                        t =AA2num(part1)-part2
                        if t < 0:
                            errors = 1
                            return(1,1)
                        else: ans ='"'+ num2AA(t) +'"'
                elif int1 and excel2:
                    if act == '+': ans = AA2num(part2)+part1
                    else:
                        ans = part1-AA2num(part2)
                else:
                    if (str1 and int2) or (int1 and str2):
                        errors = 1
                        return(1,1)
                    else:
                        if act == '+': ans = part1 + part2
                        else: ans = part1 - part2
        ans = str(ans)
        if re.search(r'\".*',ans):
            ans = '\"' + re.sub(r'\"','',ans) + '\"'
        elif re.search(r'[0-9]+\.0+\b',ans):
            ans = re.sub(r'\.0+', '', ans)
        b = a.replace(d,ans)
        return (b,0)
    a = str(a)
    if context != 0:
        if dics:
            a = removeVariables(a, dics)
        excel = eval("{}.table".format(context))
        if excel:
            a = removeBrakets(a,excel)
    errors = 0
    while errors == 0 and re.search(r'(\*)|(\/)',a):
        s = multi(a)
        if s[1] == 0:
            a = s[0]
        else:
            print('unsupported operand')
            break
    while errors == 0 and re.search(r'(\+|\-)',a):
        s = sumstr(a)
        if s[1] == 0:
            a = s[0]
        else:
            print('unsupported operand')
            break
    if errors == 0:
        return a

def removeVariables(a, vares):
    a = '+'+a+'+'
    for x in vares:
        pattern1 = re.compile(r'([\-\*\+\-\[]|")(\s)?(%s)(\s)?([\-\*\+\-\]]|")' %x)
        while pattern1.search(a):
            matches = pattern1.search(a)
            pd = matches.group(0)
            p1 = matches.group(1)
            p3 = matches.group(3)
            p5 = matches.group(5)
            if p1 == '\"' and p5 == '\"':
                p = '\'' + p3 + '\''
                a = a.replace(pd , p)
            else:
                p3 = str(vares[x])
                if p3 == 'None':
                    a = 'None'
                else:
                    p = p1 + p3 + p5
                    a = a.replace(pd , p)
    a = re.sub(r'\'', '\"', a)
    a = a[1:-1]
    return a
def removeBrakets(a,excel):
    pattern = re.compile(r'(\[)([^\[\]]+)(\])')
    while pattern.search(a):
        matches = pattern.search(a)   
        d = matches.group(0)
        parts = matches.group(2)
        parts = solver(parts)
        parts = re.sub(r'"','', parts)
        excels = re.search(r'([A-Z]+)([0-9]+)', parts)
        if excels:    
            dd = excels.group(0)
            column = AA2num(excels.group(1))
            row = 0
            if excels.group(2):
                row = int(excels.group(2))-1
            ans = excel[row][column]
            if ans == 'None':
                a = 'None'
            else:
                a = re.sub(r'\b%s\b' %dd,str(ans), a)
        else:
            a = a.replace(d, parts)
    pattern = re.compile(r'([A-Z]+)([0-9]+)')
    while pattern.search(a):
        excels = pattern.search(a)    
        dd = excels.group(0)
        column = AA2num(excels.group(1))
        row = 0
        if excels.group(2):
            row = int(excels.group(2))-1
        ans = excel[row][column]
        if ans == 'None':
            a = 'None'
        else:
            a = re.sub(r'\b%s\b' %dd,str(ans), a)
    return a  
def condition(a):
    global errors
    a = re.sub(r'\s', '', a)
    a = re.sub(r'and', ' and ', a)
    a = re.sub(r'or', ' or ', a)
    pattern = re.compile(r'([\w\+\-\*\/\"]*)(==|>|<)([\w\+\-\*\/\"]*)')
    while pattern.search(a):
        maches = pattern.search(a)
        exp0 = maches.group(0)
        exp1 = maches.group(1)
        exp1 = solver(exp1)
        str1 = re.search(r'".*"',exp1)
        float1 = re.search(r'[0-9]+\.[0-9]+',exp1)
        if not str1:
            if not float1:
                exp1 = int(exp1)
                int1 = 1
            else:
                exp1 = float(exp1)
        exp2 = maches.group(2)
        exp3 = maches.group(3)
        exp3 = solver(exp3)
        str3 = re.search(r'".*"',exp3)
        float3 = re.search(r'[0-9]+\.[0-9]+',exp3)
        if not str3:
            if not float3:
                exp3 = int(exp3)
                int3 = 1
            else:
                exp3 = float(exp3)
        if str3 and not str1:
            errors = 1
            return(0)
        elif not str3 and str1:
            errors = 1
            return(0)
        else:
            if exp2 == '==':
                if exp1 == exp3:
                    ans = 'true'
                else:
                    ans = 'false'
            elif exp2 == '>':
                if exp1 > exp3:
                    ans = 'true'
                else:
                    ans = 'false' 
            elif exp2 == '<':
                if exp1 < exp3:
                    ans = 'true'
                else:
                    ans = 'false'
            a = a.replace(exp0, ans)
    pattern = re.compile(r'(true|false)(\s)*(or|and)(\s)*(true|false)')
    while pattern.search(a):
        maches = pattern.search(a)
        exp0 = maches.group(0)
        exp1 = maches.group(1)
        exp2 = maches.group(3)
        exp3 = maches.group(5)
        if exp2 == 'or':
            if exp1 == 'true' or exp3 == 'true':
                ans = 'true'
            else:
                ans = 'false'
        elif exp2 == 'and':
            if exp1 == 'true' and exp3 == 'true':
                ans = 'true'
            else:
                ans = 'false'
        a = a.replace(exp0, ans)
    pattern = re.compile(r'true|false')
    maches = pattern.search(a)
    exp0 = maches.group(0)
    if exp0 == 'true':
        a = 'true'
    else:
        a = 'false'
    return a
n = int(input())
errors = 0
context = 0
sheets = []
dics = {}
cinput = ''
create_pattern = re.compile(r'create\(([^,]+),([0-9]+),([0-9]+)')
context_pattern = re.compile(r'context\(([^,]+)\)')
setFunc_pattern = re.compile(r'setFunc\(([A-Z]+)([0-9]+),(.+)\)')
setFunc2_pattern = re.compile(r'setFunc\((\[.+\])(\[.+\]),(.+)\)')
display_pattern = re.compile(r'display\(([^,]+)\)')
printt_pattern = re.compile(r'print\(([^,]+)\)')
setcell_pattern = re.compile(r'([A-Z]+)([0-9]+)\s+=\s+(.+)\s*')
setcell2_pattern = re.compile(r'(\[.+\])(\[.+\])\s+=\s+(.+)\s*')
setvall_pattern = re.compile(r'\s*(.+)\s+=\s+(.+)')

command_pattern = re.compile(r'(.+)(\n)')
while_pattern = re.compile(r'(\s*)while\((.+)\)\{')
if_pattern = re.compile(r'(\s*)if\((.+)\)\{')
coment_pattern = re.compile(r'(.*)(\$)(.*)')
for _ in range(n):
    command = str(input())
    maches = coment_pattern.search(command)
    if maches:
        command = maches.group(1)
        if command:
            cinput = cinput + command + '\n'
    else:
        cinput = cinput + command + '\n'     
while cinput:
    maches = command_pattern.search(cinput)
    ends = maches.end()
    command = maches.group(1)
    if errors != 0:
        print('Error')
        break
    if if_pattern.search(command):
        maches2 = if_pattern.search(command)
        condition1 = condition(maches2.group(2))
        if maches2.group(1): spaces = len(maches2.group(1))
        else: spaces = 0
        if condition1 == 'false':
            end_pattern = re.compile(r'\n\s{%s}(\})\n' %spaces)
            maches3 = end_pattern.search(cinput)
            end2 = maches3.end()
            cinput = cinput[end2:]
        else:
            cinput = cinput[ends:]
    elif while_pattern.search(command):
        maches2 = while_pattern.search(command)
        condition1 = condition(maches2.group(2))
        if maches2.group(1): spaces = len(maches2.group(1))
        else: spaces = 0
        end_pattern = re.compile(r'\n\s{%s}(\})\n' %spaces)
        maches3 = end_pattern.search(cinput)
        end2 = maches3.end()
        if condition1 == 'false':
            cinput = cinput[end2:]
        else:
            while condition(maches2.group(2)) == 'true':
                tinput = cinput[ends:end2]
                while tinput:
                    maches4 = command_pattern.search(tinput)
                    ends4 = maches4.end()
                    command2 = maches4.group(1)
                    if create_pattern.search(command2):
                        maches = create_pattern.search(command2)
                        name = maches.group(1)
                        sheets.append(name)
                        column = maches.group(2)
                        row = maches.group(3)
                        exec("{} = tables({}, {})".format(name, int(column), int(row)))
                    elif context_pattern.search(command2):
                        maches = context_pattern.search(command2)
                        context = maches.group(1)
                        s3265= 52
                        if context not in sheets:
                            errors += 1
                    elif setFunc_pattern.search(command2):
                        if context == 0:
                            errors += 1
                        else:
                            maches = setFunc_pattern.search(command2)
                            column = AA2num(maches.group(1))
                            row = int(maches.group(2))-1
                            expFunc = maches.group(3)
                            exec("{}.setFunc({},{},'{}')".format(context, row, column, expFunc))
                    elif setFunc2_pattern.search(command2):
                        if context == 0:
                            errors += 1
                        else:
                            maches = setFunc2_pattern.search(command2)
                            column = maches.group(1)
                            column = AA2num(solver(column))
                            row = maches.group(2)
                            row = int(solver(row))-1
                            expFunc = maches.group(3)
                            exec("{}.setFunc({},{},'{}')".format(context, row, column, expFunc))
                    elif display_pattern.search(command2):
                        maches = display_pattern.search(command2)
                        name = maches.group(1)
                        exec("{}.display()".format(name))
                    elif printt_pattern.search(command2):
                        maches = printt_pattern.search(command2)
                        exp = maches.group(1)
                        exp = solver(exp)
                        print('out:', exp, sep = '')
                    elif setcell_pattern.search(command2):
                        if context == 0:
                            errors += 1
                        else:        
                            maches = setcell_pattern.search(command2)
                            column = AA2num(maches.group(1))
                            row = int(maches.group(2))-1
                            exp = maches.group(3)
                            exp = solver(exp)
                            exec("{}.setcell({},{},'{}')".format(context, row, column, exp))
                    elif setcell2_pattern.search(command2):
                        if context == 0:
                            errors += 1
                        else:
                            maches = setcell2_pattern.search(command2)
                            column = maches.group(1)
                            column = AA2num(solver(column))
                            row = maches.group(2)
                            row = int(solver(row))-1
                            exp = maches.group(3)
                            exp = solver(exp)
                            exec("{}.setcell({},{},'{}')".format(context, row, column, exp))
                    elif setvall_pattern.search(command2):
                        if context == 0:
                            errors += 1
                        else:
                            maches = setvall_pattern.search(command2)
                            key = maches.group(1)
                            exp = maches.group(2)
                            exp = solver(exp)
                            dics[key] = exp
                            #exec("{}.setvall('{}','{}')".format(context, str(key), str(exp)))
                    else:
                        pass
                    tinput = tinput[ends4:]
                    xcs = 5
            cinput = cinput[end2:]
            x235 = 235     
    else:
        if create_pattern.search(command):
            maches = create_pattern.search(command)
            name = maches.group(1)
            sheets.append(name)
            column = maches.group(2)
            row = maches.group(3)
            exec("{} = tables({}, {})".format(name, int(column), int(row)))
        elif context_pattern.search(command):
            maches = context_pattern.search(command)
            context = maches.group(1)
            if context not in sheets:
                errors += 1
        elif setFunc_pattern.search(command):
            if context == 0:
                errors += 1
            else:
                maches = setFunc_pattern.search(command)
                column = AA2num(maches.group(1))
                row = int(maches.group(2))-1
                expFunc = maches.group(3)
                exec("{}.setFunc({},{},'{}')".format(context, row, column, expFunc))
        elif setFunc2_pattern.search(command):
            if context == 0:
                errors += 1
            else:
                maches = setFunc2_pattern.search(command)
                column = maches.group(1)
                column = AA2num(solver(column))
                row = maches.group(2)
                row = int(solver(row))-1
                expFunc = maches.group(3)
                exec("{}.setFunc({},{},'{}')".format(context, row, column, expFunc))
        elif display_pattern.search(command):
            maches = display_pattern.search(command)
            name = maches.group(1)
            exec("{}.display()".format(name))
        elif printt_pattern.search(command):
            maches = printt_pattern.search(command)
            exp = maches.group(1)
            exp = solver(exp)
            print('out:', exp, sep = '')
        elif setcell_pattern.search(command):
            if context == 0:
                errors += 1
            else:        
                maches = setcell_pattern.search(command)
                column = AA2num(maches.group(1))
                row = int(maches.group(2))-1
                exp = maches.group(3)
                exp = solver(exp)
                exec("{}.setcell({},{},'{}')".format(context, row, column, exp))
        elif setcell2_pattern.search(command):
            if context == 0:
                errors += 1
            else:
                maches = setcell2_pattern.search(command)
                column = maches.group(1)
                column = AA2num(solver(column))
                row = maches.group(2)
                row = int(solver(row))-1
                exp = maches.group(3)
                exp = solver(exp)
                exec("{}.setcell({},{},'{}')".format(context, row, column, exp))
        elif setvall_pattern.search(command):
            if context == 0:
                errors += 1
            else:
                maches = setvall_pattern.search(command)
                key = maches.group(1)
                exp = maches.group(2)
                exp = solver(exp)
                dics[key] = exp
                #exec("{}.setvall('{}','{}')".format(context, str(key), str(exp)))
        cinput = cinput[ends:]
        x232 = 262