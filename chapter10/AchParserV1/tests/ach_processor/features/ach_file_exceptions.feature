Feature: Create ACH files with exception conditions
  The files that are created in this feature should all contain exceptions

  Scenario: Create an ACH file where the blocking factor is overridden
    Given I want to create an ACH file named "invalid_block_factor.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to override the field "blocking_factor" to be "20"
    And I want to have 1 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 1 and 100000
    And I want to use individual names of "Barry Cuda, Paige Turner, Justin Time, Terry Aki, Sue Flay, Holly Wood, Al Beback, Will Power, Sandy Beaches, Ella Vator"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be a "20" in the blocking factor field of the file header
    And there should be 1 batch in the file
    And there should be 10 entries in the file

  Scenario: Create an ACH file where the record size is overridden
    Given I want to create an ACH file named "invalid_record_size.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to override the field "record_size" to be "188"
    And I want to have 1 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 1 and 100000
    And I want to use individual names of "Barry Cuda, Paige Turner, Justin Time, Terry Aki, Sue Flay, Holly Wood, Al Beback, Will Power, Sandy Beaches, Ella Vator"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be a "188" in the record type 1 in field starting at 34 and ending at 37
    And there should be 1 batch in the file
    And there should be 10 entries in the file

  Scenario: Create an ACH file where the file totals are overridden
    Given I want to create an ACH file named "invalid_file_totals.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to override the field "file_control_total_debits" to be "123456789012"
    And I want to override the field "file_control_total_credits" to be "987654321098"
    And I want to have 1 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 1 and 100000
    And I want to use individual names of "Barry Cuda, Paige Turner, Justin Time, Terry Aki, Sue Flay, Holly Wood, Al Beback, Will Power, Sandy Beaches, Ella Vator"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be a "123456789012" in the record type 9 in field starting at 31 and ending at 43
    And there should be a "987654321098" in the record type 9 in field starting at 43 and ending at 55
    And there should be 1 batch in the file
    And there should be 10 entries in the file

  Scenario: Create an ACH file with invalid effective date on the batch
    Given I want to create an ACH file named "invalid_batch_effective_date.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH debits only and a standard entry class code of "PPD"
    And I want 1 entries per batch with random amounts between 100 and 100
    And I want to use individual names of "John Doe"
    And I want to have company name "My Company" and company id "1234567890"
    And I want to override the field "effective_entry_date" to be "YYMMDD"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 1 entries in the file

  Scenario: Create an ACH file with invalid file id
    Given I want to create an ACH file named "invalid_file_id.ach" with a File ID of "i"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH debits only and a standard entry class code of "PPD"
    And I want 1 entries per batch with random amounts between 100 and 100
    And I want to use individual names of "John Doe"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be a "i" in the File ID field of the file header
    And there should be 1 batch in the file
    And there should be 1 entries in the file

  Scenario: Create an ACH file with immediate destination that is not in table
    Given I want to create an ACH file named "invalid_immediate_destination.ach"
    And I want to have an immediate destination of "000000000"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH debits only and a standard entry class code of "PPD"
    And I want 1 entries per batch with random amounts between 100 and 100
    And I want to use individual names of "John Doe"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 1 entries in the file