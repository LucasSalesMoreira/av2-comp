def remove_unit_productions(grammar):
    updated_grammar = {variable: [production for production in productions] for variable, productions in grammar.items()}

    # Passo 1: Encontrar produções unitárias e adicioná-las à gramática atualizada
    unit_productions = []
    for variable, productions in grammar.items():
        for production in productions:
            if len(production) == 1 and production.isupper():
                unit_productions.append((variable, production))

    for unit_production in unit_productions:
        variable, unit_variable = unit_production
        if unit_variable in updated_grammar:
            unit_productions_to_add = [(variable, production) for production in updated_grammar[unit_variable]]
            for unit_production_to_add in unit_productions_to_add:
                if unit_production_to_add not in unit_productions:
                    unit_productions.append(unit_production_to_add)

    for unit_production in unit_productions:
        variable, unit_variable = unit_production
        if unit_variable in updated_grammar:
            updated_productions = updated_grammar[variable]
            unit_productions_to_add = [(variable, production) for production in updated_grammar[unit_variable]]
            for unit_production_to_add in unit_productions_to_add:
                if unit_production_to_add not in updated_productions:
                    updated_productions.append(unit_production_to_add)

    # Passo 2: Remover as produções unitárias da gramática atualizada
    for variable in updated_grammar:
        updated_productions = updated_grammar[variable]
        updated_grammar[variable] = [production for production in updated_productions if len(production) > 1 or not production.isupper()]

    return updated_grammar


def remove_empty_productions(grammar):
    updated_grammar = {variable: [production for production in productions if production != ''] for variable, productions in grammar.items()}
    nullable_variables = set()
    updated_productions = {variable: set(productions) for variable, productions in updated_grammar.items()}

    # Passo 1: Encontrar variáveis nulas
    while True:
        nullable_variables_prev = set(nullable_variables)
        for variable, productions in updated_grammar.items():
            if any(all(symbol in nullable_variables for symbol in production) for production in productions):
                nullable_variables.add(variable)
        if nullable_variables == nullable_variables_prev:
            break

    # Passo 2: Remover produções vazias
    for variable, productions in updated_grammar.items():
        updated_productions[variable] = set(production for production in productions if production != 'ε')

    # Passo 3: Adicionar produções adicionais para variáveis nulas
    for variable, productions in updated_grammar.items():
        for nullable_variable in nullable_variables:
            updated_productions[variable].update(production.replace(nullable_variable, '') for production in productions if nullable_variable in production)

    return {variable: list(productions) for variable, productions in updated_productions.items()}


def rename_variables(grammar):
    updated_grammar = {variable: [production for production in productions] for variable, productions in grammar.items()}
    new_variable_counter = 0
    used_variables = set(updated_grammar.keys())
    new_variable_mapping = {}

    def generate_new_variable():
        nonlocal new_variable_counter
        while True:
            new_variable_counter += 1
            new_variable = 'X' + str(new_variable_counter)
            if new_variable not in used_variables:
                used_variables.add(new_variable)
                return new
