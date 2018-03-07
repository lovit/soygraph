import os
import psutil
import numpy as np
from collections import defaultdict
from scipy.sparse import csr_matrix

def get_available_memory():
    """It returns remained memory as percentage"""

    mem = psutil.virtual_memory()
    return 100 * mem.available / (mem.total)

def get_process_memory():
    """It returns the memory usage of current process"""
    
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 ** 3)

def bow_to_graph(x):
    """It transform doc-term sparse matrix to graph.
    Vertex = [doc_0, doc_1, ..., doc_{n-1}|term_0, term_1, ..., term_{m-1}]

    Arguments
    ---------
    x: scipy.sparse

    Returns
    -------
    g: scipy.sparse.csr_matrix
        V` = x.shape[0] + x.shape[1]
        its shape = (V`, V`)
    """
    x = x.tocsr()
    x_ = x.transpose().tocsr()
    data = np.concatenate((x.data, x_.data))
    indices = np.concatenate(
        (x.indices + x.shape[0] , x_.indices))
    indptr = np.concatenate(
        (x.indptr, x_.indptr[1:] + len(x.data)))
    return csr_matrix((data, indices, indptr))

def matrix_to_dict(m):
    """It transform sparse matrix (scipy.sparse.matrix) to dictdict"""
    d = defaultdict(lambda: {})
    for f, (idx_b, idx_e) in enumerate(zip(m.indptr, m.indptr[1:])):
        for idx in range(idx_b, idx_e):
            d[f][g.indices[idx]] = m.data[idx]
    return dict(d)