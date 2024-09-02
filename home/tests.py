from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from django.test import Client
from unittest.mock import patch


@pytest.mark.parametrize("method, usr, post_data, expected_data, expected_user, expected_all_user_data, test_id", [
    ("GET", "guest", None, "Guest has no data", "guest", {}, "guest_get"),
    ("POST", "guest", {'username_input': 'user1', 'user_data': 'data1'}, 'data1', 'user1', {'user1': 'data1'},
     "user1_post"),
    ("POST", "guest", {'username_input': 'user2', 'user_data': ''}, 'No data was entered for the user', 'user2',
     {'user2': 'No data was entered for the user'}, "user2_post_empty_data"),
    ("POST", "guest", {'username_input': '', 'user_data': 'data'}, 'Guest has no data', 'guest', {},
     "guest_post_no_username"),
    ("POST", "guest", {'username_input': 'user3', 'user_data': None}, 'No data was entered for the user', 'user3',
     {'user3': 'No data was entered for the user'}, "user3_post_none_data"),
], ids=lambda val: val[-1])
@patch('home.views.my_cache')
def test_home_view(mock_my_cache, method, usr, post_data, expected_data, expected_user, expected_all_user_data,
                   test_id):
    client = Client()
    mock_my_cache.exists.side_effect = lambda x: x in expected_all_user_data
    mock_my_cache.fetch.side_effect = lambda x: expected_all_user_data[x].encode(
        'utf-8') if x in expected_all_user_data else None
    mock_my_cache.get_all.return_value = expected_all_user_data

    # Act
    if method == 'GET':
        response = client.get(reverse('home'), {'usr': usr})
    else:
        response = client.post(reverse('home'), post_data)

    # Assert
    assert response.status_code == 200
    assert response.context['data'] == expected_data
    assert response.context['user'] == expected_user
    assert response.context['all_user_data'] == expected_all_user_data


@pytest.mark.parametrize("url, template, test_id", [
    (reverse('users'), "index.html", "users_view"),
    (reverse('about'), "about.html", "about_view"),
], ids=lambda val: val[-1])
def test_static_views(url, template, test_id):
    client = Client()

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert template in [t.name for t in response.templates]
