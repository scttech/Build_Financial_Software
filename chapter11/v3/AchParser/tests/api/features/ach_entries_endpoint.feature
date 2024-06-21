Feature: The /files/{fileId}/batches/{batchId}/entries endpoint
  Test returning entries for a batch

  Scenario: I want to check the entries for a Checking Application
    Given that I have a clean database
    And that I have posted the file "ppd-single-credit.ach"
    When I request entries for a file and batch
    Then I should have a response that includes all applications of "Checking"
