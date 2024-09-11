from datetime import datetime, date
from matplotlib import pyplot as plt
import numpy as np
from bcb import sgs

capital = float(input("Digite o capital investido: "))

frequencia = input("Digite a frquência do período (Y, M, D): ")

inicio = input ("Digite a data inicial maior do que 1995/01/01 no formato YYYY/MM/DD: ")

final = input ("Digite a data final no formato YYYY/MM/DD: ")

data_inicial = datetime.strptime(inicio, "%Y/%m/%d").date()

data_final = datetime.strptime(final, "%Y/%m/%d").date()

taxas_selic = sgs.get({"selic":11}, start= data_inicial, end = data_final)

taxas_selic = taxas_selic/100

capital_acumulado = capital + (1 + taxas_selic["selic"]).cumprod() - 1

capital_com_frquencia = capital_acumulado.resample(frequencia).last()