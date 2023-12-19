from abc import ABC, abstractmethod
from typing import List
import random


class Muddler(ABC):  # abstract class... instantiate one of the subclasses below.
    def __init__(self, max_value=255):
        self.max_value = max_value

    @abstractmethod
    def muddle(self, input_sequence: List[int]) -> List[int]:
        pass


class PacketwiseMuddler(Muddler):
    def __init__(self, max_value=255, packet_size=24, errors_per_packet=1):
        super().__init__(max_value)
        self.packet_size = packet_size
        self.errors_per_packet = errors_per_packet

    def muddle(self, input_sequence: List[int]) -> List[int]:
        output = []
        packet_num = 0
        while packet_num < len(input_sequence)/self.packet_size:
            start = packet_num * self.packet_size
            end = min(len(input_sequence), (packet_num+1)*self.packet_size)
            packet = input_sequence[start:end]
            if len(packet) < self.packet_size:
                print("input_sequence wasn't an integer number of packets.")
                packet.extend([0]*(self.packet_size - len(packet)))
            targets_used = []
            for i in range(self.errors_per_packet):
                target = random.randint(0, self.packet_size - 1)
                replacement = random.randint(0, self.max_value)
                if packet[target] != replacement and target not in targets_used:  # if this actually is a change...
                    packet[target] = replacement
                    targets_used.append(target)
                else:  # try again.
                    i -= 1
            output.extend(packet)
            packet_num += 1
        return output


class ProbabilisticMuddler(Muddler):
    def __init__(self, max_value: int = 255, error_rate: float = 0.05):
        super().__init__(max_value)
        self.error_rate = error_rate

    def muddle(self, input_sequence: List[int]) -> List[int]:
        output = []
        for n in input_sequence:
            if random.random() < self.error_rate:
                output.append(random.randint(0, self.max_value))
            else:
                output.append(n)
        return output
