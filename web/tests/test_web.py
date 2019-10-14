import pytest

from app.tables import device, report
from app.app import Application
from tornado.escape import json_decode, json_encode
from tornado.tcpclient import TCPClient


@pytest.fixture
def app():
    ap = Application()
    ap.init_db()
    return ap


@pytest.mark.gen_test
async def test_device(http_client, app):
    device_id = 0
    response = await http_client.fetch(
        'http://web/api/v1/device',
        method='POST',
        body=json_encode({
          "id": device_id
        })
    )
    assert response.code == 201
    await app.query(device.delete().where(device.c.id == device_id))


@pytest.mark.gen_test
async def test_report_fetch(http_client, app):
    # create device
    device_id = 0
    device_response = await http_client.fetch(
        'http://web/api/v1/device',
        method='POST',
        body=json_encode({
          "id": device_id
        })
    )

    # create report
    stream = await TCPClient().connect('tcp', 8999)
    data = "@{device_id}, test@".format(device_id=device_id)
    await stream.write(data.encode())
    stream.close()

    # get report
    report_response = await http_client.fetch(
        'http://web/api/v1/device/{id}/reports'.format(id=device_id)
    )

    # remove test data
    await app.query(report.delete().where(report.c.device_id == device_id))
    await app.query(device.delete().where(device.c.id == device_id))

    assert device_response.code == 201
    assert report_response.code == 200


@pytest.mark.gen_test
async def test_report_post(http_client, app):
    # create device
    device_id = 0
    device_response = await http_client.fetch(
        'http://web/api/v1/device/{id}/reports'.format(id=device_id),
        method='POST',
        body=json_encode({
            "id": device_id,
            "report": "test"
        })
    )
    assert device_response.code == 201
