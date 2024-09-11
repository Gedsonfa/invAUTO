from datetime import datetime, date
from matplotlib import pyplot as plt
import numpy as np
from bcb import sgs

data_inicial = date(2000, 1, 1)

data_final = date(2022, 3, 31)

taxas_selic = sgs.get({"selic":11}, start= data_inicial, end = data_final)/100

print(taxas_selic)