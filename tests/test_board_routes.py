# BOARD ROUTE TESTS

def test_create_board(client):
    board_params = {'title': 'Inspiration Board', 'owner': 'pytest'}

    response = client.post('/boards', json=board_params)
    response_body = response.get_json()

    assert response.status_code == 201
    assert 'board' in response_body
    assert response_body['board'] == {
        'board_id': 1,
        'title': 'Inspiration Board',
        'owner': 'pytest',
        'theme': 'grey',
        'cards': []
    }

def test_create_board_w_theme(client):
    board_params = {'title': 'Inspiration Board', 'owner': 'pytest', 'theme': 'green'}

    response = client.post('/boards', json=board_params)
    response_body = response.get_json()

    assert response.status_code == 201
    assert 'board' in response_body
    assert response_body['board'] == {
        'board_id': 1,
        'title': 'Inspiration Board',
        'owner': 'pytest',
        'theme': 'green',
        'cards': []
    }

def test_create_board_w_incomplete_data_fails_w_400_and_message(client):
    invalid_params = [
        {'title': 'Inspiration Board', 'owner': ''},
        {'title': '', 'owner': 'pytest'},
        {'title': 'Inspiration Board'}
    ]

    responses = [client.post('/boards', json=params) for params in invalid_params]
    bodies = [response.get_json() for response in responses]

    assert all([response.status_code == 400 for response in responses])
    assert all(['message' in response_body for response_body in bodies])

def test_get_boards_no_saved_boards(client):
    response = client.get('/boards')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'boards' in response_body
    assert response_body['boards'] == []

def test_get_boards_one_board(client, one_board):
    response = client.get('/boards')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'boards' in response_body
    assert len(response_body['boards']) == 1
    assert response_body['boards'][0] == {
        'board_id': 1,
        'title': 'One Board',
        'owner': 'one_board fixture',
        'theme': 'grey',
        'cards': []
    }

def test_get_board_by_id(client, one_board):
    response = client.get('/boards/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'board' in response_body
    assert response_body['board'] == {
        'board_id': 1,
        'title': 'One Board',
        'owner': 'one_board fixture',
        'theme': 'grey',
        'cards': []
    }

def test_get_board_by_id_missing_id(client, one_board):
    response = client.get('/boards/3')
    response_body = response.get_json()

    assert response.status_code == 404
    assert 'board' not in response_body
    assert 'message' in response_body
    assert response_body['message'] == "Board with id of 3 was not found"

def test_get_board_by_id_invalid_id(client, one_board):
    response = client.get('/boards/one')
    response_body = response.get_json()

    assert response.status_code == 400
    assert 'board' not in response_body
    assert 'message' in response_body
    assert response_body['message'] == "one is not a valid id"

def test_update_board_title_and_owner(client, one_board):
    updates = { "title": "A new name", "owner": "pytest" }
    response = client.patch('/boards/1', json=updates)
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'board' in response_body
    assert response_body['board']['title'] == "A new name"
    assert response_body['board']['owner'] == "pytest"

def test_update_board_title_only(client, one_board):
    updates = { "title": "A new name" }
    response = client.patch('/boards/1', json=updates)
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'board' in response_body
    assert response_body['board']['title'] == "A new name"

def test_update_board_theme_only(client, one_board):
    updates = { "theme": "heliotrope" }
    response = client.patch('/boards/1', json=updates)
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'board' in response_body
    assert response_body['board']['theme'] == "heliotrope"

def test_delete_board_by_id(client, one_board, one_board_w_three_cards):
    before_deleting_get = client.get('/boards')
    before_deleting_boards = before_deleting_get.get_json()['boards']

    assert len(before_deleting_boards) == 2

    response = client.delete('/boards/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'message' in response_body

    after_deleting_get = client.get('/boards')
    after_deleting_boards = after_deleting_get.get_json()['boards']

    assert len(after_deleting_boards) == 1