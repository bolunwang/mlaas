#Google prediction api need Oauth tokens / user authorisation and require training data to be uploaded on Google Cloud.
#Usage: python filename locationOfTrainingData modelID projectID
#Usage eg: python gpa_predict_baseball.py mlaas/baseball.csv prisubmit mlass-148223
from __future__ import print_function

import argparse
import os
import pprint
import sys
import time

from apiclient import discovery
from apiclient import sample_tools
from oauth2client import client


# Time to wait (in seconds) between successive checks of training status.
SLEEP_TIME = 10


# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('object_name',
    help='Full Google Storage path of csv data (ex bucket/object)')
argparser.add_argument('model_id',
    help='Model Id of your choosing to name trained model')
argparser.add_argument('project_id',
    help='Project Id of your Google Cloud Project')


def print_header(line):
  '''Format and print header block sized to length of line'''
  header_str = '='
  header_line = header_str * len(line)
  print('\n' + header_line)
  print(line)
  print(header_line)


def main(argv):
  service, flags = sample_tools.init(
      argv, 'prediction', 'v1.6', __doc__, __file__, parents=[argparser],
      scope=(
          'https://www.googleapis.com/auth/prediction',
          'https://www.googleapis.com/auth/devstorage.read_only'))
  print (service) 
  try:
    # Get access to the Prediction API.
    papi = service.trainedmodels()
    # List models.
    print_header('Fetching list of first ten models')
    result = papi.list(maxResults=10, project=flags.project_id).execute()
    print('List results:')
    pprint.pprint(result)

    # Start training request on a data set.
    print_header('Submitting model training request')
    body = {'id': flags.model_id, 'storageDataLocation': flags.object_name, 'modelType':'regression', 'storagePMMLLocation' : 'mlaas/baseball_pmml.xml'}
    start = papi.insert(body=body, project=flags.project_id).execute()
    print('Training results:')
    pprint.pprint(start)

    # Wait for the training to complete.
    print_header('Waiting for training to complete')
    while True:
      status = papi.get(id=flags.model_id, project=flags.project_id).execute()
      state = status['trainingStatus']
      print('Training state: ' + state)
      if state == 'DONE':
        break
      elif state == 'RUNNING':
        time.sleep(SLEEP_TIME)
        continue
      else:
        raise Exception('Training Error: ' + state)

      # Job has completed.
      print('Training completed:')
      pprint.pprint(status)
      break

    # Describe model.
    print_header('Fetching model description')
    result = papi.analyze(id=flags.model_id, project=flags.project_id).execute()
    print('Analyze results:')
    pprint.pprint(result)
    
    """result = papi.delete(id=flags.model_id, project=flags.project_id).execute()
    print('Model deleted.')"""

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize.')


if __name__ == '__main__':
  main(sys.argv)
