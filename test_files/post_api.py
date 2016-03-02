import requests
import zlib
import base64


def read_compress(file_name):
    with open(file_name, 'r') as ff:
        df = ff.read()
    return base64.b64encode(zlib.compress(df))


def post_data(host_url, username, password,
              data_name, target_column, workflow_elements, data_file):
    """
    To post data to the datarun api.
    Data are compressed (with zlib) and base64-encoded before being posted.

    :param host_url: api host url, such as http://127.0.0.1:8000/ (localhost)
    :param username: username to be used for authentication
    :param password: password to be used for authentication
    :param data_name: name of the raw dataset
    :param target_column: name of the target column
    :param workflow_elements: workflow elements associated with this dataset,
    e.g., feature_extractor, classifier
    :param data_file: name with absolute of the dataset file

    :type host_url: string
    :type username: string
    :type password: string
    :type data_name: string
    :type target_column: string
    :type workflow_elements: string
    :type data_file: string
    """

    data = {'name': data_name, 'target_column': target_column,
            'workflow_elements': workflow_elements}
    df = read_compress(data_file)
    data['files'] = {data_name + '.csv': df}
    url = host_url + '/runapp/rawdata/'
    # removing double /
    url = url[0:9] + url[9::].replace('//', '/')
    return requests.post(url, auth=(username, password), json=data)


def post_split(host_url, username, password,
               held_out_test, raw_data_id, random_state=42):
    url = host_url + '/runapp/rawdata/split/'
    # removing double /
    url = url[0:9] + url[9::].replace('//', '/')
    data = {'random_state': random_state, 'held_out_test': held_out_test,
            'raw_data_id': raw_data_id}
    return requests.post(url, auth=(username, password), json=data)


def post_submission_fold(host_url, username, password,
                         sub_id, sub_fold_id, train_is, test_is,
                         priority='low',
                         raw_data_id=None, list_submission_files=None):
    """
    To post submission on cv fold and submission (if not already posted).
    Submission files are compressed (with zlib) and base64-encoded before being
    posted.

    :param host_url: api host url, such as http://127.0.0.1:8000/ (localhost)
    :param username: username to be used for authentication
    :param password: password to be used for authentication
    :param sub_id: id of the submission on databoard
    :param sub_fold_id: id of the submission on cv fold on databoard
    :param train_is: train indices for the cv fold
    :param test_is: test indices for the cv fold
    :param priority: priority level to train test the model: low or high

    :type host_url: string
    :type username: string
    :type password: string
    :type sub_id: integer
    :type sub_fold_id: integer
    :type train_is: numpy array
    :type test_is: numpy array
    :type priority: string
    """
    # Compress train and test indices
    train_is = base64.b64encode(zlib.compress(train_is.tostring()))
    test_is = base64.b64encode(zlib.compress(test_is.tostring()))
    data = {'databoard_sf_id': sub_fold_id, 'databoard_s_id': sub_id,
            'train_is': train_is, 'test_is': test_is}
    # If the submission does not exist, post info needed to save it in the db
    if raw_data_id and list_submission_files:
        data['raw_data'] = raw_data_id
        data['files'] = {}
        for ff in list_submission_files:
            data['files'][ff.split('/')[-1]] = read_compress(ff)
    url = host_url + '/runapp/submissionfold/'
    # removing double /
    url = url[0:9] + url[9::].replace('//', '/')
    return requests.post(url, auth=(username, password), json=data)
