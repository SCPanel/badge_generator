class EmailFixer:
    def fix(email: str) -> str:
        '''
        Do e.x.a.m.p.l.e@gmail.com, etc same as example@gmail.com by removing dot's because that's same user on gmail.
        Preventing multi-accounts on one gmail. 
        '''
        if email.endswith("@gmail.com"):
            return "@".join([email.split("@")[0].replace(".", ""), "gmail.com"])
        return email