import heapq
from collections import defaultdict


RIGHT = 'R'
LEFT = 'L'
UP = 'U'
DOWN = 'D'


class GameOfEight:
    @staticmethod
    def get_neighbours(state: str) -> list[tuple[str, str]]:
        """
        Returns (State, Action) pairs where State is reached by performing Action
        """
        empty_idx = state.find('_')

        actions = []

        if 3 <= empty_idx:
            actions.append(UP)
        if empty_idx < 6:
            actions.append(DOWN)
        if not (empty_idx % 3 == 0):
            actions.append(LEFT)
        if not (empty_idx % 3 == 2):
            actions.append(RIGHT)

        neighbours = []

        for action in actions:
            neighbours.append((GameOfEight.move(state, action), action))

        return neighbours

    @staticmethod
    def move(state: str, action: str) -> str:
        if action == RIGHT:
            e_idx = state.find('_')
            state_list = list(state)
            state_list[e_idx], state_list[e_idx + 1] = state_list[e_idx + 1], state_list[e_idx]
            return ''.join(state_list)
        elif action == LEFT:
            e_idx = state.find('_')
            state_list = list(state)
            state_list[e_idx], state_list[e_idx - 1] = state_list[e_idx - 1], state_list[e_idx]
            return ''.join(state_list)
        elif action == DOWN:
            e_idx = state.find('_')
            state_list = list(state)
            state_list[e_idx], state_list[e_idx + 3] = state_list[e_idx + 3], state_list[e_idx]
            return ''.join(state_list)
        elif action == UP:
            e_idx = state.find('_')
            state_list = list(state)
            state_list[e_idx], state_list[e_idx - 3] = state_list[e_idx - 3], state_list[e_idx]
            return ''.join(state_list)

    @staticmethod
    def is_goal(state, goal_state) -> bool:
        return state == goal_state

    @staticmethod
    def visualise(state) -> str:
        rep = (f'+---+\n'
               f'+{state[0]}{state[1]}{state[2]}+\n'
               f'+{state[3]}{state[4]}{state[5]}+\n'
               f'+{state[6]}{state[7]}{state[8]}+\n'
               f'+---+\n\n')
        return rep


class Solver:
    def __init__(self, init_state: str, goal_state: str = '1234_5678'):
        self.init_state = init_state
        self.goal_state = goal_state

    def solve_bfs(self):
        parents = defaultdict(lambda: -1)
        actions = defaultdict(lambda: -1)

        node = self.init_state

        if GameOfEight.is_goal(node, self.goal_state):
            return 'Trivial Solution Exists'

        container = []
        heapq.heappush(container, node)
        explored = set()

        while True:
            if len(container) == 0:
                return 'No Solution Exists'

            node = heapq.heappop(container)
            explored.add(node)

            for c_state, c_action in GameOfEight.get_neighbours(node):
                if c_state not in explored:
                    parents[c_state] = node
                    actions[node, c_state] = c_action
                    if GameOfEight.is_goal(c_state, self.goal_state):
                        states_seq = []
                        moves_seq = []
                        while parents[c_state] != -1:
                            states_seq.append(c_state)
                            moves_seq.append(actions[parents[c_state], c_state])
                            c_state = parents[c_state]
                        states_seq.reverse()
                        moves_seq.reverse()
                        for state in states_seq:
                            print(GameOfEight.visualise(state))
                        return f'Found a solution!'
                    heapq.heappush(container, c_state)


# g = Solver('1234_5678', '_23145678')
g = Solver('13547_682', '1234_5678')
print(g.solve_bfs())


