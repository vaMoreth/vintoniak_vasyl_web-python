from flask import url_for

def test_all_posts_page_loads(client):
    response = client.get(url_for('post_bp.posts'))
    assert response.status_code == 200
    
    
def test_post_create_page_loads(client, log_in_default_user):
    response = client.get(url_for('post_bp.create_post'))
    assert response.status_code == 200
    assert u'Додати пост' in response.data.decode("utf8")
    
    
def test_post_by_id_page_loads(client, init_database):
    response = client.get(url_for('post_bp.view_post', id=1))
    assert response.status_code == 200
    assert b'Written by:' in response.data
    
    
def test_post_edit_page_loads(client, init_database, log_in_default_user):
    response = client.get(url_for('post_bp.update_post', id=1))
    assert response.status_code == 200
    assert u'Оновлення поста' in response.data.decode("utf8")