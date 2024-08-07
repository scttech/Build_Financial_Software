Feature: API /files

  Scenario: I get a 200 status code when we call /api/v1/files
    When I make a GET request to the endpoint /api/v1/files
    Then the status code should be 200

  Scenario: I get a 201 status code when we post to /api/v1/files
    When I make a POST request to the endpoint /api/v1/files
    Then the status code should be 201
