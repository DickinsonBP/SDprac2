import pandas
import lithops
from lithops.multiprocessing import Pool
from lithops import Storage, FunctionExecutor

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
    dicc = {}

    storage = Storage()
    archivoCsv = storage.get_object(bucket=BUCKET,key=archivo, stream=True)
    datos = pandas.read_csv(archivoCsv)
    #ordenadoPorfecha = datos.sort_values(by='TipusCasData')

    #fecha = datos['TipusCasData'].values_counts()
    #dicc['TipusCasData'] = fecha

    return datos


if __name__ == '__main__':
    '''with FunctionExecutor(config=config) as fexec:
        future = fexec.call_async(tratar_archivo,KEY)
        print(future.result())'''
    fexec = FunctionExecutor(config=config)
    fexec.call_async(tratar_archivo,KEY)
    print(fexec.get_result())