from langchain_openai import ChatOpenAI

def load_llm(model_name):
    
    
    if model_name == "gpt-3.5-turbo":
        return ChatOpenAI(
            model=model_name,
            temperature=0,
            max_tokens=100
        )
    else:
        raise ValueError(
            "Model is not founded."
        )