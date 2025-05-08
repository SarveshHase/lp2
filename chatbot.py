import streamlit as st
from nltk.chat.util import Chat, reflections
import re

# Book inventory
books = {
    'fiction': ["The Alchemist", "1984", "The Great Gatsby"],
    'non-fiction': ["Sapiens", "Atomic Habits", "Educated"],
    'academic': ["Engineering Mathematics", "Human Anatomy", "Principles of Management"]
}

# Conversation patterns
patterns = [
    (r'hi|hello|hey', [
        'Hello! Welcome to BookWorld 📚. How can I assist you today?',
        'Hey there! Need help with books or orders?',
        'Hi! Looking for something to read?']),
    (r'how are you', [
        "I'm just a bot, but I'm here to help you find the perfect book!"]),
    (r'(.*)book(.*)', [
        'We have fiction, non-fiction, and academic books. What are you looking for?']),
    (r'(.*)fiction(.*)', [
        f"Our fiction section includes: {', '.join(books['fiction'])}. Would you like to buy one?"]),
    (r'(.*)non[- ]fiction(.*)', [
        f"Our non-fiction books include: {', '.join(books['non-fiction'])}. Would you like to buy one?"]),
    (r'(.*)academic(.*)', [
        f"Our academic books include: {', '.join(books['academic'])}. Interested in purchasing?"]),
    (r'(.*)price(.*)|(.*)cost(.*)', [
        'Most books range from ₹200 to ₹1500 depending on the category and author.']),
    (r'(.*)buy(.*)|(.*)order(.*)', [
        "Great! Let's proceed with your order. Type 'start order' to begin."]),
    (r'(.*)help(.*)', [
        'I can assist you with book categories, prices, and placing orders.']),
    (r'(.*)contact(.*)', [
        'You can email us at support@bookworld.com or call 1800-BOOK-123.']),
    (r'(.*)bye|goodbye|exit', [
        'Thank you for visiting BookWorld! 📖 Goodbye!']),
    (r'(yes|yeah|yep)', [
        "Great! Let's proceed with your order. Type 'start order' to begin."]),
]

# Initialize NLTK chatbot
chatbot = Chat(patterns, reflections)

# Streamlit app setup
st.set_page_config(
    page_title="BookWorld Chatbot",
    page_icon="📚",
    layout="centered"
)

st.title("📚 BookWorld Chatbot")
st.markdown("Ask me about books, prices, or place an order!")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.order_mode = False
    st.session_state.step = 0

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Order processing functions
def step_0(message):
    if message.lower() not in books:
        return "Category not found. Please choose from fiction, non-fiction, or academic."
    st.session_state.category = message.lower()
    st.session_state.step = 1
    return f"You selected {message} category. We have {', '.join(books[message.lower()])} books for this category. Which one would you like to buy? You can also type 'nothing' if you would like to exit."

def step_1(message):
    if message.lower() == 'nothing':
        st.session_state.order_mode = False
        st.session_state.step = 0
        return "Thank you for chatting with us. Feel free to browse more books!"
    
    # Check if the book exists in the selected category
    if message.lower() not in [book.lower() for book in books[st.session_state.category]]:
        return f"Sorry, we don't have '{message}' in our {st.session_state.category} collection. Please select from: {', '.join(books[st.session_state.category])}"
    
    st.session_state.book = message
    st.session_state.step = 2
    return f"'{message}' added to your cart. Cost is ₹500. Should I confirm the order? (yes/no)"

def step_2(message):
    st.session_state.order_mode = False
    st.session_state.step = 0
    
    if message.lower() in ['yes', 'y', 'yeah', 'yep', 'sure']:
        return "Order confirmed! Your book will be delivered soon. Thank you for shopping with BookWorld! 📖"
    else:
        return "No worries! Your order has been cancelled. Feel free to browse more books!"

step_functions = {
    0: step_0,
    1: step_1,
    2: step_2
}

# Get user input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Process response
    if st.session_state.order_mode:
        response = step_functions[st.session_state.step](user_input)
    elif re.search(r'\bstart\s+order\b', user_input.lower()):
        st.session_state.order_mode = True
        st.session_state.step = 0
        response = "Ok let's start. Which category book would you like to browse? (fiction/non-fiction/academic)"
    else:
        response = chatbot.respond(user_input)
        if not response:
            response = "I'm not sure how to respond to that. Can I help you find a book or place an order?"
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display bot response
    with st.chat_message("assistant"):
        st.write(response)

# Sidebar with book categories
with st.sidebar:
    st.header("Book Categories")
    
    for category, book_list in books.items():
        with st.expander(f"{category.capitalize()} Books"):
            for book in book_list:
                st.write(f"- {book}")
    
    st.markdown("---")
    st.markdown("**Contact Us:**  \nsupport@bookworld.com  \n1800-BOOK-123")