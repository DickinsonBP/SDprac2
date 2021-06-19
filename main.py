from genericpath import exists
from logging.config import dictConfig
import pandas
import lithops
from lithops.multiprocessing import Pool
from lithops import Storage, FunctionExecutor
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker
from collections import OrderedDict

#configuracion de lithops
config = {'lithops' : {'storage_bucket' : BUCKET},
        'ibm_cf' : {'endpoint' : ENDPOINT, 'namespace' : NAMESPACE, 'api_key' : API_KEY},
        'ibm_cos' : {'region' : REGION, 'access_key' : ACCESS_KEY_ID, 'secret_key' : SECRET_ACCESS_KEY}}


#tratar archivo
def tratar_archivo(archivo):
    casosFecha = {}
    casosSexo = {}
    casosComarca = {}
    dicc = {}
    
    storage = Storage(config=config)
    archivoCsv = storage.get_object(bucket=BUCKET,key=archivo, stream=True)
    datos = pandas.read_csv(archivoCsv)
    datos = datos.sort_values(by='TipusCasData')

    #añadir datos para casos por fecha
    #primero se ordenan bien por fecha
    datos['TipusCasData'] = pandas.to_datetime(datos['TipusCasData'], format= '%d/%m/%Y').dt.date
    if('TipusCasData' in datos):
        for clave, valor in datos['TipusCasData'].value_counts().iteritems():
            casosFecha[clave] = valor
    
    casosComarca = {'Comarca':'Casos'}
    if('ComarcaDescripcio'in datos):
        for clave, valor in datos['ComarcaDescripcio'].value_counts().iteritems():
            casosComarca[clave] = valor

    if('SexeDescripcio' in datos):
        for clave, valor in datos['SexeDescripcio'].value_counts().iteritems():
            casosSexo[clave] = valor
    
    casosFecha = OrderedDict(sorted(casosFecha.items()))

    dicc = {'Fecha':casosFecha,'Comarca':casosComarca, 'Sexo': casosSexo}

    return dicc


if __name__ == '__main__':
    result = {}
    nombresCsv = []
    with FunctionExecutor(config=config) as fexec:
        for i in KEY:
            future = fexec.call_async(tratar_archivo,i)
            result = future.result()
        for i in result.keys():
                nombre = 'datos/'+str(i)+'.csv'
                nombresCsv.append(nombre)
                with open(nombre, 'w') as f:
                    writer = csv.writer(f)
                    for k, v in result[i].items():
                        writer.writerow([k, v])
                if(i not in 'Comarca'):
                    x = list(result[i].keys())
                    y = list(result[i].values())
                    plt.plot(x,y)
                    plt.ylabel('Infectados',fontsize=10)
                    plt.xticks(rotation=16)
                    plt.xlabel('Casos por '+str(i),fontsize=10)
                    plt.figure()
        plt.show()

