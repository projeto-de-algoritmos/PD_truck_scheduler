def knapsack(v, w, C):
    N = len(v)
    m = {}

    for c in range(C+1):
        m[(0, c)] = 0

    for i in range(1, N+1):
        m[(i, 0)] = 0
        for c in range(1, C+1):
            if w[i-1] <= c:
                m[(i, c)] = max(m[(i-1, c)], v[i-1] + m[(i-1, c-w[i-1])])
            else:
                m[(i, c)] = m[(i-1, c)]

    return m[(N, C)]

# Info
v = [500, 250, 1500, 1200, 1200, 800]
w = [4, 3, 10, 12, 9, 6]
C = 30

while True:
    print('######Temporary Menu#######')
    print('Selecione uma opção')
    print('1.- Inserir um packete')
    print('2.- Mostrar packetes')
    print('3.- Eliminar packetes')
    print('4.- Calcular TRUCKS')
    print('5.- Mostrar TRUCKS')
    print('6.- Eliminar TRUCKS')
    print('7.- Sair')

    option = input()

    if option == '1':
        packet_weight = int(input("Ingrese peso de paquete"))
        packet_value = int(input("Ingrese valor de paquete"))
        w.append(packet_weight)
        v.append(packet_value)
    elif option == '2':
        for p in w:
            print(f"{w[p]}: {v[p]}")
    elif option == '3':
        print("WIP")
    elif option == '4':
        print("WIP")
        result = knapsack(v, w, C)
        print(result)
    elif option == '5':
        print("WIP")
    elif option == '6':
        print("WIP")        
    elif option == '7':
        break