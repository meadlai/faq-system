from langchain.chains import RetrievalQA
from FAQAPI import FAQAPI

if __name__ == "__main__":
    api = FAQAPI()
    while True:
        query = input('you: ')
        print("The Question is: ", query)
        if query == 'q':
            break
        answer = api.ask_question(query)
        print("The Answer is:", answer)

