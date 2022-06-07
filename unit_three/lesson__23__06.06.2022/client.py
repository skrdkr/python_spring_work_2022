# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50008              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    filename = "alice_in_wonderland.txt"
    s.send(bytes(f'GET {filename}', encoding='UTF-8')) #отправляем байтовый запрос на получение файла
    #открываем файл на запись данных с сервера. Пришлось писать абсолютный путь, так как через относительный непонятно,
    #куда записывал
    f = open("C:\\Users\\USER\\PycharmProjects\\pythonProject\\python_spring_work_2022\\unit_three"
             "\\lesson__23__06.06.2022"
             "\\client_alice_in_wonderland.txt", 'w', newline='') #добавление client для идентификации файла
    while True:                                                   #newline для удаление лишних пустых строк при записи
        data = s.recv(1024) #получаем данные с сервера
        data_decode = data.decode(encoding="ansi") #декодируем
        f.write(data_decode) #записываем в файл
        if not data:
            break
    f.close()
    print(f'{filename} received')
