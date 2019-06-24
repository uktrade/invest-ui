from django.urls import reverse


def test_sitemap(client):
    response = client.get(reverse('sitemap'))

    assert response.status_code == 200
