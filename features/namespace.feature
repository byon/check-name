Feature: Analyzing namespace names

  Scenario: Namespaces in CamelCase are not reported
    Given source with namespace "Abc"
    When analysis is made
    Then analysis should report no rule violations

  Scenario: Namespaces not in CamelCase are reported
    Given source with namespace "aBc"
    When analysis is made
    Then analysis reports "namespace" "aBc" as "CamelCase" rule violation
