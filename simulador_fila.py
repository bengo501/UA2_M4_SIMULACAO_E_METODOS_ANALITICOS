import random

#parâmetros do gerador linear congruente
class RandomGenerator:
    def __init__(self, seed=1, a=1664525, c=1013904223, M=2**32):
        self.previous = seed
        self.a = a
        self.c = c
        self.M = M
    
    def NextRandom(self):
        self.previous = (self.a * self.previous + self.c) % self.M
        return self.previous / self.M if self.M != 0 else 0  #evita divisão por zero

#simulador de fila 
class QueueSimulator:
    def __init__(self, num_servers, capacity, arrival_min, arrival_max, service_min, service_max, num_events=100000):
        self.num_servers = num_servers
        self.capacity = capacity
        self.arrival_min = arrival_min
        self.arrival_max = arrival_max
        self.service_min = service_min
        self.service_max = service_max
        self.num_events = num_events
        self.generator = RandomGenerator(seed=42)
        
        self.clock = 0  #tempo atual
        self.queue = []  #lista de clientes na fila
        self.servers = [None] * num_servers  #estado dos servidores
        self.events = []  #lista de eventos futuros
        self.clients_lost = 0  #contador de clientes perdidos
        self.time_in_state = {i: 0 for i in range(capacity + 1)}  #tempo em cada estado
        self.last_event_time = 0
        
    def schedule_event(self, event_type, time):
        self.events.append((time, event_type))
        self.events.sort()
        
    def generate_arrival_time(self):
        return self.clock + self.arrival_min + (self.arrival_max - self.arrival_min) * self.generator.NextRandom()
    
    def generate_service_time(self):
        return self.service_min + (self.service_max - self.service_min) * self.generator.NextRandom()
    
    def process_arrival(self):
        if len(self.queue) < self.capacity:
            self.queue.append(self.clock)
            self.schedule_event("arrival", self.generate_arrival_time())
        else:
            self.clients_lost += 1
        
        for i in range(self.num_servers):
            if self.servers[i] is None and self.queue:
                self.start_service(i)
                
    def start_service(self, server_index):
        if self.queue:
            client = self.queue.pop(0)
            service_time = self.generate_service_time()
            self.servers[server_index] = self.clock + service_time
            self.schedule_event("departure", self.clock + service_time)
    
    def process_departure(self):
        for i in range(self.num_servers):
            if self.servers[i] and self.clock >= self.servers[i]:
                self.servers[i] = None
                self.start_service(i)
                
    def run(self):
        print(f"Iniciando simulação para fila G/G/{self.num_servers}/5...")
        print(f"Chegadas entre {self.arrival_min} e {self.arrival_max}, Atendimento entre {self.service_min} e {self.service_max}")
        self.schedule_event("arrival", self.generate_arrival_time())
        
        for i in range(self.num_events):
            if not self.events:
                print("Simulação finalizada antes de atingir", self.num_events, "eventos.")
                break
            
            self.clock, event_type = self.events.pop(0)
            time_elapsed = self.clock - self.last_event_time
            self.time_in_state[min(len(self.queue), self.capacity)] += time_elapsed
            self.last_event_time = self.clock
            
            if event_type == "arrival":
                self.process_arrival()
            elif event_type == "departure":
                self.process_departure()
            
            if i % 10000 == 0:
                print(f"Processando evento {i}: {event_type} - Tempo atual: {self.clock}")
        
        print("Simulação concluída. Clientes perdidos:", self.clients_lost)
        print("Distribuição de Estados:")
        for state, time in self.time_in_state.items():
            print(f"Estado {state}: {time / self.clock * 100:.2f}% do tempo")
        
        return {
            "Clientes Perdidos": self.clients_lost,
            "Tempo Global": self.clock,
            "Distribuição de Estados": {k: v / self.clock if self.clock > 0 else 0 for k, v in self.time_in_state.items()}
        }

#simular fila G/G/1/5
print("Rodando simulação para G/G/1/5...")
sim_gg1_5 = QueueSimulator(num_servers=1, capacity=5, arrival_min=2, arrival_max=5, service_min=3, service_max=5)
result_gg1_5 = sim_gg1_5.run()
print("Resultados G/G/1/5:", result_gg1_5) #imprimir resultado G/G/1/5

#simular fila G/G/2/5
print("Rodando simulação para G/G/2/5...")
sim_gg2_5 = QueueSimulator(num_servers=2, capacity=5, arrival_min=2, arrival_max=5, service_min=3, service_max=5)
result_gg2_5 = sim_gg2_5.run()
print("Resultados G/G/2/5:", result_gg2_5) #imprimir resultado G/G/2/5
