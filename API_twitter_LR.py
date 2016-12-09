import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json 
import csv



# def json_to_csv(json_name,outfile):
#     data = json.loads(json_name)
#     print data
#     writer = csv.writer(outfile,delimiter=',')

#     for row in json_name:
#         writer.writerow(row)
#     return
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        # elif type(x) is list:
        #     i = 0
        #     for a in x:
        #         flatten(a, name + str(i) + '_')
        #         i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


index = [1E-15,1E-11,1E-09,1E-07,1E-5,1E-3]
index2 = [1E-08,1E-06,1E-04,1E-02,0,1,100]
for Optimization in index:
    for L1 in index2:
        for L2 in index2:
            data =  {
                    "GlobalParameters": {
                    "Optimization tolerance": Optimization,
                    "L1 regularization weight": L1,
                    "L2 regularization weight": L2,
            }
                }

            body = str.encode(json.dumps(data))

            url = 'https://ussouthcentral.services.azureml.net/workspaces/61e69c946deb46649f26c488452887c0/services/d817d49c013b4b3182d72d0d9ec27dd5/execute?api-version=2.0&details=true'
            api_key = 'ot7NfQ7WjQa1SJ3psPXk+NrAWEBR6x8ft0XJhjdiMKTnQGe1E9q+j02pXjWZ3FqZUevMYLDlUVsekPVcFDTAHg==' # Replace this with the API key for the web service
            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

            req = urllib2.Request(url, body, headers) 

            try:
                response = urllib2.urlopen(req)

                # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
                # req = urllib.request.Request(url, body, headers) 
                # response = urllib.request.urlopen(req)

                result = response.read()
                json_name = json.loads(result)
                new_dic = flatten_json(json_name)
                new_list = new_dic["Results_output1_value_Values"][-2]
                new_list.append(Optimization)
                new_list.append(L1)
                new_list.append(L2)
                with open('dict.csv', 'a') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(new_list)

            except urllib2.HTTPError, error:
                print("The request failed with status code: " + str(error.code))

                # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
                print(error.info())

                print(json.loads(error.read()))       