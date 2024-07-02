Feature: Parsing a Nacha Batch Header

  Scenario: We have a record type 5
    When we parse the batch header "5200Company name    DiscretionaryData   1234567890ARCComp desc 0216232302160471061000010000001"
    Then the record type should be 5