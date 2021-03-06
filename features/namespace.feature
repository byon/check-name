Feature: Analysing namespace names

  Scenario: Namespaces in CamelCase are not reported
    Given source with namespace "Abc"
    And nested function "necessaryOrNamespaceIsNotAnalysed"
    When analysis is made
    Then analysis should report no rule violations

  Scenario: Namespaces not in CamelCase are reported
    Given source with namespace "aBc"
    And nested function "necessaryOrNamespaceIsNotAnalysed"
    When analysis is made
    Then analysis reports "namespace" "aBc" as "CamelCase" rule violation

  Scenario: Sequential namespaces are analysed
    Given source with namespace "ABC"
    And nested function "necessaryOrNamespaceIsNotAnalysed"
    And source with namespace "abc"
    And nested function "necessaryOrNamespaceIsNotAnalysed"
    When analysis is made
    Then analysis reports "namespace" "ABC" as "CamelCase" rule violation
    Then analysis reports "namespace" "abc" as "CamelCase" rule violation

  Scenario: Nested namespaces are analysed
    Given source with namespace "outer"
    And nested namespace "inner"
    And nested function "necessaryOrNamespaceIsNotAnalysed"
    When analysis is made
    Then analysis reports "namespace" "outer" as "CamelCase" rule violation
    And analysis reports "namespace" "inner" as "CamelCase" rule violation
