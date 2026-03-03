Feature: Gestión de gastos
  Como estudiante
  Quiero registrar mis gastos
  Para controlar cuánto dinero gasto

  Scenario: Crear un gasto y comprobar cual es el total que llevo gastado
    Given un gestor de gastos vacío
    When añado un gasto de 5 euros llamado Café
    Then el total de dinero gastado debe ser 5 euros

  Scenario: Eliminar un gasto y comprobar cual es el total que llevo gastado
    Given un gestor con un gasto de 5 euros
    When elimino el gasto con id 1
    Then debe haber 0 gastos registrados

  Scenario: Crear y eliminar un gasto y comprobar que no he gastado dinero
    Given un gestor de gastos vacío
    When añado un gasto de 5 euros llamado Café
    And elimino el gasto con id 1
    Then debe haber 0 gastos registrados

  Scenario: Crear dos gastos diferentes y comprobar que el total que llevo gastado es la suma de ambos
    Given un gestor de gastos vacío
    When añado un gasto de 5 euros llamado Café
    And añado un gasto de 10 euros llamado Comida
    Then el total de dinero gastado debe ser 15 euros

  Scenario: Crear tres gastos diferentes que sumen 30 euros hace que el total sean 30 euros
    Given un gestor de gastos vacío
    When añado un gasto de 10 euros llamado Libros
    And añado un gasto de 10 euros llamado Bus
    And añado un gasto de 10 euros llamado Cena
    Then el total de dinero gastado debe ser 30 euros

  Scenario: Crear tres gastos de 10, 30, 30 euros y elimino el ultimo gasto la suma son 40 euros
    Given un gestor de gastos vacío
    When añado un gasto de 10 euros llamado Gasto1
    And añado un gasto de 30 euros llamado Gasto2
    And añado un gasto de 30 euros llamado Gasto3
    And elimino el gasto con id 3
    Then el total de dinero gastado debe ser 40 euros

  Scenario: Verificar que el número de gastos es correcto tras añadir y eliminar
    Given un gestor de gastos vacío
    When añado un gasto de 10 euros llamado A
    And añado un gasto de 10 euros llamado B
    And elimino el gasto con id 1
    Then debe haber 1 gastos registrados

  Scenario: Intentar añadir un gasto con cantidad negativa
    Given un gestor de gastos vacío
    When intento añadir un gasto de -10 euros
    Then el sistema debe lanzar un error de cantidad inválida

  Scenario: El total no cambia si elimino un ID que no existe
    Given un gestor con un gasto de 15 euros
    When elimino el gasto con id 999
    Then el total de dinero gastado debe ser 15 euros

  Scenario: Verificar que el ID aumenta automáticamente
    Given un gestor de gastos vacío
    When añado un gasto de 10 euros llamado Primero
    And añado un gasto de 20 euros llamado Segundo
    Then el gasto llamado Segundo debe tener el id 2