Feature: The inventory service back-end
    As an Inventory Admin
    I need a RESTful service
    So that I can keep track of all my inventories

Background:
    Given the following inventories
        | id | name        | quantity | status  |
        |  1 | shampoo     | 5        | new     |
        |  2 | conditioner | 3        | openBox |
        |  3 | body lotion | 8        | used    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Inventory
    When I visit the "Home Page"
    And I set the "Name" to "face cream"
    And I set the "Quantity" to "12"
    And I select the "Status" to "new"
    And I press the "Create" button
    Then I should see the message "Success"

    When I set the "ID" to "4"
    And I press the "Retrieve" button
    Then I should see "face cream" in the "Name" field
    And I should see "new" in the "Status" field
    And I should see "12" in the "Quantity" field

Scenario: Read an Inventory
    When I visit the "Home Page"
    And I set the "ID" to "1"
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "shampoo" in the "Name" field
    And I should see "5" in the "Quantity" field
    And I should see "new" in the "Status" field

Scenario: Update an Inventory
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "shampoo" in the "Name" field
    And I should see "5" in the "Quantity" field
    And I should see "new" in the "Status" field
    When I set the "Quantity" to "99"
    And I press the "Update" button
    Then I should see the message "Success"
    Then I should see "99" in the "Quantity" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "99" in the results
    Then I should not see "5" in the results

"""
Scenario: List all pets
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "shampoo" in the results
    And I should see "conditioner" in the results
    And I should see "body lotion" in the results

Scenario: List all dogs
    When I visit the "Home Page"
    And I set the "Category" to "dog"
    And I press the "Search" button
    Then I should see "fido" in the results
    And I should not see "kitty" in the results
    And I should not see "leo" in the results

"""