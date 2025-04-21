import streamlit as st

st.title('Streamlit Demo')
st.header('This is a header')
st.subheader('This is a subheader')
st.text('This is some text.')

if st.button('Click me'):
    st.write('Button clicked!')

name = st.text_input('Enter your name:')
st.write(f'Hello, {name}!')

age = st.slider('Select your age:', 0, 100, 25)
st.write(f'Your age is: {age}')

options = st.selectbox('Choose an option:', ['Option 1', 'Option 2', 'Option 3'])
st.write(f'You selected: {options}')

uploaded_file = st.file_uploader('Upload a file')
if uploaded_file is not None:
    st.write('File uploaded successfully!')

st.sidebar.title('Sidebar Title')
st.sidebar.text('This is the sidebar.')