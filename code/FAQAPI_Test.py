from FAQAPI import FAQAPI

if __name__ == "__main__":
    api = FAQAPI()
    answer = api.ask_question("What is BlackDuck?")
    print("The Answer is:", answer)