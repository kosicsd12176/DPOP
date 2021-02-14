import threading
import time

from packages.agent import Agent
from utils.util_message import util_message_propagation


class AgentThread(threading.Thread):
    def __init__(self, agent: Agent, nodes_dict: dict, cycles=None):
        threading.Thread.__init__(self)
        if cycles is None:
            cycles = []
        self.agent = agent
        self.name = agent.name
        self.cycles = cycles
        self.nodes_dict = nodes_dict

    def run(self) -> None:
        print(f"Starting agent {self.name}...")
        # Get lock to synchronize threads
        handle_util_messages(self.agent, self.nodes_dict, self.cycles)
        # Free lock to release next thread


threadLock = threading.Lock()


def handle_util_messages(agent: Agent, nodes_dict: dict, cycles_counter: list):
    variables_counter = 0
    while variables_counter < len(agent.variables):
        print(f"Executing thread for agent {agent.name}\n")
        for v in agent.variables.keys():
            node = nodes_dict[v]
            if not node.util_message_sent:
                if len(node.children) == 0:
                    threadLock.acquire()
                    cycles_counter.append(util_message_propagation(node))
                    variables_counter += 1
                    threadLock.release()
                elif len(node.children) == len(node.util_messages.keys()):
                    threadLock.acquire()
                    if node.root:
                        node.set_util_message_sent(True)
                    else:
                        cycles_counter.append(util_message_propagation(node))
                    variables_counter += 1
                    threadLock.release()

    print(f"Thread for agent {agent.name} finished!\n")
