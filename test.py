import storage_utils
auth = storage_utils.get_auth()
print(auth['name'])
print(auth['pass'])
