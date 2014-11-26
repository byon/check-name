Feature: Exceptional situations
  As a user
  I want exceptional situations result in clear error messages
  So that I can focus on fixing the problems

  Scenario: Empty source file is not an error
    Given an empty source file
    When analysis is made
    Then analysis should succeed
    And there should be no output

  Scenario: Path to missing source file is an error
    Given source file does not exist
    When analysis is made
    Then analysis should fail
    And analysis error cause should be missing source file

  Scenario: Options can be passed to clang
    Given source file with namespace "f" inside preprocessor condition "FOO"
    And preprocessor definitions contain "FOO"
    When analysis is made
    Then analysis should succeed
