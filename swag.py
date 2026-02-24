class NFAtoDFAConverter:
    def __init__(self):
        self.states = set()
        self.alphabet = {'a', 'b'}
        self.transitions = {}
        self.initial_states = set()
        self.final_states = set()
    def read_input(self):
        print("Введите множество состояний ")
        self.states = set(input().strip().split())
        print(f"Входной алфавит фиксированный: {', '.join(sorted(self.alphabet))}")
        print("Введите функцию переходов")
        print("Пример: 1 a 2")
        print("Введите 'end' для завершения ввода")
        self.transitions = {}
        while True:
            line = input().strip()
            if line.lower() == 'end':
                break
            if line:
                parts = line.split()
                if len(parts) == 3:
                    current, symbol, next_state = parts
                    if symbol in self.alphabet:
                        key = (current, symbol)
                        if key not in self.transitions:
                            self.transitions[key] = set()
                        self.transitions[key].add(next_state)
                    else:
                        print(f"Ошибка: символ '{symbol}' не входит в алфавит.")
        print("Введите начальное состояние")
        self.initial_states = {input().strip()}
        print("Введите конечные состояния")
        self.final_states = set(input().strip().split())
    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for epsilon_char in ['e', '']:
                epsilon_key = (state, epsilon_char)
                if epsilon_key in self.transitions:
                    for next_state in self.transitions[epsilon_key]:
                        if next_state not in closure:
                            closure.add(next_state)
                            stack.append(next_state)
        return frozenset(closure)
    def move(self, states, symbol):
        result = set()
        for state in states:
            key = (state, symbol)
            if key in self.transitions:
                result.update(self.transitions[key])
        return frozenset(result)

    def convert_to_dfa(self):
        start_state = self.epsilon_closure(self.initial_states)
        dfa_states = set()
        dfa_transitions = {}
        unprocessed_states = [start_state]
        dfa_states.add(start_state)
        dfa_final_states = set()
        while unprocessed_states:
            current_dfa_state = unprocessed_states.pop()
            if any(state in self.final_states for state in current_dfa_state):
                dfa_final_states.add(current_dfa_state)
            for symbol in ['a', 'b']:
                next_states = self.move(current_dfa_state, symbol)
                next_dfa_state = self.epsilon_closure(next_states)
                if next_dfa_state and next_dfa_state not in dfa_states:
                    dfa_states.add(next_dfa_state)
                    unprocessed_states.append(next_dfa_state)
                if next_dfa_state:
                    dfa_transitions[(current_dfa_state, symbol)] = next_dfa_state

        return start_state, dfa_states, dfa_transitions, dfa_final_states
    def state_set_to_name(self, state_set):
        if not state_set:
            return "∅"
        return ''.join(sorted(state_set))
    def print_dfa(self, start_state, dfa_states, dfa_transitions, dfa_final_states):
        print("Результат преоброзавания НКА -> ДКА")
        state_names = [self.state_set_to_name(state) for state in dfa_states]
        print(f"Множество состояний: {', '.join(sorted(state_names))}")
        print(f"Входной алфавит: {', '.join(sorted(self.alphabet))}")
        print("Функция переходов:")
        for (state, symbol), next_state in sorted(dfa_transitions.items(),
                                       key=lambda x: (self.state_set_to_name(x[0][0]), x[0][1])):
            state_str = self.state_set_to_name(state)
            next_state_str = self.state_set_to_name(next_state)
            print(f"D({state_str}, {symbol}) = {next_state_str}")
        start_str = self.state_set_to_name(start_state)
        print(f"Начальные состояния: {start_str}")
        final_names = [self.state_set_to_name(state) for state in dfa_final_states]
        print(f"Конечные состояния: {', '.join(sorted(final_names))}")
    def run_interactive(self):
        print("Преобразователь НКА в ДКА")
        self.read_input()
        start_state, dfa_states, dfa_transitions, dfa_final_states = self.convert_to_dfa()
        self.print_dfa(start_state, dfa_states, dfa_transitions, dfa_final_states)

def run_example():
    print("Запуск примера из задания")
    converter = NFAtoDFAConverter()
    converter.states = {'1', '2', '3'}
    converter.transitions = {
        ('1', 'a'): {'1', '2'},
        ('1', 'b'): {'3'},
        ('2', 'a'): {'2'},
        ('2', 'b'): {'1', '3'},
        ('3', 'a'): {'3'},
        ('3', 'b'): {'3'}
    }
    converter.initial_states = {'1'}
    converter.final_states = {'3'}
    start_state, dfa_states, dfa_transitions, dfa_final_states = converter.convert_to_dfa()
    converter.print_dfa(start_state, dfa_states, dfa_transitions, dfa_final_states)
def main():
    print("Программа преобразования НКА в ДКА")
    print("1. Запустить пример из задания")
    print("2. Ввести свой НКА")
    while True:
        choice = input("\nВыберите вариант ").strip()

        if choice == '1':
            run_example()
        elif choice == '2':
            converter = NFAtoDFAConverter()
            converter.run_interactive()
        else:
            print("Неверный выбор. Пожалуйста, введите 1 или 2")
if __name__ == "__main__":
    main()