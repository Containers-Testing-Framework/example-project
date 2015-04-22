Feature: Open ports

  Scenario: SSH port
    When Docker container is started
    Then port 22 is open
     And ssh connection can be established

  Scenario: Web port
    When Docker container is started
    Then port 80 is open
