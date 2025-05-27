import numpy as np

def fun_load_touchstone(fname):
    """
    Load the scattering parameters from a Touchstone file (.sNp)
    Supports up to 9 ports and 1e5 frequency points. Handles S-parameter formats:
      MA (magnitude/angle), DB (dB/angle), RI (real/imag).

    Automatically detects frequency unit and converts to Hz.

    Parameters:
      fname : str
          Path to the .sNp file. The penultimate character indicates number of ports.

    Returns:
      f : np.ndarray
          1D array of frequencies in Hz.
      S : list of np.ndarray
          List of S-matrices (nports x nports complex) per frequency point.
    """
    # Determine port count from filename, e.g. 'file.4p' -> 4 ports
    try:
        nports = int(fname[-2])
    except Exception:
        raise ValueError("Cannot determine number of ports from filename (expect penultimate digit before 'p').")

    nelements = 2 * nports * nports

    with open(fname, 'r') as f:
        # Find header line starting with '#'
        header = None
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                header = line.lstrip('#').strip()
                break
        if header is None:
            raise ValueError("No header line (starting with '#') found.")

        # Tokenize header: e.g. ['MHz', 'S', 'MA', 'R', '50'] or ['Hz','S','RI','R','46.7']
        parts = header.split()
        if len(parts) < 3 or parts[1].upper() != 'S':
            raise ValueError(f"Unexpected header format: '{header}'")

        # Frequency unit, accept full strings like 'Hz','kHz','MHz', etc.
        unit_key = parts[0].upper()
        unit_map = {
            'HZ': 1,
            'KHZ': 1e3,
            'MHZ': 1e6,
            'GHZ': 1e9,
            'THZ': 1e12,
        }
        if unit_key not in unit_map:
            raise ValueError(f"Unknown frequency unit '{parts[0]}' in header.")
        unit = unit_map[unit_key]

        # S-format: MA, DB, or RI
        s_format = parts[2].upper()
        if s_format not in ('MA', 'DB', 'RI'):
            raise ValueError(f"Unsupported S-parameter format '{parts[2]}'. Use MA, DB, or RI.")

        # Skip to data: skip lines starting with '!', '#' beyond header
        data_lines = []
        for line in f:
            line = line.strip()
            if not line or line.startswith('!') or line.startswith('#'):
                continue
            data_lines.append(line)

    # Parse numeric data
    data = np.fromstring(' '.join(data_lines), sep=' ')
    if data.size == 0:
        raise ValueError("No numeric data found in file.")

    chunk_size = 1 + nelements
    num_points = int(data.size // chunk_size)
    freqs = np.zeros(num_points)
    S_mats = []

    for idx in range(num_points):
        chunk = data[idx*chunk_size:(idx+1)*chunk_size]
        # Convert frequency to Hz
        freqs[idx] = chunk[0] * unit
        vals = chunk[1:]
        # Extract complex values based on format
        if s_format == 'MA':
            mags = vals[0::2]
            angs = np.deg2rad(vals[1::2])
            comps = mags * np.exp(1j * angs)
        elif s_format == 'DB':
            dbs = vals[0::2]
            mags = 10**(dbs/20)
            angs = np.deg2rad(vals[1::2])
            comps = mags * np.exp(1j * angs)
        else:  # RI
            real = vals[0::2]
            imag = vals[1::2]
            comps = real + 1j * imag

        # Reshape and transpose to nports x nports
        S_mat = comps.reshape(nports, nports).T
        S_mats.append(S_mat)

    return freqs, S_mats