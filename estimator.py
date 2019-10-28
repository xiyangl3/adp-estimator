import numpy as np
import scipy.io as sio

from scipy.special import comb


dic_list_cheb_2z_1 = np.load('dic_list_cheb_2z_1.npy')
dic_list_cheb_z = np.load('dic_list_cheb_z.npy')


coeff_uk = sio.loadmat('coeff_uk.mat')['coeff2']
coeff_vk = sio.loadmat('coeff_vk.mat')['coeff1']
coeff_absx = sio.loadmat('coeff_absx.mat')['coeff_absx']


def MVUE_p_to_k(p, k, n):
#     p*(p-1/n)* .... *(p-(k-1)/n)
    output = 1
    for i in range(k):
        output *= p-i/n
    return output

def MVUE_ep_q_j(p,q,j,n,epsilon):
    output = 0
    for k in range(0,j+1):
        output+=comb(j,k)* MVUE_p_to_k(p, k,n)*np.exp(epsilon*k)*(-1)**(j-k)*MVUE_p_to_k(q, j-k,n)
    return output


def poly1(K, p, q, n, epsilon, c_1, coeff):
    Delta2 = 2 * c_1 * np.log(n) / n

    powers_p = []
    for i in range(K + 1):
        powers_p.append(np.exp(i * epsilon) * MVUE_p_to_k(p, i, n) / (Delta2 ** i))
    powers_q = []
    for i in range(K + 1):
        powers_q.append(  MVUE_p_to_k(q, i, n) / (Delta2 ** i))

    chebs_x = []
    for i in range(K + 1):
        output = 0
        for key, value in dic_list_cheb_2z_1[i].items():
            output += value * (powers_p[key[0]])
        chebs_x.append(output)
    chebs_y = []
    for i in range(K + 1):
        output = 0
        for key, value in dic_list_cheb_2z_1[i].items():
            output += value * (powers_q[key[0]])
        chebs_y.append(output)

    res = 0
    for i in range(K + 1):
        for j in range(K + 1):
            res += coeff[i][j] * chebs_y[i] * chebs_x[j]
    return res


def P1(K, p, q, n, epsilon, c_1):
    Delta2 = 2 * c_1 * np.log(n) / n
    h2k = poly1(K, p, q, n, epsilon, c_1, coeff_vk) * poly1(K, p, q, n, epsilon, c_1, coeff_uk)
    h00 = poly1(K, 0, 0, n, epsilon, c_1, coeff_vk) * poly1(K, 0, 0, n, epsilon, c_1, coeff_uk)
    return Delta2*(h2k - h00)


def P2(K, p2, q2, p1, q1, n, epsilon, c_1):
    coeff = coeff_absx[K][0].ravel()
    powers_ep_q = []
    W = np.sqrt(8 * c_1 * np.log(n) / n) * (np.sqrt(np.exp(epsilon) * p1 + q1))
    for i in range(K + 1):
        powers_ep_q.append(MVUE_ep_q_j(p2, q2, i, n, epsilon) / (W**i))
    chebs_ep_q = []
    for i in range(K + 1):
        output = 0
        for key, value in dic_list_cheb_z[i].items():
            output += value * (powers_ep_q[key[0]])
        chebs_ep_q.append(output)
    res = 0
    for i in range(len(coeff)):
        res += coeff[i] * chebs_ep_q[i]

    out = 0.5 * W * res + (q2 - np.exp(epsilon) * p2) / 2
    return out




def mle_estimator(count1, count2,n1,n2, epsilon):


    delta = 0
    support = count1.keys()
    for event in support:

        p = count1[event]/n1
        q = count2[event]/n2

        delta = delta + max(q-np.exp(epsilon)*p,0)



    return delta


def opt_estimator(count1, count2, count12, count22,n1, n2, n12, n22, n,epsilon, c_1 = 4, c_2 = 0.1, c_3 = 1.5):

    K = int(np.floor(c_3 * np.log(n)))
    support = count1.keys()
    delta_sum = 0
    for event in support:

        p1 = count1[event] / n1
        q1 = count2[event] / n2

        p2 = count12[event] / n12
        q2 = count22[event] / n22

        threshold = np.sqrt((c_1 + c_2) * np.log(n) / n)
        delta =0
        if np.sqrt(q1) - np.exp(0.5*epsilon) * np.sqrt(p1) < -threshold:
            delta = 0
        elif np.sqrt(q1) - np.exp(0.5*epsilon) * np.sqrt(p1) > threshold:
            delta = q2 - np.exp(epsilon) * p2
        elif np.exp(epsilon) * p1 + q1 < c_1 * np.log(n) / n:
            delta = P1(K, p2, q2, n, epsilon, c_1)
        elif np.abs(np.sqrt(q1) - np.exp(0.5*epsilon) * np.sqrt(p1)) <= threshold and np.exp(
                epsilon) * p1 + q1 >= c_1 * np.log(n) / n:
            delta = P2(K, p2, q2, p1, q1, n, epsilon, c_1)

        delta_sum += delta
        delta_sum = max(min(delta_sum,1), 0)

    return delta_sum

