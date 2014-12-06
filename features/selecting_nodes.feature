Feature: Selecting nodes
  As a user
  I want to filter the node analysis to files in specific directories
  So that I will get the feedback faster and avoid unnecessary details

  Scenario: Filtering header that is not in include list
    Given source file that includes file "a/header.hpp"
    And source file "a/header.hpp" contains namespace "violation"
    And filter includes directory "b"
    When analysis is made
    Then analysis should succeed

  Scenario: Including header that is in include list
    Given source file that includes file "a/header.hpp"
    And source file "a/header.hpp" contains namespace "violation"
    And filter includes directory "a"
    When analysis is made
    Then analysis should fail

  Scenario: Excluding headers from directories in include list
    Given source file that includes file "a/b/header.hpp"
    And source file "a/b/header.hpp" contains namespace "violation"
    And filter includes directory "a"
    And filter excludes directory "a/b"
    When analysis is made
    Then analysis should succeed
