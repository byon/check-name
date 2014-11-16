Feature: Exceptional situations
  As a user
  I want exceptional situations result in clear error messages
  So that I can focus on fixing the problems

  Scenario: Empty source file is not an error
    Given an empty source file
    When analysis is made
    Then analysis should succeed
    And there should be no output
