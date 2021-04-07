import numpy as np
from scipy.optimize import linprog
from os.path import join,pardir,abspath
import csv
from enum import Enum 


input_filename=abspath(join(__file__,pardir,"tmp","input.csv"))
output_filename=abspath(join(__file__,pardir,"tmp","output.csv"))

class Constraint:
  def __init__(self,x,y,z,op,num):
    self.x=x #-100~100
    self.y=y #-100~100
    self.z=z #-100~100
    self.op=op #"=","<=",">="
    self.num=num

class Target:
  def __init__(self,x,y,z,goal):
    self.x=x #-100~100
    self.y=y #-100~100
    self.z=z #-100~100
    self.goal=goal #"Minimize","Maximize"

class Abnormal(Enum):
  ITERATION_LIMIT=1
  INFEASIBLE=2
  UNBOUNDED=3
  NUMERICAL_ERROR=4
ITERATION_LIMIT=Abnormal.ITERATION_LIMIT
INFEASIBLE=Abnormal.INFEASIBLE
UNBOUNDED=Abnormal.UNBOUNDED
NUMERICAL_ERROR=Abnormal.NUMERICAL_ERROR

def get_A_b(constraints):
  A_eq=[]
  b_eq=[]
  A_ub=[] 
  b_ub=[]
  for const in constraints:
    if const.op=="=":
      A_eq.append(np.array([const.x,const.y,const.z]))
      b_eq.append(const.num)
    elif const.op=="<=":
      A_ub.append(np.array([const.x,const.y,const.z]))
      b_ub.append(const.num)
    elif const.op==">=":
      A_ub.append(np.array([-const.x,-const.y,-const.z]))
      b_ub.append(-const.num)
  kwargs={}
  if A_eq!=[]:
    kwargs["A_eq"]=np.stack(A_eq)
    kwargs["b_eq"]=np.array(b_eq)
  if A_ub!=[]:
    kwargs["A_ub"]=np.stack(A_ub)
    kwargs["b_ub"]=np.array(b_ub)
  return kwargs

def get_c(target):
  if target.goal=="Minimize":
    return np.array([target.x,target.y,target.z])
  elif target.goal=="Maximize":
    return np.array([-target.x,-target.y,-target.z])

def solve(target,constraints):
  sol=linprog(get_c(target),**get_A_b(constraints))
  if sol.status==1:
    return ITERATION_LIMIT
  if sol.status==2:
    return INFEASIBLE
  if sol.status==3:
    return UNBOUNDED
  if sol.status==4:
    return NUMERICAL_ERROR
  return [round(float(x),4) for x in sol.x]

def main():
  target=None
  constraints=[]
  with open(input_filename,'r',newline='') as f:
    reader=csv.reader(f)
    for i,row in enumerate(reader):
      print(i,row)
      if i==0:
        target=Target(float(row[1]),float(row[2]),float(row[3]),row[0])
      else:
        const=Constraint(float(row[0]),float(row[1]),float(row[2]),row[3],float(row[4]))
        constraints.append(const)
    print("finished reading input.csv")
  sol=solve(target,constraints)
  if type(sol)==Abnormal:
    print(sol.name)
    with open(output_filename,'w',newline='') as f:
      writer=csv.writer(f)
      writer.writerow([sol.name,sol.name,sol.name])
  else:
    print("Solution: ({},{},{})".format(sol[0],sol[1],sol[2]))
    sol_in_str=[str(x) for x in sol]
    with open(output_filename,'w',newline='') as f:
      writer=csv.writer(f)
      writer.writerow(sol_in_str)
  print("finished writing output.csv")
  print()

main()

    