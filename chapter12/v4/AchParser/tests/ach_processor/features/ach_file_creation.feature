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

  Scenario: Create an ACH file with a single transaction for customer "Sally Saver"
    Given I want to create an ACH file named "sally_saver.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH credits only and a standard entry class code of "PPD"
    And I want 1 entries per batch with random amounts between 100 and 100
    And I want to use individual names of "Sally Saver"
    And I want to have company name "My Company" and company id "1234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 1 entries in the file

  Scenario: Create an ACH file for company "Stellar Services Ltd"
    Given I want to create an ACH file named "stellar_services.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 2 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 100 and 5000
    And I want to use individual names of "Sal Monella, Pat Myback, Bill Board, Crystal Clear, Barry Cuda, Paige Turner, Justin Time, Terry Aki, Sue Flay, Holly Wood, Al Beback, Will Power, Sandy Beaches, Ella Vator"
    And I want to have company name "StellarServicesLtd" and company id "345678901"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 2 batch in the file
    And there should be 20 entries in the file

  Scenario: Create an ACH file for company "Petro Power LLC"
    Given I want to create an ACH file named "petro_power.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 2 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 100 and 5000
    And I want to use individual names of "Gail Force, Tex Drillman, Bard Dwyer, Will Drillman, Ollie Petro, Derrick Turner, Crude Oylman, Fossil Fielder, Slick Wheeler"
    And I want to have company name "PetroPowerLLC" and company id "234567890"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 2 batch in the file
    And there should be 20 entries in the file

  Scenario: Create an ACH file for company "Elemental Resources Inc"
    Given I want to create an ACH file named "elemental_resources.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 2 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 100 and 5000
    And I want to use individual names of "Rocky Gravel, Sandy Stone, Clay Earthman, Mason Bricks, Gemmy Quartz, Rusty Ironwood, Flint Stoney, Dusty Boulderson, Shelly Shale"
    And I want to have company name "ElementalResourcesInc" and company id "459876543"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 2 batch in the file
    And there should be 20 entries in the file

  Scenario: Create an ACH for for IAT
    Given I want to create an ACH file named "iat.ach"
    And I want to have an immediate destination of "990000013" with a destination name of "Metropolis Trust Bank"
    And I want to have an immediate origin of "691000134" with an origin name of "ASF APPLICATION SUPERVI"
    And I want to have 1 batch with ACH credits only and a standard entry class code of "IAT"
    And I want 1 entries per batch with random amounts between 100 and 100
    And I want to use individual names of "James Smith, Sarah Johnson, David Williams, Emma Martinez, Olivia Thomas"
    And I want to have company name "My Company" and company id "1234567890"
    And I want to override the field "odfi" to be "12345678"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 1 entries in the file

  Scenario: Create an ACH for for IAT with multiple batches
    Given I want to create an ACH file named "iat_multiple.ach"
    And I want to have an immediate destination of "990000013" with a destination name of "Metropolis Trust Bank"
    And I want to have an immediate origin of "691000134" with an origin name of "ASF APPLICATION SUPERVI"
    And I want to have 3 batch with ACH credits only and a standard entry class code of "IAT"
    And I want 1 entries per batch with random amounts between 100 and 100
    And I want to use individual names of "James Smith, Sarah Johnson, David Williams, Emma Martinez, Olivia Thomas"
    And I want to have company name "My Company" and company id "1234567890"
    And I want to override the field "odfi" to be "12345678"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 3 batch in the file
    And there should be 3 entries in the file

  Scenario: Create a file for "Elemental Resources Inc" with OFAC suspects
    Given I want to create an ACH file named "ofac_elemental_resources.ach"
    And I want to have an immediate destination of "990000013"
    And I want to have an immediate origin of "987654321"
    And I want to have 1 batch with ACH credits and debits and a standard entry class code of "PPD"
    And I want 10 entries per batch with random amounts between 100 and 5000
    And I want to use individual names of "Lou Pol, Lou Polle, Loo Pole, Will Chatham, Will Cheatam, Cash Stiller, Cash Steelor, Dusty Boulderson, Shelly Shale"
    And I want to have company name "ElementalResourcesInc" and company id "459876543"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 10 entries in the file

  Scenario: Create an IAT file with OFAC suspects
    Given I want to create an ACH file named "ofac_iat.ach"
    And I want to have an immediate destination of "990000013" with a destination name of "Metropolis Trust Bank"
    And I want to have an immediate origin of "691000134" with an origin name of "ASF APPLICATION SUPERVI"
    And I want to have 1 batch with ACH credits only and a standard entry class code of "IAT"
    And I want 1 entries per batch with random amounts between 100 and 100
    And I want to use individual names of "Lou Pol"
    And I want to have company name "My Company" and company id "1234567890"
    And I want to override the field "odfi" to be "12345678"
    When my ACH is created
    Then I should have a file of the same name
    And there should be 1 batch in the file
    And there should be 1 entries in the file



