Feature: Exceptions returned for files
  Test the functionality of the exception returned for loaded ACH files

  Scenario: I get a list of exceptions for a file
    Given that I have a clean database
    And that I have posted the file "invalid_file_id.ach"
    When I request a list of exceptions for the file "invalid_file_id.ach"
    Then I should receive an error of "004" and a message of "Invalid File ID Modifier"

  Scenario: I get a list of exceptions for all files
    Given that I have a clean database
    And that I have posted the file "invalid_file_id.ach"
    When I request a list of exceptions for all files
    Then I should receive an error of "004" and a message of "Invalid File ID Modifier"

  Scenario: I get the unparsed record for a specific exception
    Given that I have a clean database
    And that I have posted the file "invalid_file_id.ach"
    When I request the unparsed record for the exception code "004"
    Then I should receive an unparsed record of "101 990000013 9876543212403291512i094101DEST NAME              ORIGIN NAME            XXXXXXXX"

