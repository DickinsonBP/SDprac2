import pandas
from lithops.multiprocessing import Pool
from lithops import Storage, FunctionExecutor

REGION = 'eu-de'
NAMESPACE = 'anna.graciac@estudiants.urv.cat_dev'
API_KEY = "7GRiz9Ifl-8di9MZF9kP1IAci8M7kk0ytrJAGJrKjs0c"
ACCESS_KEY_ID = '21d22b43d16f4d19b6e5ed4ff9eebaad'
SECRET_ACCES_KEY = '1ec74d1f3d926d28de2cd6eda3fbbb526c50dfe9840d837e' 
BUCKET = 'covid-dataset'
ENDPOINT = 'https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints'
FILE_CSV = 'covid-muni-sex.csv'

#configuracion de lithops
conf = {'lithops':{'storage_bucket':BUCKET},
        'ibm_cf':{'endpoint':ENDPOINT,
                    'namespace':NAMESPACE,
                    'api_key':API_KEY},
        'ibm_cos':{'region':REGION,
                    'acces_key':ACCESS_KEY_ID,
                    'secret_key':SECRET_ACCES_KEY}}
#leer archivo
def obtener_file(archivo, conf):
    dicc = {}
    storage = Storage(config=conf)
    
    #obtener dict lithops de conf para obtener el bucket name
    lithp = conf["lithops"]
    bucket = lithp["storage_bucket"]
    archivo = storage.get_object(bucket=bucket, key=file, stream=True)

    #extraer datos del csv y ordenarlos por fecha
    datos = pandas.read_csv(archivo)
    fecha = datos.sort_values(by = 'TipusCasData')

    #el value counts devuelve 
    fecha = datos['TipusCasData'].values_counts()
    dicc['TipusCasData'] = fecha


    return dicc


if __name__ == '__main__':
    with FunctionExecutor() as fexec:
        fut = fexec.call_async(obtener_file, (FILE_CSV, conf))