import glob
import os
import pytest
import requests

def read_graphql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

directory_path = dirname = os.path.join(
 os.path.dirname(__file__),
    './graphql_create'
)
graphql_files = glob.glob(os.path.join(directory_path, '*.graphql'))

@pytest.mark.parametrize('graphql_file', graphql_files)
def test_graphql_files(graphql_file):
    query = read_graphql_file(graphql_file)

    response = requests.post('http://localhost:5001/graphql', json={'query': query})

    assert response.status_code == 200
    result = response.json()

    assert 'errors' not in result


if __name__ == "__main__":
    pytest.main()
