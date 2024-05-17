from langchain.memory import ConversationBufferWindowMemory
import asyncio

async def create_window_buffer_memory(length_history : int = 3):
    """
    This function creates a window buffer memory. This functions is used to saved the chat history as chunk of text in a window size of 3.

    Args:
        length_history (int): length of the window buffer

    Returns:
        memory (ConversationBufferWindowMemory): window buffer memory
    """
    memory = ConversationBufferWindowMemory(k = length_history, output_key='answer', memory_key="chat_history")
    return memory