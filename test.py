import requests
dictToSend = {'status':'what is the answer?'}
res = requests.post('http://localhost:5000/soc', json=dictToSend)