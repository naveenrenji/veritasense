from transformers import PegasusForConditionalGeneration
from transformers import PegasusTokenizer
from transformers import pipeline


def response_generator(question, context):
    input_text = f"Question: {question} Context: {context}"
    # Pick model
    model_name = "google/pegasus-xsum"

    # Load pretrained tokenizer
    pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)

    # Define PEGASUS model
    pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)

    # Create tokens
    tokens = pegasus_tokenizer(input_text, truncation=True, padding="longest", return_tensors="pt")
    
    # Summarize text
    #encoded_summary = pegasus_model.generate(**tokens)

    # Define summarization pipeline 
    summarizer = pipeline(
        "summarization", 
        model=model_name, 
        tokenizer="google/pegasus-xsum", 
        framework="pt"
    )

    # Create summary 
    summary = summarizer(input_text, min_length=30, max_length=150)
    response = summary[0]["summary_text"]

    return response

# print(answer_question(question, context))