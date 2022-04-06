import time
from settings import Start_NodeID, URL
from opcua import Client
import asyncio
import asyncua

from asyncua import Client


async def connect():
    async with Client(URL) as client:
        start_tags = client.get_node(Start_NodeID)  # получение нод
        tags_children = await start_tags.get_children()
        # print(tags_children)
        t = []
        for i in range(len(tags_children)):
            tag_child_low = await tags_children[i].get_children()
            # print(tag_child_low)
            for j in range(len(tag_child_low)):
                tag_child = client.get_node(tag_child_low[j])
                # print(tag_child)
                t.append(tag_child)
    return t, client


async def run(r, client):
    for k in range(len(r)):
        try:
            tag_child_value = await client.get_node(
                r[k]).get_value()  # получение значения тега, если StatusCode = Good
            # val = val_st.get_data_value() # полные данные тега
            # status = val.StatusCode.name  # получение StatusCode, если необходимо
            print(f"{r[k]} {tag_child_value}")
        except:
            tag_child_value = "Нет значения"
            print(f"{r[k]} {tag_child_value}")  # получение значения тега, если StatusCode = Bad

    # value = await node.read_value()
    # print(value)


async def main():
    task = asyncio.create_task(run(connect()))
    await task


if __name__ == "__main__":
    # t0 = time.time()
    asyncio.run(main())
    # t1 = time.time() - t0
    # print(t1)
