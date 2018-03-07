import os
import psutil
import numpy as np
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
    indices = x_.indices + x.shape[1]
    indices = np.concatenate((x.indices, indices))
    indptr = x_.indptr[1:] + len(x.data)
    indptr = np.concatenate((x.indptr, indptr))
    return csr_matrix((data, indices, indptr))