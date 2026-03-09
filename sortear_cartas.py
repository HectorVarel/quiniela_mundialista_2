import random

jor = "1"

jugadores = [
    "Bryan", "Alfonso", "Brian", "Saem", "Fernando", "Miguel", "Félix", "Omar",
    "Manuel", "Juan Luis", "Erick", "Héctor", "Leo", "Jorge", "Victor", "Rafa", "Hora"
]

for jugador in jugadores:
    cartas = ["OD", "OD", "OT", "OT", "MA", "MA", "MA", "M", "M", 
              "J", "J", "T", "T", "E", "E", "DQ", "DQ"]
    random.shuffle(cartas)
    print(f"Cartas de {jugador} en la jornada {jor}: {cartas}")
