import numpy as np  

def update(R, U, V, lambda_U, lambda_V, K, users, items):
    for i in range(users): 
        V_j = V[:, R[i, :] > 0]
        U[:, i] = np.dot(np.linalg.inv(np.dot(V_j, V_j.T) + lambda_U * np.identity(K)), np.dot(R[i, R[i, :] > 0], V_j.T)) 
    for j in range(items): 
        U_i = U[:, R[:, j] > 0] 
        V[:, j] = np.dot(np.linalg.inv(np.dot(U_i, U_i.T) + lambda_V * np.identity(K)), np.dot(R[R[:, j] > 0, j], U_i.T)) 
    return U,V
    
def train(R, max_round):
    rounds = 0
    global U,V,K,users,items,lambda_U,lambda_V
    while rounds<=max_round:
        rounds = rounds + 1    
        U,V=update(R,U,V,lambda_U,lambda_V,K,users,items)
    return U, V
 
 
"""   
R=[
   [5,3,1,1,4],
   [4,0,0,1,4],
   [1,0,0,5,5],
   [1,3,0,5,0],
   [0,1,5,4,1],
   [1,2,3,5,4]
   ]
"""
R = np.random.randint(0,10,(100,100))
print(R)

K = 2
users = len(R)
items = len(R[0])
lambda_U=0.03
lambda_V=0.03
U = np.random.rand(K, users)
V = np.random.rand(K, items)
U, V=train(R, 500)
# print("P为：\n",U)
# print("Q为：\n",V)
M = np.dot(U.T,V)
print("预测矩阵：\n",M)