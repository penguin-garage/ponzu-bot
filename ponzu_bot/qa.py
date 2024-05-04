from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from ponzu_bot.chatter import DEFAULT_INITIAL_PROMPT
from langgraph.prebuilt import ToolInvocation
from langgraph.prebuilt import ToolExecutor
from llama_index.core import VectorStoreIndex, get_response_synthesizer, load_index_from_storage, StorageContext
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

qa_prompt = """
下記のcontextに基づいて、questionに答えてください。
context:
{context}

question:
{question}

contextに回答に必要な情報が含まれていない場合、ポンズらしく分からないと回答してください。
"""

model = ChatOpenAI(model="gpt-4-turbo")

ponzu_qa_template = ChatPromptTemplate.from_messages([
    ("system", DEFAULT_INITIAL_PROMPT),
    ("human", qa_prompt)
])

storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(persist_dir="data/storage_context"),
    vector_store=SimpleVectorStore.from_persist_dir(persist_dir="data/storage_context"),
    index_store=SimpleIndexStore.from_persist_dir(persist_dir="data/storage_context"),
)

# don't need to specify index_id if there's only one index in storage context
vector_store_index = load_index_from_storage(storage_context)

retriever = VectorIndexRetriever(
    index=vector_store_index,
    similarity_top_k=5,
)

response_synthesizer = get_response_synthesizer()

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
)

class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")

@tool(args_schema=SearchInput, return_direct=True)
def penguin_vector_search(query: str) -> str:
    """
    Search the documents using the penguin garage community vector index and return the result
    """
    result=query_engine.query(query)
    return result

tools=[penguin_vector_search]

model_with_search_tool = model.bind_tools(tools, tool_choice="penguin_vector_search")
ponzu_qa_chain = ponzu_qa_template | model
search_query_chain = model_with_search_tool

def qa_bot(question: str) -> str:
    result = search_query_chain.invoke(question)
    print(result)
    tool_executor = ToolExecutor(tools)
    for tool_call in result.tool_calls:
        action = ToolInvocation(
            tool=tool_call["name"],
            tool_input=tool_call["args"]
        )
    response = tool_executor.invoke(action)
    result = ponzu_qa_chain.invoke({"context": response.response, "question": question})
    return result.content