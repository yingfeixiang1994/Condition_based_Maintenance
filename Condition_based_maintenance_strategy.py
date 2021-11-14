import numpy as np
from scipy.special import gamma
from scipy import integrate
from Params import args
from Inventory_strategy import Inven
import random
import matplotlib.pyplot as plt

def burden():
    if random.random()<0.8:
        return np.random.normal(loc=30, scale=10, size=1)
    else:
        return random.randrange(60,70,1)

class Maintenance:
    def __init__(self,args):
        self.args=args
        self.L_s=args.L_s
        self.L_c=args.L_c
        self.L_p=args.L_p
        self.Maintenance_times=[0 for _ in range(args.n)]
        self.X_current=[0 for _ in range(args.n)]
        self.current_check=None
        self.KPts=None

    def Maintenace_cost(self,k):
        if k==0:
            return np.power(self.args.a,self.Maintenance_times[k])*self.args.C_m1
        else:
            return np.power(self.args.a, self.Maintenance_times[k]) * self.args.C_m2

    def check(self,X_t,k):
        '''
        :param X_t: 退化量
        :return: TS,PR,M,FR
        '''
        TS=False    #订购判断
        PR=False    #预防性更换
        M=False     #预防性维修
        FR=False    #故障更换
        if X_t>=self.L_p and X_t<self.L_c:
            M_cost=self.Maintenace_cost(k)
            if k==0:
                if M_cost>=self.args.C_R1:   #关键件预防性更换
                    FR=True
                else:                        #关键件预防性维修
                    M=True
            else:
                if M_cost >= self.args.C_R2:  # 关键件预防性更换
                    FR = True
                else:  # 关键件预防性维修
                    M = True
        elif X_t>self.L_c:
            FR=True
        elif X_t>self.L_s :
            TS=True
        return PR,M,FR,TS

    #正常工作状态t时刻的概率密度函数
    def F1(self,t):
        x =t
        return (np.power(self.args.lamda1, self.args.alpha1 ) \
                / gamma(self.args.alpha1 )) * np.power(x, self.args.alpha1 - 1) \
               * np.exp(-self.args.lamda1 * x)

    #超出正常工作状态t时刻的概率密度函数
    def F2(self,t):
        x=t
        return (np.power(self.args.lamda2, self.args.alpha2 ) \
                / gamma(self.args.alpha2 )) * np.power(x, self.args.alpha2  - 1) \
               * np.exp(-self.args.lamda2 * x)

    def main(self):
        Total_cost=0
        Current_T=[0 for _ in range(self.args.n)]
        Last_CT=[0 for _ in range(self.args.n)]
        i=0
        D1,D2,D3=0,0,0
        while i<1000:
            Total_cost+=self.args.C_t
            i+=self.args.delta_t
            Current_T=[_+self.args.delta_t for _ in Current_T]
            PR_set=[]
            M_set=[]
            FR_set=[]
            TS_set=[]
            for j in range(self.args.n):
                self.current_check = j
                if burden()<self.args.D:
                    X_t,err=integrate.quad(self.F1,Last_CT[j],Current_T[j])
                else:
                    X_t, err = integrate.quad(self.F2, Last_CT[j], Current_T[j])
                self.X_current[j] += X_t
                PR, M, FR, TS = self.check(self.X_current[j], j)
                PR_set.append(PR)
                M_set.append(M)
                FR_set.append(FR)
                TS_set.append(TS)
            NPR,NFR,NTS=0,0,0
            for k in range(self.args.n):
                if k==0:
                    if FR_set[k]==True:
                        if self.KPts!=None:
                            C,D1=Inven.Falt_replace_KP(self.KPts,Current_T[k])
                            Total_cost += C
                            self.X_current[k]=0
                            Last_CT[k]=0
                            Current_T[k]=0
                        else:
                            C,D1=Inven.Falt_replace_KP(Current_T[k], Current_T[k])
                            Total_cost += C
                            self.X_current[k] = 0
                            Last_CT[k] = 0
                            Current_T[k] = 0
                        self.KPts=None
                    if  FR_set[k]!=True and PR_set[k]==True:
                        if self.KPts!=None:
                            C,D1=Inven.Preventive_replace_KP(self.KPts,Current_T[k])
                            self.X_current[k] = 0
                            Last_CT[k] = 0
                            Current_T[k] = 0
                        else:
                            C,D1=Inven.Preventive_replace_KP(Current_T[k],Current_T[k])
                            self.X_current[k] = 0
                            Last_CT[k] = 0
                            Current_T[k] = 0
                        self.KPts=None
                    if FR_set[k]!=True and PR_set[k]!=True and M_set[k]==True:
                        C=self.Maintenace_cost(k)
                        Total_cost += C
                        self.X_current[k] = 0
                        Last_CT[k] = 0
                        Current_T[k] = 0
                    if FR_set[k]!=True and PR_set[k]!=True and M_set[k]!=True and TS_set[k]==True:
                        self.ts[k]=Current_T[k]
                    # Total_cost+=C
                else:
                    if FR_set[k]==True:
                        NFR+=1
                        self.X_current[k] = 0
                        Last_CT[k] = 0
                        Current_T[k] = 0
                    if  FR_set[k]!=True and PR_set[k]==True:
                        NPR+=1
                        self.X_current[k] = 0
                        Last_CT[k] = 0
                        Current_T[k] = 0
                    if FR_set[k]!=True and PR_set[k]!=True and M_set[k]==True:
                        C = self.Maintenace_cost(k)
                        Total_cost+=C
                        self.X_current[k] = 0
                        Last_CT[k] = 0
                        Current_T[k] = 0
                    if FR_set[k]!=True and PR_set[k]!=True and M_set[k]!=True and TS_set[k]==True:
                        NTS+=1
            tp=i
            if NPR>0:
                C1,D2=Inven.Preventive_replace(NPR,tp)
                Total_cost+=C1
            if NFR>0:
                C2,D3=Inven.Falt_replace(NFR, tp)
                Total_cost+=C2
            if NTS>0:
                Inven.NP_oder(tp, NTS)
            max_D=max(D1,D2,D3)
            i+=max_D
        return Total_cost




S=[]
TC_list=[]
# m=Maintenance(args)
for i in range(10):
    m = Maintenance(args)
    # try:
    # args.L_s+=0.01
    # args.S+=1
    # print(args.S)
    T=m.main()
    print(T)
    TC_list.append(T)
    S.append( args.S)
    args.S+=1
    # except:
    #     pass
plt.plot(S,TC_list)
plt.show()
def draw_Gamma_graph():
    x=[]
    y=[]
    y1=[]
    L2=[]
    m = Maintenance(args)
    l=[]
    k=0
    for i in range(200):
        # k+=0.1*1
        print(k)
        x.append(k)
        y.append(m.F1(k))
        l1,e=integrate.quad(m.F1,0,k)
        l.append(l1)
        y1.append(m.F2(k))
        l2, e = integrate.quad(m.F2, 0, k)
        L2.append(l2)
        k += 0.1 * 1

    plt.plot(x,y)
    plt.plot(x,l)
    plt.plot(x,y1)
    plt.plot(x,L2)
    plt.show()

# draw_Gamma_graph()