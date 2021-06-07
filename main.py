import time
#from multiprocessing import Pool
from lithops.multiprocessing import Pool
from lithops import FunctionExecutor

REGION = 'eu-de'
NAMESPACE = 'anna.graciac@estudiants.urv.cat_dev'
API_KEY = "7GRiz9Ifl-8di9MZF9kP1IAci8M7kk0ytrJAGJrKjs0c"
ACCESS_KEY_ID = '21d22b43d16f4d19b6e5ed4ff9eebaad'
SECRET_ACCES_KEY = '1ec74d1f3d926d28de2cd6eda3fbbb526c50dfe9840d837e' 
BUCKET = 'covid-dataset'
ENDPOINT = 'https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints'



def f(x):
    time.sleep(10)
    return x*x


if __name__ == '__main__':
    with Pool() as p:
        print(p.map(f,range(100)))

'''def hello(name):
    return 'Hello {}!'.format(name)

with FunctionExecutor() as fexec:
    future = fexec.call_async(hello,'World')
    print(future.result())'''