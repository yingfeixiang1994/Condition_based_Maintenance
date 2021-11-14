import random
import argparse

#Parameters Initialization
parser=argparse.ArgumentParser()

#cost parameters
parser.add_argument("--C_01",type=float,default=12000,help="单个关键件订购费用")
parser.add_argument("--C_02",type=float,default=1500,help="单个非关键件订购费用")
parser.add_argument("--C_d",type=float,default=4000,help="停机成本")
parser.add_argument("--C_h1",type=float,default=150,help="关键件的库存成本")
parser.add_argument("--C_h2",type=float,default=15,help="非关键件的库存成本")
parser.add_argument("--C_m1",type=float,default=5000,help="关键件预防性维修成本")
parser.add_argument("--C_c1",type=float,default=8000,help="关键件故障更换成本")
parser.add_argument("--C_m2",type=float,default=600,help="非关键件预防性维修成本")
parser.add_argument("--C_c2",type=float,default=1000,help="非关键件故障更换成本")
parser.add_argument("--t1",type=int,default=60,help="关键件提前期")
parser.add_argument("--t2",type=float,default=50,help="非关键件提前期")
parser.add_argument("--C_R1",type=float,default=3000,help="关键件的预防性更换")
parser.add_argument("--C_R2",type=float,default=500,help="非关键件的预防性更换")
parser.add_argument("--n",type=int,default=20,help="部件个数")
parser.add_argument("--a",type=float,default=1.25,help="系数")
parser.add_argument("--T",type=int,default=30,help="循环")
parser.add_argument("--alpha1",type=int,default=7.5,help="正常工作范围内的形状参数")
parser.add_argument("--alpha2",type=int,default=2,help="超出工作范围内的形状参数")
parser.add_argument("--lamda1",type=int,default=1,help="正常工作范围内的尺度参数")
parser.add_argument("--lamda2",type=int,default=2,help="超出工作范围内的形状参数")
parser.add_argument("--delta_t",type=int,default=5,help="周期检测时间")
parser.add_argument("--I",type=int,default=1000,help="完整周期")
parser.add_argument("--D",type=int,default=60,help="负载阈值")
parser.add_argument("--L_s",type=float,default=0.3,help="更换退化阈值")
parser.add_argument("--S",type=int,default=5,help="安全库存")
parser.add_argument("--C_t",type=int,default=200,help="检查成本")
# Degradation Parameters
parser.add_argument("--L_p",type=float,default=0.8)       #预防性更换
parser.add_argument("--L_c",type=float,default=1,help="Fault threshold")    #故障更换

args=parser.parse_args()
# print(args.C_i)