Feature: Searching loaded ACH transactions
  For loaded files we should be able to search for transactions by various
  criteria such as individual name, amount, etc.

  Scenario: Search by individual name
    Given that I have a clean database
    And that I have posted the file "sally_saver.ach"
    When I search for transactions with search criteria "Sally Saver"
    Then I should receive a list of "1" transaction with the individual name of "Sally Saver"

  Scenario: Search by amount
    Given that I have a clean database
    And that I have posted the file "sally_saver.ach"
    When I search for transactions with search criteria "1.00"
    Then I should receive a list of "1" transaction with the amount of "1.00"

  Scenario: Search by amount range
    Given that I have a clean database
    And that I have posted the file "sally_saver.ach"
    When I search for transactions with search criteria "0.50 1.50"
    Then I should receive a list of "1" transaction with the amount of "1.00"