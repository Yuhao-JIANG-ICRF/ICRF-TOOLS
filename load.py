#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 09:40:00 2025

@author: YJ281217
"""

import numpy as np

def fun_load_touchstone(fname):
    """
    Load the scattering parameters of a touchstone file
    with module in natural units and argument in degrees.
    It can handle up to 9 ports and 1e5 frequency points.
    
    Parameters:
      fname : str
          Name of the touchstone file. Assumes that the second last
          character of the file name indicates the number of ports.
    
    Returns:
      f : numpy.ndarray
          1D array of frequency points (in Hz, after applying unit scaling).
      S : list of numpy.ndarray
          List of scattering matrices. Each matrix is of shape (nports, nports).
    """

    try:
        nports = int(fname[-2])
    except Exception as e:
        raise ValueError("Cannot determine number of ports from filename.") from e

    nelements = 2 * nports * nports  

    with open(fname, 'r') as f:
        header_line = None
        for line in f:
            if line.startswith('#'):
                header_line = line.strip()
                break
        if header_line is None:
            raise ValueError("No header line (starting with '#') found in file.")

        
        trimmed = header_line[1:].lstrip()
        if not trimmed:
            raise ValueError("Header line is empty after '#'.")

        
        unit_letter = trimmed[0]
        unit_mapping = {'H': 1, 'k': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}
        if unit_letter in unit_mapping:
            unit = unit_mapping[unit_letter]
        else:
            raise ValueError("Error: wrong unit.")

        
        if len(trimmed) < 8 or trimmed[4:8] != "S MA":
            raise ValueError("Error: wrong format.")

        
        data_lines = []
        for line in f:
            line = line.strip()
            if line.startswith('!') or line.startswith('#') or not line:
                continue
            data_lines.append(line)

    
    data_str = " ".join(data_lines)
    data = np.fromstring(data_str, sep=' ')
    if data.size == 0:
        raise ValueError("No numeric data found in file.")

    
    chunk_size = 1 + nelements
    num_chunks = int(data.size // chunk_size)
    freq_points = []
    S_matrices = []

    for i in range(num_chunks):
        chunk = data[i*chunk_size : (i+1)*chunk_size]

        freq = chunk[0] * unit
        freq_points.append(freq)
        
   
        amplitudes = chunk[1::2]
        arguments = chunk[2::2]

        Xtmp = amplitudes * np.exp(1j * np.deg2rad(arguments))

        S_matrix = np.reshape(Xtmp, (nports, nports)).T
        S_matrices.append(S_matrix)

    return np.array(freq_points), S_matrices