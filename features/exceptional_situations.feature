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
    Given source with preprocessor condition "FOO"
    And nested namespace "violation"
    When analysis is made
    Then analysis should succeed

  Scenario: Syntax warnings are reported
    Given source file with a syntax warning
    When analysis is made
    Then analysis should succeed
    And warning cause should be reported

  Scenario: Syntax errors are reported
    Given source file with a syntax error
    When analysis is made
    Then analysis should fail
    And error cause should be reported
