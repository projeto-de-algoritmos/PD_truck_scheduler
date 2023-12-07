def weighted_interval_scheduling(batches):
    sorted_batches = sorted(batches, key=lambda x: x['end time'])
    
    n = len(sorted_batches)
    dp = [0] * n
    selected_batches = [None] * n 
    
    dp[0] = sorted_batches[0]['value']
    selected_batches[0] = [sorted_batches[0]['id']]

    for i in range(1, n):
        latest_non_overlapping = -1
        for j in range(i - 1, -1, -1):
            if sorted_batches[j]['end time'] <= sorted_batches[i]['start time']:
                latest_non_overlapping = j
                break

        include_current = sorted_batches[i]['value'] + (dp[latest_non_overlapping] if latest_non_overlapping != -1 else 0)
        exclude_current = dp[i - 1]

        if include_current > exclude_current:
            dp[i] = include_current
            selected_batches[i] = selected_batches[latest_non_overlapping] + [sorted_batches[i]['id']]
        else:
            dp[i] = exclude_current
            selected_batches[i] = selected_batches[i - 1]

    return dp[-1], selected_batches[-1]

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

    selected_items = []
    i, c = N, C
    while i > 0 and c > 0:
        if m[(i, c)] != m[(i - 1, c)]:
            selected_items.append(i - 1)
            c -= w[i - 1]
        i -= 1

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
    print('7.- Calcular batch')
    print('8.- Sair')

    option = input()

    if option == '1':
        packet_weight = int(input("Ingrese peso de paquete"))
        if packet_weight < 0:
            print("peso debe ser maior a 0")
        else:
            packet_value = int(input("Ingrese valor de paquete"))
            if packet_value < 0:
                print("valor debe ser maior a 0")
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
            if index_to_delete < 0:
                print("Indice nao debe ser menor que 0")
            else:
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
            print("Calculating batch...")
            start_h = input("Enter start hour for job")
            start_m = input("Enter start minute for job")
            if(int(start_h)<0 or int(start_h)>23 or int(start_m)<0 or int(start_m)>60):
                print("Start time invalid")
            else:
                start_time = str(start_h) + str(start_m)
                start_time = int(start_time)
                
                end_h = input("Enter end time for job")
                end_m = input("Enter entime for job")
                
                if(int(end_h)<0 or int(end_h)>23 or int(end_m)<0 or int(end_m)>60):
                    print("end time invalid")
                else:
                    end_time = str(end_h) + str(end_m)
                    end_time = int(end_time)
                    if(end_time<start_time):
                        print("end time cant be less tan start time")
                    else:
                        batchNumber += 1
                        result = knapsack(v, w, C)
                        print(f"Maximum value of batch: {result}")
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
            if batch_to_delete < 0:
                print("id nao debe ser menor a 0")
            else:
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
        sched_num = 0
        while len(batch) > 0:
            max_value, selected_batches = weighted_interval_scheduling(batch)
            print(f"Valor total de schedule {sched_num + 1}: {max_value}")
            print(f"Contenido de schedule {sched_num + 1}:")
        
            for batch_id in selected_batches:
                batch_index = next((index for (index, d) in enumerate(batch) if d["id"] == batch_id), None)

                if batch_index is not None:
                    selected_batch = batch[batch_index]
                
        
                    print(f"ID: {selected_batch['id']}")
                    print(f"Valor: {selected_batch['value']}")
                    print(f"Start time: {selected_batch['start time']}")
                    print(f"End time: {selected_batch['end time']}")
                
                    # Remove the batch from the 'batch' list
                    del batch[batch_index]
            sched_num += 1
        if len(batch) < 1:
            print("nao tem mais batches para schedule")
    elif option == '8':
        break