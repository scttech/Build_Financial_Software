Feature: Create ACH files
  There is a need to be able to easily create ACH files

  Scenario: Create an ACH file with a PPD batch
    Given I want to create an ACH file named "ppd-credits.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH credits only and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 1 and 1000
    And I want to use individual names of "John Doe, Jane Doe"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 10 entries in the file

  Scenario: Create an ACH file with multiple PPD batches
    Given I want to create an ACH file named "ppd-multiple.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 5 batch with ACH credits only and a standard entry class code of "PPD"
    And I want 20 entries per batch with random amounts between 1 and 100000
    And I want to use individual names of "John Doe, Jane Doe"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 5 batch in the file
    And there should be 100 entries in the file

  Scenario: Create an ACH file with a single batch and debit entries
    Given I want to create an ACH file named "ppd-debits.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH debits only and a standard entry class code of "PPD"
    And I want 5 entries per batch with random amounts between 1 and 100000
    And I want to use individual names of "John Doe, Jane Doe"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 5 entries in the file

  Scenario: Create an ACH file with a single batch and mixed entries
    Given I want to create an ACH file named "ppd-mixed.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 1 and 100000
    And I want to use individual names of "John Doe, Jane Doe"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 10 entries in the file

  Scenario: Create an ACH file with a single batch and a single credit
    Given I want to create an ACH file named "ppd-single-credit.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH credits only and a standard entry class code of "PPD"
    And I want 1 entries per batch with random amounts between 100 and 100
    And I want to use individual names of "John Doe"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 1 entries in the file

  Scenario: Create an ACH file with a single batch and a single debit
    Given I want to create an ACH file named "ppd-single-debit.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH debits only and a standard entry class code of "PPD"
    And I want 1 entries per batch with random amounts between 100 and 100
    And I want to use individual names of "John Doe"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 1 entries in the file

  Scenario: Create an ACH file where the individual name is short
    Given I want to create an ACH file named "ppd-short-names.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 1 and 100000
    And I want to use individual names of "Barry Cuda, Paige Turner, Justin Time, Terry Aki, Sue Flay, Holly Wood, Al Beback, Will Power, Sandy Beaches, Ella Vator"
    And I want to have company name "My Company" and company id "1234567890"
    And I want to have individual names with an invalid length
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 10 entries in the file

  Scenario: Create an ACH file where the File ID is set
    Given I want to create an ACH file named "specific_file_id.ach" with a File ID of "C"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 1 and 100000
    And I want to use individual names of "Barry Cuda, Paige Turner, Justin Time, Terry Aki, Sue Flay, Holly Wood, Al Beback, Will Power, Sandy Beaches, Ella Vator"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be a "C" in the File ID field of the file header
    And there should be 10 entries in the file

