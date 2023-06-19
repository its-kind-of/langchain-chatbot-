import os
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
import pickle
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
from langchain.vectorstores.base import VectorStore

# add your openai api key
os.environ["OPENAI_API_KEY"] = " "

urls = [
    "https://jurasystems.in/"
]

loaders = UnstructuredURLLoader(urls=urls)
data = loaders.load()
text_splitter = CharacterTextSplitter(separator="\n",
                                      chunk_size=1000,
                                      chunk_overlap=200) # 10% or 20%
docs = text_splitter.split_documents(data)

if len(docs)==0:
    print("Doc has no data", "\n")
    print("DOC : ", docs)
    breakpoint()



embedding = OpenAIEmbeddings()
vectorStore_openAI = FAISS.from_documents(docs, embedding)


with open("faiss_store_openai.pkl", "wb") as file:
  pickle.dump(vectorStore_openAI, file)

with open("faiss_store_openai.pkl", "rb") as file:
  vectorStore = pickle.load(file)


llm = OpenAI(temperature=0, model_name='text-davinci-003')
chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorStore.as_retriever())


queryInput = input()
chain({"question": queryInput}, return_only_outputs=True)