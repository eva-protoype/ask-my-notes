##the main file
from ask import ask
from store import get_collection, build_store

print("wanna submit ne new file?")

notes = get_collection()
while True:
    q = input("Ask your notes (or 'quit'): ")
    if q.strip().lower() == "quit":
        break
    print(ask(q, notes))