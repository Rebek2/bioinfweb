import { useState } from "react";
import React from 'react';
import { useHistory } from "react-router-dom";
import App4 from '../navbar/navBar'
import './add.css'
const Create = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [author, setAuthor] = useState('');
  const[isPending,setIsPending] = useState(false);
  const history = useHistory();


  

  const handleSubmit = (e) => {
    e.preventDefault();
    const blog = { title, content, author };
    setIsPending(true)
    fetch('http://127.0.0.1:8000/api/posts/', {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(blog)
    }).then(() => {

      history.push('/blog');
    })
    .catch((error) =>{
      setIsPending(false)
  })

  }    
  return (
    <div class="container" id='rozmiar'>
      <div class = 'mb-3' id='rozmiar'>
      <form onSubmit={handleSubmit}>
        <div class = 'mb-3'>
        <label for= "exampleFormControlInput1" class="form-label">Tytuł posta:</label>
        <input
          id='shadow-add' 
          type="text" 
          class='form-control'
          placeholder="Tytuł.."
          required 
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        </div>
        <div class ='mb-3'>
        <label for='exampleFormControlTextarea1' class="form-label">Tekst posta:</label>
        <textarea
        id='shadow-add' 
        class="form-control"  rows="3"
          required
          value={content}
          onChange={(e) => setContent(e.target.value)}
        ></textarea>
        </div>
        <div class = 'mb-3'>
        <label for= "exampleFormControlInput1" class="form-label">Autor:</label>
        <input 
        id='shadow-add' 
          type="text" 
          class='form-control'
         
          required 
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
        />
        </div>
        <center>
        {!isPending && <button id='shadow-add'  type = 'submit' class = 'btn btn-primary'>Dodaj post</button>}
        { isPending && <button disabled type = 'submit' class = 'btn btn-primary'>Dodawanie...</button>}
        </center>
      </form>
      </div>
    </div>
  );
}

function App3() {
  return (<div>
    <App4/>
    <div class ='mb-3'>
      <div class = 'container'>
      <h1 class="display-4">Dodaj nowy post</h1>
      </div>
      <Create/>
    
    </div>
    </div>
  )
}

export default App3;