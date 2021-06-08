import pandas
import lithops
from lithops.multiprocessing import Pool
from lithops import Storage, FunctionExecutor

REGION = 'eu-de'
NAMESPACE = 'anna.graciac@estudiants.urv.cat_dev'
API_KEY = "2e728aba-560e-40f1-988b-6965b5ea4579:UDIJT2tLhxF5YKhLi00f1OWFNVN1XSpH1y9SMpJPyUZmPBSDsRMwixt6Qre2YThc"
ACCESS_KEY_ID = '21d22b43d16f4d19b6e5ed4ff9eebaad'
SECRET_ACCES_KEY = '1ec74d1f3d926d28de2cd6eda3fbbb526c50dfe9840d837e' 
BUCKET = 'covid-dataset'
ENDPOINT = 'https://eu-de.functions.cloud.imb.com'
KEY = 'covid-cat.csv'

#configuracion de lithops
config = {'lithops' : {'storage_bucket' : BUCKET},
        'ibm_cf' : {'endpoint' : ENDPOINT, 'namespace' : NAMESPACE, 'api_key' : API_KEY},
        'ibm_cos' : {'region' : REGION, 'acces_key' : ACCESS_KEY_ID, 'secret_key' : SECRET_ACCES_KEY}}
#leer archivo
def obtener_file(key, config):
    dicc = {}
    storage = Storage(config=config)
    
    #obtener dict lithops de conf para obtener el bucket name
    lithp = config["lithops"]
    bucket = lithp["storage_bucket"]
    archivo = storage.get_object(bucket=bucket, key=key, stream=True)

    #extraer datos del csv y ordenarlos por fecha
    datos = pandas.read_csv(archivo)
    fecha = datos.sort_values(by = 'TipusCasData')

    #el value counts devuelve 
    fecha = datos['TipusCasData'].values_counts()
    dicc['TipusCasData'] = fecha

    return dicc


if __name__ == '__main__':
    with FunctionExecutor(config=config) as fexec:
        future = fexec.call_async(obtener_file, (KEY, config))
        dicc = future.result()
        print(dicc)