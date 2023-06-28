import os

import pytest
import requests

stage = os.environ.get("STAGE", "dev")


@pytest.mark.integration(method="POST", endpoint="/examples/{example_id}")
def test_example_endpoint_status_code_response_is_200(headers, control_table):

    # Add pre-conditions here, if needed
    # control_table.put_item(Item={ "PK": "TEST#123"})

    response = requests.post(
        f"https://api.goentri.com/v2/{stage}/template/examples/123",
        headers=headers,
    )

    assert response.status_code == 200

    # Add post-conditions here, if needed
    # control_table.delete_item(Key={"PK": "TEST#123"})
