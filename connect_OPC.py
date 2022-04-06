"""
Подключение к OPCUA Wincc.
Перебор и получение значения тегов.
"""
import time
from settings import Start_NodeID, URL
from opcua import Client


def connect():
    try:
        client = Client(URL)
        client.connect()

        time_start = time.time()

        start_tags = client.get_node(Start_NodeID)  # получение нод
        tags_children = start_tags.get_children()  # получение вложений
        t = []
        for i in range(len(tags_children)):
            tag_child_low = tags_children[i].get_children()
            for j in range(len(tag_child_low)):
                tag_child = client.get_node(tag_child_low[j])
                t.append(tag_child)

        for k in range(len(t)):
            try:
                tag_child_value = client.get_node(
                    t[k]).get_value()  # получение значения тега, если StatusCode = Good
                # val = val_st.get_data_value() # полные данные тега
                # status = val.StatusCode.name  # получение StatusCode, если необходимо
                print(f"{t[k]}  {tag_child_value}")
            except:
                tag_child_value = "Нет значения"
                print(
                    f"{t[k]}    {tag_child_value}")  # получение значения тега, если StatusCode = Bad

        time_finish = time.time() - time_start
        print(time_finish)

    except ConnectionRefusedError:
        print('Подключение не установлено, т.к. конечный компьютер отверг запрос на подключение')

        client.disconnect()


connect()
