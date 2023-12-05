def knapsack(v, w, C):
    N = len(v)
    m = {}

    for c in range(C + 1):
        m[(0, c)] = 0

    for i in range(1, N + 1):
        m[(i, 0)] = 0
        for c in range(1, C + 1):
            if w[i - 1] <= c:
                m[(i, c)] = max(m[(i - 1, c)], v[i - 1] + m[(i - 1, c - w[i - 1])])
            else:
                m[(i, c)] = m[(i - 1, c)]

    # Find the selected items
    selected_items = []
    i, c = N, C
    while i > 0 and c > 0:
        if m[(i, c)] != m[(i - 1, c)]:
            selected_items.append(i - 1)
            c -= w[i - 1]
        i -= 1

    # Delete selected items from the list
    for item in sorted(selected_items, reverse=True):
        del w[item]
        del v[item]

    return m[(N, C)]

# Info
v = [500, 250, 1500, 1200, 1200, 800]
w = [4, 3, 10, 12, 9, 6]
C = 30
batch = []
batchNumber = 0

while True:
    print('######Temporary Menu#######')
    print('Selecione uma opção')
    print('1.- Inserir um packete')
    print('2.- Mostrar packetes')
    print('3.- Eliminar packetes')
    print('4.- Calcular batch')
    print('5.- Mostrar batch')
    print('6.- Eliminar batch')
    print('7.- Sair')

    option = input()

    if option == '1':
        packet_weight = int(input("Ingrese peso de paquete"))
        packet_value = int(input("Ingrese valor de paquete"))
        w.append(packet_weight)
        v.append(packet_value)
    elif option == '2':
        if len(w) > 0:
            for i in range(len(w)):
                print(f"{w[i]}: {v[i]}")
        else:
            print("nao tem pacote para mostrar")
    elif option == '3':
        if len(w) > 0:
            print("Lista de pacotes:")
            for i in range(len(w)):
                print(f"{i + 1}. Peso: {w[i]}, Valor: {v[i]}")

            index_to_delete = int(input("Coloque index del pacote: ")) - 1

            if 0 <= index_to_delete < len(w):
                del w[index_to_delete]
                del v[index_to_delete]
                print("Pacote eliminado.")
            else:
                print("Pacote nao encontrado.")
        else:
            print("nao tem pacote para eliminar")
    elif option == '4':
        while len(v) > 0 and len(w) > 0:
            print("Calculating maximum value of batch...")
            result = knapsack(v, w, C)
            print(f"Maximum value of batch: {result}")
            batchNumber += 1
            start_time = int(input("Enter start time: "))
            end_time = int(input("Enter end time: "))
            new_batch = {'id': batchNumber, 'value': result, 'start time': start_time, 'end time': end_time}
            batch.append(new_batch)
        if len(v) <= 0 and len(w) <= 0:
            print("Nao tem mais pacotes para agrupar")
    elif option == '5':
        if len(batch) > 0:
            for i in range(len(batch)):
                print(batch[i])
        else:
            print("nao tem batch para mostrar")
    elif option == '6':
        if len(batch) > 0:
            print("Lista de batches:")
            for i in range(len(batch)):
                print(f"{batch[i]}")

            batch_to_delete = int(input("Coloque ID do batch a eliminar: "))

            found_batch = None
            for b in batch:
                if b['id'] == batch_to_delete:
                    found_batch = b
                    break

            if found_batch:
                batch.remove(found_batch)
                print("Batch eliminado.")
            else:
                print("Batch nao encontrado.")
        else:
            print("nao tem batch para eliminar")   
    elif option == '7':
        break