
import sys
import dill
import numpy as np
import mfcc
import scipy.io.wavfile as wave
from pylab import *


def seq_frame(input, ind, n):
    x,y = input.shape[0],input.shape[1]
    f = np.zeros((n,y))
    pos = int(n/2)
    f[pos] = input[ind]
    if (ind < pos):
        f[(pos-ind):pos,:] = input[0:ind,:]
        f[pos+1:,:] = input[ind+1:ind+pos+1,:]
    elif ((x-ind-1) < (pos) ):
        f[(pos+1):(pos+x-ind),:] = input[ind+1:,:]
        f[0:pos,:] = input[ind-pos:ind,:]
    else:
        f[0:pos,:] = input[ind-pos:ind,:]
        f[pos+1:,:] = input[ind+1:ind+pos+1,:]
    return f

def seq_frame_word(input,n):
    frame = seq_frame(input,0,n).reshape(1,600)
    for i in range(1,len(input)):
        frame_aux = seq_frame(input,i,n).reshape(1,600)
        frame = np.concatenate([frame,frame_aux])
    return frame

def extrair(arquivo):
    rate = 8000
    sinal = wave.read(arquivo, mmap = 'false')
    m = mfcc.mfcc(200,rate,13)
    return m.extrair_fbank_mel(sinal[1])

def verificar(observacao):
    resultados = np.zeros(5)
    lista = ["avance","direita",'esquerda','pare','recue']
    resultados[0] = modelo_avance.forward(observacao)[1]
    resultados[1] = modelo_direita.forward(observacao)[1]
    resultados[2] = modelo_esquerda.forward(observacao)[1]
    resultados[3] = modelo_pare.forward(observacao)[1]
    resultados[4] = modelo_recue.forward(observacao)[1]
    ind = np.argmax(resultados)
    return lista[ind],ind, resultados

n = 15
def id_fonema(f):
    fonemas = np.array(["a","v","an","c","i","p","r","rr","e","k","u","d","e_c","t","s","sil"])
    return int(np.where(fonemas == f)[0][0])

def classificar(audio):

    sinal = seq_frame_word(extrair(audio),n)
    resultado, ind, prob = verificar(sinal)
    return resultado

batch_size = 100
with open('rede.pkl', 'rb') as f:
    rede = dill.load(f)

with open('modelo_avance_cnn.pkl', 'rb') as f:
    modelo_avance = dill.load(f)
with open('modelo_recue_cnn.pkl', 'rb') as f:
    modelo_recue = dill.load(f)
with open('modelo_pare_cnn.pkl', 'rb') as f:
    modelo_pare = dill.load(f)
with open('modelo_direita_cnn.pkl', 'rb') as f:
    modelo_direita = dill.load(f)
with open('modelo_esquerda_cnn.pkl', 'rb') as f:
    modelo_esquerda = dill.load(f)
