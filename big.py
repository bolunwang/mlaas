from bigml.api import BigML
import csv

api = BigML(dev_mode=True,storage='/Users/YunZhao/Desktop/16FallProject/5dataset/lgr')
#source = api.create_source('/Users/YunZhao/Desktop/16FallProject/5dataset/twitter_spammers.csv')
#api.update_source(source, {"fields": {"your_field_name_or_id": {"optype": "categorical"}}})
#api.ok(source)
#dataset = api.create_dataset(source)
#api.ok(dataset)
csvfile = file('bigml_multi.csv', 'wb')
writer = csv.writer(csvfile)
for x in [1E-15,1E-13,1E-11,1E-9,1E-7,1E-5,1E-3]:
  for y in [1E-8,1E-6,1E-4,1E-2,1,1E2]:
     logistic_regression = api.create_logistic_regression('dataset/58391ead49c4a13ae8000140', {"name": "my logistic regression","eps": x,"regularization": "l2", "c": y})
     api.ok(logistic_regression)
     test_source = api.create_source('/Users/YunZhao/Desktop/16FallProject/5dataset/twitter_spammers.csv')
     api.ok(test_source)
     test_dataset = api.create_dataset(test_source)
     api.ok(test_dataset)
     evaluation = api.create_evaluation(logistic_regression, test_dataset)
     api.ok(evaluation)
 
 

