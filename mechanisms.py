# This file is built upon https://github.com/cmla-psu/statdp/tree/master/statdp.


import numpy as np

def noisy_max_v1a(queries, epsilon):
    # find the largest noisy element and return its index
    # range: 0,1,...,num_queries-1 1-dimensional discrete
    return (np.asarray(queries, dtype=np.float32) + np.random.laplace(scale=2.0 / epsilon, size=len(queries))).argmax()


def noisy_max_v1b(queries, epsilon):
    # INCORRECT: returning maximum value instead of the index
    # range: 1-dimensional continuous
    return (np.asarray(queries, dtype=np.float32) + np.random.laplace(scale=2.0 / epsilon, size=len(queries))).max()


def noisy_max_v2a(queries, epsilon):
    # range: 0,1,...,num_queries-1 1-dimensional discrete
    return (np.asarray(queries, dtype=np.float32) + np.random.exponential(scale=2.0 / epsilon, size=len(queries))).argmax()


def noisy_max_v2b(queries, epsilon):
    # INCORRECT: returning the maximum value instead of the index
    # range: 1-dimensional continuous
    return (np.asarray(queries, dtype=np.float32) + np.random.exponential(scale=2.0 / epsilon, size=len(queries))).max()


def histogram_eps(queries, epsilon):
    # INCORRECT: using (epsilon) noise instead of (1 / epsilon)
    noisy_array = np.asarray(queries, dtype=np.float32) + np.random.laplace(scale=epsilon, size=len(queries))
    # return noisy_array
    return noisy_array[0]


def histogram(queries, epsilon):
    noisy_array = np.asarray(queries, dtype=np.float32) + np.random.laplace(scale=1.0 / epsilon, size=len(queries))
    # return noisy_array
    return noisy_array[0]


def laplace_mechanism(queries, epsilon):
    noisy_array = np.asarray(queries, dtype=np.float32) + np.random.laplace(scale=len(queries) / epsilon, size=len(queries))
    # return noisy_array
    return np.count_nonzero(np.logical_and(noisy_array > 0.73, noisy_array < 1.75))

def SVT(queries, epsilon, N, T):
    out = []
    eta1 = np.random.laplace(scale=2.0 / epsilon)
    noisy_T = T + eta1
    c1 = 0
    for query in queries:
        eta2 = np.random.laplace(scale=4.0 * N / epsilon)
        if query + eta2 >= noisy_T:
            out.append(True)
            c1 += 1
            if c1 >= N:
                break
        else:
            out.append(False)
    return out


def iSVT1(queries, epsilon, T):
    out = []
    delta = 1
    eta1 = np.random.laplace(scale=2.0 * delta / epsilon)
    noisy_T = T + eta1
    for query in queries:
        # INCORRECT: no noise added to the queries
        eta2 = 0
        if (query + eta2) >= noisy_T:
            out.append(True)
        else:
            out.append(False)


    return out


def iSVT2(queries, epsilon, T):
    out = []
    delta = 1
    eta1 = np.random.laplace(scale=2.0 * delta / epsilon)
    noisy_T = T + eta1
    for query in queries:
        # INCORRECT: noise added to queries doesn't scale with N
        eta2 = np.random.laplace(scale=2.0 * delta / epsilon)
        if (query + eta2) >= noisy_T:
            out.append(True)
            # INCORRECT: no bounds on the True's to output
        else:
            out.append(False)

    return out


def iSVT3(queries, epsilon, N, T):
    out = []
    delta = 1
    eta1 = np.random.laplace(scale=4.0 * delta / epsilon)
    noisy_T = T + eta1
    c1 = 0
    for query in queries:
        # INCORRECT: noise added to queries doesn't scale with N
        eta2 = np.random.laplace(scale=(4.0 * delta) / (3.0 * epsilon))
        if query + eta2 > noisy_T:
            out.append(True)
            c1 += 1
            if c1 >= N:
                break
        else:
            out.append(False)

    return out


def iSVT4(queries, epsilon, N, T):
    out = []
    eta1 = np.random.laplace(scale=2.0 / epsilon)
    noisy_T = T + eta1
    c1 = 0
    for query in queries:
        eta2 = np.random.laplace(scale=2.0 * N / epsilon)
        if query + eta2 > noisy_T:
            # INCORRECT: Output the noisy query instead of True
            out.append(query + eta2)
            c1 += 1
            if c1 >= N:
                break
        else:
            out.append(False)
    return out

def Sparse(queries, epsilon, N, T, delta):
    out = []

    if delta == 0:

        sigma = 2*N/epsilon
    else:

        sigma = np.sqrt(32*N*np.log(2/delta))/epsilon


    noisy_T = T + np.random.laplace(scale=sigma)

    c1 = 0
    for query in queries:
        eta2 = np.random.laplace(scale=2*sigma)
        if query + eta2 >= noisy_T:
            out.append(True)
            c1 += 1
            noisy_T = T+np.random.laplace(scale=sigma)
            if c1 >= N:
                break
        else:
            out.append(False)
    return out

def truncated_geometric(queries, epsilon,delta):
    # N=0,1,2,3
    out = []
    alpha = 1/np.exp(epsilon)
    sups = (-3,-2,-1,0,1,2,3)
    left = (1-(1-alpha)/(1+alpha)*alpha*2-(1-alpha)/(1+alpha)-(1-alpha)/(1+alpha)*alpha**2*2)/2
    probs = (  left  ,(1-alpha)/(1+alpha)*alpha**2,(1-alpha)/(1+alpha)*alpha,(1-alpha)/(1+alpha),(1-alpha)/(1+alpha)*alpha,(1-alpha)/(1+alpha)*alpha**2, left   )

    Ys = np.random.choice(a=sups,size = len(queries), p=probs, replace =True)
    for i in range(len(queries)):
        query = queries[i]
        Y1 = Ys[i]
        if np.random.rand()>=delta:
            if Y1+query>=2:
                out.append(2)
            elif Y1+query<=0:
                out.append(0)
            else:
                out.append(Y1+query)
        else:
            out.append(query)
    return np.asarray(out)

