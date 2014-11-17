Feature: Analyzing namespace names

  Scenario: Namespaces not in CamelCase are reported
    Given source with namespace "aBc"
    When analysis is made
    Then analysis reports "namespace" "aBc" as "CamelCase" rule violation
