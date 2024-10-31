Feature: The /files endpoint
  Test the functionality of the /files endpoint

  Scenario: I want to get a list that contains a single file
    Given that I have a clean database
    And that I have posted the file "sample.ach"
    When I request a list of files
    Then I should have a single file named "sample.ach"
    And it should have a total credit amount of "1146114.80"
    And it should have a total debit amount of "78.25"
    And there should be no exceptions

  Scenario: I want to get a list of files
    Given that I have a clean database
    And that I have posted the file "sample.ach"
    And that I have posted the file "sample1.ach"
    When I request a list of files
    Then I should have a response that includes the file "sample.ach"
    And I should have a response that includes the file "sample1.ach"
    And there should be no exceptions

  Scenario: I should get a file even when it has an exception
    Given that I have a clean database
    And that I have posted the file "invalid_file_id.ach"
    When I request a list of files
    Then I should have a response that includes the file "invalid_file_id.ach"

  Scenario: I should not have any exceptions
    Given that I have a clean database
    And that I have posted the file "sample.ach"
    When I request a list of files
    Then the has_exceptions field should be False

  Scenario: I should get a file even when it has an exception
    Given that I have a clean database
    And that I have posted the file "invalid_file_id.ach"
    When I request a list of files
    Then I should have a response that includes the file "invalid_file_id.ach"
    And the has_exceptions field should be True
