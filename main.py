import pandas
import lithops
from lithops.multiprocessing import Pool
from lithops import Storage, FunctionExecutor
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker
from collections import OrderedDict

REGION = 'eu-de'
NAMESPACE = 'anna.graciac@estudiants.urv.cat_dev'
API_KEY = "2e728aba-560e-40f1-988b-6965b5ea4579:UDIJT2tLhxF5YKhLi00f1OWFNVN1XSpH1y9SMpJPyUZmPBSDsRMwixt6Qre2YThc"
ACCESS_KEY_ID = '21d22b43d16f4d19b6e5ed4ff9eebaad'
SECRET_ACCESS_KEY = '1ec74d1f3d926d28de2cd6eda3fbbb526c50dfe9840d837e' 
BUCKET = 'covid-dataset'
ENDPOINT = 'https://eu-gb.functions.cloud.ibm.com'
KEY = 'covid-cat.csv'

#configuracion de lithops
config = {'lithops' : {'storage_bucket' : BUCKET},
        'ibm_cf' : {'endpoint' : ENDPOINT, 'namespace' : NAMESPACE, 'api_key' : API_KEY},
        'ibm_cos' : {'region' : REGION, 'access_key' : ACCESS_KEY_ID, 'secret_key' : SECRET_ACCESS_KEY}}


#tratar archivo
def tratar_archivo(archivo):
    casosFecha = {}
    casosSexo = {}
    casosUbicacion = {}
    storage = Storage(config=config)
    archivoCsv = storage.get_object(bucket=BUCKET,key=archivo, stream=True)
    datos = pandas.read_csv(archivoCsv)
    datos = datos.sort_values(by='TipusCasData')

    #añadir datos para casos por fecha
    for clave, valor in datos['TipusCasData'].value_counts().iteritems():
        casosFecha[clave] = valor
    
    for valor, clave in datos['RegioSanitariaDescripcio'].value_counts().iteritems():
        casosUbicacion[clave] = valor

    for valor, clave in datos['SexeDescripcio'].value_counts().iteritems():
        casosSexo[clave] = valor
    
    casosFecha = OrderedDict(sorted(casosFecha.items()))

    dicc = {'Fecha':casosFecha,'Ubicacion': casosUbicacion, 'Sexo': casosSexo}    

    return dicc


if __name__ == '__main__':
    result = {}
    with FunctionExecutor(config=config) as fexec:
        future = fexec.call_async(tratar_archivo,KEY)
        result = future.result()
        print(result['Fecha'])
        #dataX = list(result['Fecha'].keys())
        #dataY = list(result['Fecha'].values())
        #print('Data X: '+str(dataX)+' Data Y: '+str(dataY))
        #plt.plot(dataX,dataY)
        #plt.gcf().autofmt_xdate()
        #plt.xticks(rotation=35)
        #plt.ylabel('infectats por fecha')
        #loc = matplotlib.ticker.LinearLocator(numticks = 10)
        #plt.gca().xaxis.set_major_locator(loc)
        #plt.show()

        '''df = pandas.DataFrame.from_dict(result['Fecha'], orient="index")
        df.to_csv('casosFecha.csv')
        df = pandas.DataFrame.from_dict(result['Ubicacion'], orient="index")
        df.to_csv('casosUbicacion.csv')
        df = pandas.DataFrame.from_dict(result['Sexo'], orient="index")
        df.to_csv('casosSexo.csv')'''