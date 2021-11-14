from Params import args

class Inventory():
    def __init__(self,args):
        self.args=args
        self.C_01=args.C_01
        self.C_02=args.C_02
        self.C_d=args.C_d
        self.C_h1=args.C_h1
        self.C_h2=args.C_h2
        self.C_m1=args.C_m1
        self.C_c1=args.C_c1
        self.t1=args.t1
        self.t2=args.t2
        self.u=0        #剩余库存
        self.S=args.S
        self.last_tp=0
        self.NP_ts=[]

    def Preventive_replace_KP(self,ts,tp):
        '''
        :param ts: 订购时间点
        :param tp: 预防性维护时间
        :return C ：总成本
        '''
        C = self.C_R1
        if ts+self.t1<=tp:
            t=tp-(ts+self.t1)
            C+=self.C_h1*t
            C+=self.C_01
        else:
            D=ts+self.t1-tp
            C+=self.C_d*D
            C+=self.C_01
        return C,D

    def Falt_replace_KP(self,ts,tp):
        C = self.C_c1
        if ts + self.t1 <=tp:
            t = tp - (ts + self.t1)
            C += self.C_h1 * t
            C += self.C_01
        else:
            D = ts + self.t1 - tp
            C += self.C_d * D
            C += self.C_01
        return C,D

    def Preventive_replace(self, n,tp):
        D=0
        C1=self.check_inven(tp)
        C = self.C_R1*n+C1
        if self.u-n<0:
            K=self.S+n-self.u-len(self.NP_ts)
            if K>0:
                pass
            else:
                K=0
            if self.u+len(self.NP_ts)-n>=0:
                CD=0
                for i in range(n-self.u):
                    CD+=self.C_d*(self.NP_ts[0]+self.t2-tp)
                    D=self.NP_ts[0]
                    del self.NP_ts[0]

            else:
                CD=0
                k=len(self.NP_ts)
                for i in self.NP_ts:
                    CD += self.C_d * (i + self.t2 - tp)
                CD+=self.C_d*(n-self.u-k)
                self.NP_ts=[]
                D=self.t2
            C=C+CD+K*self.C_02+self.C_h2*(tp-self.last_tp)*self.u     #表示更换成本+停机成本+库存成本+订购成本
            self.u=S
        elif self.u-n<self.S and self.u-n>=0:
            K = self.S + n - self.u-len(self.NP_ts)
            if K>0:
                pass
            else:
                K=0
            C=C+K*self.C_02+self.C_h2*(tp-self.last_tp)*self.u      #更换成本+订购成本+库存成本
            self.u=self.S
        else:
            self.u-=n
            C=C+self.C_h2*(tp-self.last_tp)*self.u                  #更换成本+库存成本
        self.last_tp=tp
        return C,D

    def Falt_replace(self,n,tp):
        C1 = self.check_inven(tp)
        C = self.args.C_c2 * n+C1
        D=0
        if self.u - n < 0:
            K = self.S + n - self.u - len(self.NP_ts)
            if K > 0:
                pass
            else:
                K = 0
            if self.u + len(self.NP_ts) - n >= 0:
                CD = 0
                for i in range(n - self.u):
                    CD += self.C_d * (self.NP_ts[0] + self.t2 - tp)
                    D=self.NP_ts[0]
                    del self.NP_ts[0]
            else:
                CD = 0
                k = len(self.NP_ts)
                for i in self.NP_ts:
                    CD += self.C_d * (i + self.t2 - tp)
                CD += self.C_d * (n - self.u - k)
                self.NP_ts = []
                D=self.t2
            C = C + self.C_d * self.t2 + K * self.C_02 + self.C_h2 * (
            tp - self.last_tp) * self.u             # 表示更换成本+停机成本+库存成本+订购成本
            self.u = self.S
        elif self.u - n < self.S:
            K = self.S + n - self.u - len(self.NP_ts)
            if K > 0:
                pass
            else:
                K = 0
            C = C + K * self.C_02 + self.C_h2 * (tp - self.last_tp) * self.u  # 更换成本+订购成本+库存成本
            self.u = self.S
        else:
            self.u -= n
            C = C + self.C_h2 * (tp - self.last_tp) * self.u  # 更换成本+库存成本
        self.last_tp=tp
        return C,D

    def NP_oder(self,ts,n):
        if self.u-n>=self.S:
            pass
        else:
            for i in range(self.S+n-self.u):
                self.NP_ts.append(ts)

    def check_inven(self,tp):
        C=0
        for i in self.NP_ts:
            if i<tp:
                C+=(tp-i)*self.C_h2
                self.u+=1
        return C

Inven=Inventory(args)